#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// =============================================================================
// CACHE IMPLEMENTATION
// =============================================================================

interface CacheEntry<T> {
  data: T;
  expiresAt: number;
}

class TTLCache<T> {
  private cache = new Map<string, CacheEntry<T>>();
  private defaultTTL: number;

  constructor(defaultTTLSeconds: number) {
    this.defaultTTL = defaultTTLSeconds * 1000;
  }

  get(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      return null;
    }
    return entry.data;
  }

  set(key: string, data: T, ttlSeconds?: number): void {
    const ttl = ttlSeconds ? ttlSeconds * 1000 : this.defaultTTL;
    this.cache.set(key, {
      data,
      expiresAt: Date.now() + ttl,
    });
  }

  has(key: string): boolean {
    return this.get(key) !== null;
  }

  clear(): void {
    this.cache.clear();
  }

  size(): number {
    // Clean expired entries and return count
    const now = Date.now();
    for (const [key, entry] of this.cache.entries()) {
      if (now > entry.expiresAt) {
        this.cache.delete(key);
      }
    }
    return this.cache.size;
  }
}

// Cache instances with different TTLs
const searchCache = new TTLCache<SoloditResponse>(300); // 5 minutes
const findingCache = new TTLCache<Finding>(3600); // 1 hour
const metadataCache = new TTLCache<string[]>(86400); // 24 hours

// =============================================================================
// RATE LIMITING
// =============================================================================

let requestCount = 0;
let windowStart = Date.now();
const RATE_LIMIT = 20;
const RATE_WINDOW = 60000;

function checkRateLimit(): { ok: boolean; remaining: number; resetIn: number } {
  const now = Date.now();
  if (now - windowStart >= RATE_WINDOW) {
    requestCount = 0;
    windowStart = now;
  }
  const remaining = RATE_LIMIT - requestCount;
  const resetIn = Math.ceil((RATE_WINDOW - (now - windowStart)) / 1000);
  return { ok: remaining > 0, remaining, resetIn };
}

// =============================================================================
// TYPE DEFINITIONS
// =============================================================================

interface SoloditFilter {
  keywords?: string;
  impact?: string[];
  firms?: { value: string }[];
  tags?: { value: string }[];
  protocolCategory?: { value: string }[];
  languages?: { value: string }[];
  protocol?: string;
  qualityScore?: number;
  sortField?: string;
  sortDirection?: string;
}

interface ProtocolCategory {
  title: string;
}

interface ProtocolCategoryScore {
  protocols_protocolcategory: ProtocolCategory;
  score: number;
}

interface Finding {
  id: string;
  slug: string;
  title: string;
  content: string;
  summary: string;
  impact: string;
  quality_score: number;
  firm_name: string | null;
  protocol_name: string | null;
  source_link: string | null;
  github_link: string | null;
  pdf_link: string | null;
  finders_count: number;
  issues_issuetagscore: { tags_tag: { title: string } }[];
  issues_issue_finders: { wardens_warden: { handle: string } }[];
  auditfirms_auditfirm: { name: string; logo_square: string } | null;
  protocols_protocol: {
    name: string;
    protocols_protocolcategoryscore: ProtocolCategoryScore[];
  } | null;
}

interface SoloditResponse {
  findings: Finding[];
  metadata: {
    totalResults: number;
    currentPage: number;
    pageSize: number;
    totalPages: number;
  };
  rateLimit: {
    limit: number;
    remaining: number;
    reset: number;
  };
}

// =============================================================================
// API FUNCTIONS
// =============================================================================

function getApiKey(): string {
  const apiKey = process.env.CYFRIN_API_KEY;
  if (!apiKey) {
    throw new Error(
      "CYFRIN_API_KEY not set. Get your key from https://solodit.cyfrin.io (Profile > API Keys)"
    );
  }
  return apiKey;
}

async function searchFindings(
  filters: SoloditFilter,
  page: number,
  pageSize: number,
  useCache = true
): Promise<SoloditResponse> {
  const apiKey = getApiKey();

  // Generate cache key from request parameters
  const cacheKey = JSON.stringify({ filters, page, pageSize });
  
  // Check cache first
  if (useCache) {
    const cached = searchCache.get(cacheKey);
    if (cached) {
      return cached;
    }
  }

  const rateCheck = checkRateLimit();
  if (!rateCheck.ok) {
    throw new Error(
      `Rate limit exceeded. Try again in ${rateCheck.resetIn} seconds.`
    );
  }

  requestCount++;

  const response = await fetch(
    "https://solodit.cyfrin.io/api/v1/solodit/findings",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Cyfrin-API-Key": apiKey,
      },
      body: JSON.stringify({ page, pageSize, filters }),
    }
  );

  if (!response.ok) {
    const errorText = await response.text();
    if (response.status === 401) throw new Error("Invalid API key");
    if (response.status === 429) throw new Error("Server rate limit exceeded");
    throw new Error(`API error (${response.status}): ${errorText}`);
  }

  const result = (await response.json()) as SoloditResponse;
  
  // Cache the result
  searchCache.set(cacheKey, result);
  
  // Also cache individual findings
  for (const finding of result.findings) {
    findingCache.set(`id:${finding.id}`, finding);
    if (finding.slug) {
      findingCache.set(`slug:${finding.slug}`, finding);
    }
  }

  return result;
}

async function getFindingById(idOrSlug: string): Promise<Finding | null> {
  // Check cache first
  let cached = findingCache.get(`id:${idOrSlug}`);
  if (cached) return cached;
  
  cached = findingCache.get(`slug:${idOrSlug}`);
  if (cached) return cached;

  // Search by keywords (ID or title fragment)
  const response = await searchFindings(
    { keywords: idOrSlug },
    1,
    20,
    false
  );

  // Try to find exact match
  for (const finding of response.findings) {
    if (finding.id === idOrSlug || finding.slug === idOrSlug) {
      return finding;
    }
  }

  // Return first result if any
  return response.findings[0] || null;
}

// =============================================================================
// METADATA EXTRACTION
// =============================================================================

// Known languages (from Solodit documentation)
const KNOWN_LANGUAGES = [
  "Solidity",
  "Rust",
  "Cairo",
  "Vyper",
  "Move",
  "Huff",
  "Fe",
  "Ink!",
];

// Known protocol categories (comprehensive list from API exploration)
const KNOWN_CATEGORIES = [
  "DeFi",
  "NFT",
  "NFT Marketplace",
  "Lending",
  "DEX",
  "Staking",
  "Staking Pool",
  "Governance",
  "Bridge",
  "Yield Aggregator",
  "Options",
  "Options Vault",
  "Oracles",
  "Gaming",
  "Liquid Staking",
  "RWA",
  "NFT Lending",
  "Perpetuals",
  "Insurance",
  "Launchpad",
  "DAO",
  "Wallet",
  "Identity",
  "Privacy",
  "Cross-Chain",
  "Layer 2",
  "Restaking",
];

async function fetchMetadata(type: "firms" | "tags"): Promise<string[]> {
  const cacheKey = `metadata:${type}`;
  const cached = metadataCache.get(cacheKey);
  if (cached) return cached;

  // Fetch a large sample to extract unique values
  const uniqueValues = new Set<string>();
  
  // Make multiple requests to gather comprehensive data
  const impactLevels = ["HIGH", "MEDIUM", "LOW"];
  
  for (const impact of impactLevels) {
    try {
      const response = await searchFindings(
        { impact: [impact] },
        1,
        100,
        true
      );
      
      for (const finding of response.findings) {
        if (type === "firms" && finding.firm_name) {
          uniqueValues.add(finding.firm_name);
        }
        if (type === "tags") {
          for (const tagScore of finding.issues_issuetagscore) {
            if (tagScore.tags_tag?.title) {
              uniqueValues.add(tagScore.tags_tag.title);
            }
          }
        }
      }
    } catch {
      // Continue on error
    }
  }

  const result = Array.from(uniqueValues).sort();
  metadataCache.set(cacheKey, result, 86400); // 24 hour cache
  return result;
}

// =============================================================================
// FORMATTING
// =============================================================================

function formatFinding(f: Finding, verbose = false): string {
  const tags =
    f.issues_issuetagscore.map((t) => t.tags_tag.title).join(", ") || "None";
  const finders =
    f.issues_issue_finders.map((x) => x.wardens_warden.handle).join(", ") ||
    "Unknown";
  const source = f.source_link || f.github_link || f.pdf_link || "N/A";
  const categories = f.protocols_protocol?.protocols_protocolcategoryscore
    ?.map((c) => c.protocols_protocolcategory.title)
    .join(", ") || "Unknown";

  const header = `## [${f.impact}] ${f.title}

**ID:** ${f.id}
**Slug:** ${f.slug || "N/A"}
**Audit Firm:** ${f.firm_name || "Unknown"}
**Protocol:** ${f.protocol_name || "Unknown"}
**Categories:** ${categories}
**Quality:** ${f.quality_score}/5
**Tags:** ${tags}
**Finders:** ${finders} (${f.finders_count} total)
**Source:** ${source}`;

  if (verbose) {
    return `${header}

### Summary
${f.summary || "No summary available."}

### Full Content
${f.content}

---`;
  }

  return `${header}

${f.content}

---`;
}

function formatFindingCompact(f: Finding): string {
  return `- **[${f.impact}]** ${f.title} (ID: ${f.id}, Firm: ${f.firm_name || "Unknown"}, Quality: ${f.quality_score}/5)`;
}

// =============================================================================
// MCP SERVER SETUP
// =============================================================================

const server = new Server(
  { name: "solodit-api", version: "2.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "search_vulnerabilities",
      description:
        "Search 50,000+ smart contract vulnerabilities from Cyfrin Solodit. Filter by severity, audit firm, tags, protocol, and more. Results are cached for 5 minutes.",
      inputSchema: {
        type: "object" as const,
        properties: {
          keywords: {
            type: "string",
            description: "Search terms (e.g., 'reentrancy', 'oracle')",
          },
          impact: {
            type: "array",
            items: { type: "string", enum: ["HIGH", "MEDIUM", "LOW", "GAS"] },
            description: "Severity filter",
          },
          audit_firms: {
            type: "array",
            items: { type: "string" },
            description: "Filter by audit firms (e.g., ['Cyfrin', 'Sherlock'])",
          },
          tags: {
            type: "array",
            items: { type: "string" },
            description: "Vulnerability tags (e.g., ['Reentrancy', 'Oracle'])",
          },
          protocol_categories: {
            type: "array",
            items: { type: "string" },
            description: "Protocol categories (e.g., ['DeFi', 'NFT'])",
          },
          languages: {
            type: "array",
            items: { type: "string" },
            description: "Languages (e.g., ['Solidity', 'Rust'])",
          },
          protocol: {
            type: "string",
            description: "Protocol name (partial match)",
          },
          min_quality: {
            type: "number",
            description: "Minimum quality score (1-5)",
          },
          sort: {
            type: "string",
            enum: ["recency", "quality", "rarity"],
            description: "Sort order",
          },
          page: { type: "number", description: "Page number (default: 1)" },
          page_size: {
            type: "number",
            description: "Results per page (max 100, default: 20)",
          },
        },
      },
    },
    {
      name: "get_finding",
      description:
        "Get a specific vulnerability finding by its ID or slug. Returns the full finding details including content, summary, and metadata. Results are cached for 1 hour.",
      inputSchema: {
        type: "object" as const,
        properties: {
          id: {
            type: "string",
            description: "Finding ID (numeric) or slug (URL-friendly identifier)",
          },
          verbose: {
            type: "boolean",
            description: "Include full content and summary (default: true)",
          },
        },
        required: ["id"],
      },
    },
    {
      name: "list_audit_firms",
      description:
        "List all available audit firms in the Solodit database. Results are cached for 24 hours. Use these firm names with the audit_firms filter in search_vulnerabilities.",
      inputSchema: {
        type: "object" as const,
        properties: {
          refresh: {
            type: "boolean",
            description: "Force refresh the cached list (default: false)",
          },
        },
      },
    },
    {
      name: "list_tags",
      description:
        "List all available vulnerability tags in the Solodit database. Results are cached for 24 hours. Use these tags with the tags filter in search_vulnerabilities.",
      inputSchema: {
        type: "object" as const,
        properties: {
          refresh: {
            type: "boolean",
            description: "Force refresh the cached list (default: false)",
          },
        },
      },
    },
    {
      name: "list_protocol_categories",
      description:
        "List all available protocol categories (DeFi, NFT, Lending, etc.). Use these with the protocol_categories filter in search_vulnerabilities.",
      inputSchema: {
        type: "object" as const,
        properties: {},
      },
    },
    {
      name: "list_languages",
      description:
        "List all supported programming languages (Solidity, Rust, Cairo, etc.). Use these with the languages filter in search_vulnerabilities.",
      inputSchema: {
        type: "object" as const,
        properties: {},
      },
    },
    {
      name: "get_statistics",
      description:
        "Get statistics about the Solodit vulnerability database including total findings count and cache status.",
      inputSchema: {
        type: "object" as const,
        properties: {},
      },
    },
    {
      name: "clear_cache",
      description:
        "Clear all cached data. Use this if you need fresh data or to free memory.",
      inputSchema: {
        type: "object" as const,
        properties: {
          type: {
            type: "string",
            enum: ["all", "search", "findings", "metadata"],
            description: "Type of cache to clear (default: all)",
          },
        },
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name } = request.params;
  const args = request.params.arguments as Record<string, unknown>;

  try {
    switch (name) {
      case "search_vulnerabilities": {
        const filters: SoloditFilter = {};

        if (args.keywords) filters.keywords = String(args.keywords);
        if (args.impact) filters.impact = args.impact as string[];
        if (args.audit_firms)
          filters.firms = (args.audit_firms as string[]).map((v) => ({ value: v }));
        if (args.tags)
          filters.tags = (args.tags as string[]).map((v) => ({ value: v }));
        if (args.protocol_categories)
          filters.protocolCategory = (args.protocol_categories as string[]).map(
            (v) => ({ value: v })
          );
        if (args.languages)
          filters.languages = (args.languages as string[]).map((v) => ({
            value: v,
          }));
        if (args.protocol) filters.protocol = String(args.protocol);
        if (args.min_quality) filters.qualityScore = Number(args.min_quality);

        if (args.sort) {
          const sortMap: Record<string, string> = {
            recency: "Recency",
            quality: "Quality",
            rarity: "Rarity",
          };
          filters.sortField = sortMap[String(args.sort)] || "Recency";
          filters.sortDirection = "Desc";
        }

        const page = Number(args.page) || 1;
        const pageSize = Math.min(Number(args.page_size) || 20, 100);

        const response = await searchFindings(filters, page, pageSize);

        const rateCheck = checkRateLimit();
        const rateWarning =
          rateCheck.remaining <= 5
            ? `\n**Rate Limit Warning:** ${rateCheck.remaining} requests remaining.\n`
            : "";

        const cacheStatus = searchCache.size() > 0 ? "(from cache)" : "(fresh)";

        const header = `# Solodit Search Results ${cacheStatus}

**Query:** ${args.keywords || "All vulnerabilities"}
**Filters:** Impact: ${(args.impact as string[])?.join(", ") || "All"} | Firms: ${(args.audit_firms as string[])?.join(", ") || "All"}
**Results:** ${response.metadata.totalResults} total (Page ${response.metadata.currentPage}/${response.metadata.totalPages})
**Rate Limit:** ${response.rateLimit.remaining}/${response.rateLimit.limit} remaining
${rateWarning}
---

`;

        if (response.findings.length === 0) {
          return {
            content: [
              {
                type: "text",
                text: header + "No vulnerabilities found. Try adjusting filters.",
              },
            ],
          };
        }

        const findings = response.findings.map((f) => formatFinding(f)).join("\n\n");
        return { content: [{ type: "text", text: header + findings }] };
      }

      case "get_finding": {
        const idOrSlug = String(args.id);
        const verbose = args.verbose !== false;

        const finding = await getFindingById(idOrSlug);

        if (!finding) {
          return {
            content: [
              {
                type: "text",
                text: `**Error:** Finding not found: ${idOrSlug}\n\nTry searching with keywords instead.`,
              },
            ],
          };
        }

        const result = formatFinding(finding, verbose);
        return { content: [{ type: "text", text: result }] };
      }

      case "list_audit_firms": {
        const refresh = args.refresh === true;
        
        if (refresh) {
          metadataCache.clear();
        }

        const firms = await fetchMetadata("firms");
        
        // Also include well-known firms that might not appear in sample
        const knownFirms = [
          "Cyfrin",
          "Sherlock",
          "Code4rena",
          "Trail of Bits",
          "OpenZeppelin",
          "Consensys Diligence",
          "Spearbit",
          "Pashov Audit Group",
          "Hacken",
          "ChainSecurity",
          "Halborn",
          "Certik",
          "Quantstamp",
          "Sigma Prime",
          "yAudit",
          "Guardian Audits",
          "Shieldify",
        ];
        
        const allFirms = Array.from(new Set([...firms, ...knownFirms])).sort();

        return {
          content: [
            {
              type: "text",
              text: `# Audit Firms (${allFirms.length} total)

Use these firm names with the \`audit_firms\` filter in \`search_vulnerabilities\`.

${allFirms.map((f) => `- ${f}`).join("\n")}

**Note:** This list is cached for 24 hours. Use \`refresh: true\` to update.`,
            },
          ],
        };
      }

      case "list_tags": {
        const refresh = args.refresh === true;
        
        if (refresh) {
          metadataCache.clear();
        }

        const tags = await fetchMetadata("tags");
        
        // Include commonly used tags
        const knownTags = [
          "Reentrancy",
          "Oracle",
          "Access Control",
          "Integer Overflow/Underflow",
          "Front-running",
          "Price Manipulation",
          "Flash Loan",
          "Griefing",
          "DOS",
          "Logic Error",
          "Signature",
          "Delegation",
          "ERC20",
          "ERC721",
          "ERC4626",
          "Chainlink",
          "Uniswap",
          "AAVE",
          "Compound",
        ];
        
        const allTags = Array.from(new Set([...tags, ...knownTags])).sort();

        return {
          content: [
            {
              type: "text",
              text: `# Vulnerability Tags (${allTags.length} total)

Use these tags with the \`tags\` filter in \`search_vulnerabilities\`.

${allTags.map((t) => `- ${t}`).join("\n")}

**Note:** This list is cached for 24 hours. Use \`refresh: true\` to update.`,
            },
          ],
        };
      }

      case "list_protocol_categories": {
        return {
          content: [
            {
              type: "text",
              text: `# Protocol Categories (${KNOWN_CATEGORIES.length} total)

Use these categories with the \`protocol_categories\` filter in \`search_vulnerabilities\`.

${KNOWN_CATEGORIES.map((c) => `- ${c}`).join("\n")}`,
            },
          ],
        };
      }

      case "list_languages": {
        return {
          content: [
            {
              type: "text",
              text: `# Supported Languages (${KNOWN_LANGUAGES.length} total)

Use these languages with the \`languages\` filter in \`search_vulnerabilities\`.

${KNOWN_LANGUAGES.map((l) => `- ${l}`).join("\n")}`,
            },
          ],
        };
      }

      case "get_statistics": {
        // Get total count from API
        const response = await searchFindings({}, 1, 1);
        
        const rateCheck = checkRateLimit();

        return {
          content: [
            {
              type: "text",
              text: `# Solodit Database Statistics

**Total Findings:** ${response.metadata.totalResults.toLocaleString()}

## Cache Status
- **Search Cache:** ${searchCache.size()} entries (5 min TTL)
- **Finding Cache:** ${findingCache.size()} entries (1 hour TTL)  
- **Metadata Cache:** ${metadataCache.size()} entries (24 hour TTL)

## Rate Limit
- **Remaining:** ${rateCheck.remaining}/${RATE_LIMIT} requests
- **Resets in:** ${rateCheck.resetIn} seconds

## Server Info
- **Version:** 2.0.0
- **API Endpoint:** https://solodit.cyfrin.io/api/v1/solodit/findings`,
            },
          ],
        };
      }

      case "clear_cache": {
        const cacheType = String(args.type || "all");
        
        let cleared = [];
        
        if (cacheType === "all" || cacheType === "search") {
          searchCache.clear();
          cleared.push("search");
        }
        if (cacheType === "all" || cacheType === "findings") {
          findingCache.clear();
          cleared.push("findings");
        }
        if (cacheType === "all" || cacheType === "metadata") {
          metadataCache.clear();
          cleared.push("metadata");
        }

        return {
          content: [
            {
              type: "text",
              text: `**Cache cleared:** ${cleared.join(", ")}\n\nNext requests will fetch fresh data from the API.`,
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const msg = error instanceof Error ? error.message : String(error);
    return {
      content: [{ type: "text", text: `**Error:** ${msg}` }],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Solodit MCP server v2.0.0 running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});

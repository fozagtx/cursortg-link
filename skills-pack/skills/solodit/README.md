# Solodit API Skill

[![npm version](https://img.shields.io/npm/v/solodit-api-skill.svg)](https://www.npmjs.com/package/solodit-api-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **The largest smart contract vulnerability database at your fingertips.**

Search and analyze 50,000+ security findings from [Cyfrin Solodit](https://solodit.cyfrin.io) directly within your AI coding assistant. Built as an MCP (Model Context Protocol) server for seamless integration with Claude, OpenCode, and other AI tools.

## Features

- **50,000+ Vulnerabilities** - Access the world's largest database of blockchain security findings
- **8 MCP Tools** - Comprehensive API for searching, filtering, and analyzing vulnerabilities
- **Smart Caching** - Reduce API calls with intelligent TTL-based caching
- **Rate Limit Aware** - Automatic tracking and warnings for API rate limits
- **Multi-Language** - Supports Solidity, Rust, Cairo, Vyper, Move, and more
- **Full Content** - Get complete markdown reports with code examples and remediations

## Quick Install

### For Claude Code / OpenCode

```bash
npx skills add BowTiedSwan/solodit-api-skill
```

### Manual Installation

```bash
curl -fsSL https://raw.githubusercontent.com/BowTiedSwan/solodit-api-skill/main/install.sh | bash
```

## Prerequisites

### 1. Get Your API Key

1. Create an account at [solodit.cyfrin.io](https://solodit.cyfrin.io)
2. Click your profile dropdown in the top right corner
3. Open "API Keys" modal and generate a new key

### 2. Set Environment Variable

```bash
export CYFRIN_API_KEY="sk_your_api_key_here"
```

Add to your shell profile (`~/.bashrc`, `~/.zshrc`) for persistence.

## MCP Tools Reference

### search_vulnerabilities

Search and filter security findings from the Solodit database.

| Parameter | Type | Description |
|-----------|------|-------------|
| `keywords` | string | Search terms (e.g., "reentrancy", "oracle manipulation") |
| `impact` | string[] | Severity filter: `["HIGH"]`, `["HIGH", "MEDIUM"]`, etc. |
| `audit_firms` | string[] | Filter by auditor: `["Cyfrin", "Sherlock"]` |
| `tags` | string[] | Vulnerability tags: `["Reentrancy", "Oracle", "Access Control"]` |
| `protocol_categories` | string[] | Protocol types: `["DeFi", "NFT", "Lending"]` |
| `languages` | string[] | Programming language: `["Solidity", "Rust", "Cairo"]` |
| `protocol` | string | Protocol name (partial match) |
| `min_quality` | number | Minimum quality score (1-5) |
| `sort` | string | Sort by: `"recency"`, `"quality"`, `"rarity"` |
| `page` | number | Page number (default: 1) |
| `page_size` | number | Results per page (max: 100, default: 20) |

**Example:**
```
Search for high-severity reentrancy vulnerabilities from Cyfrin audits
```

### get_finding

Retrieve a specific vulnerability by ID or slug.

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Finding ID (numeric) or slug (URL-friendly identifier) |
| `verbose` | boolean | Include full content and summary (default: true) |

**Example:**
```
Get finding with ID 64691
```

### list_audit_firms

List all available audit firms in the database.

| Parameter | Type | Description |
|-----------|------|-------------|
| `refresh` | boolean | Force refresh the cached list (default: false) |

**Returns:** List of 50+ audit firms including Cyfrin, Sherlock, Code4rena, Trail of Bits, OpenZeppelin, and more.

### list_tags

List all available vulnerability tags.

| Parameter | Type | Description |
|-----------|------|-------------|
| `refresh` | boolean | Force refresh the cached list (default: false) |

**Returns:** Comprehensive list of tags like Reentrancy, Oracle, Access Control, Flash Loan, etc.

### list_protocol_categories

List all protocol categories (DeFi, NFT, Lending, DEX, Bridge, etc.).

### list_languages

List all supported programming languages (Solidity, Rust, Cairo, Vyper, Move, Huff, Fe, Ink!).

### get_statistics

Get database statistics and cache status.

**Returns:**
- Total findings count
- Cache status (entries and TTL for each cache type)
- Rate limit remaining
- Server version

### clear_cache

Clear cached data to fetch fresh results.

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Cache type: `"all"`, `"search"`, `"findings"`, `"metadata"` |

## Caching Strategy

The MCP server implements intelligent caching to reduce API calls:

| Cache Type | TTL | Purpose |
|------------|-----|---------|
| **Search Results** | 5 minutes | Recent search queries |
| **Individual Findings** | 1 hour | Findings retrieved by ID/slug |
| **Metadata** | 24 hours | Audit firms, tags lists |

Use `clear_cache` to force fresh data when needed.

## Usage Examples

### With AI Agents

```
Search for high-severity reentrancy vulnerabilities from Cyfrin audits
```

```
Find oracle manipulation issues in DeFi protocols with quality score 4 or higher
```

```
Show me flash loan attack examples sorted by rarity
```

```
List all audit firms available in the database
```

```
Get the finding with ID 64691
```

```
What are the database statistics?
```

### Direct API (curl)

```bash
# Basic search
curl -X POST https://solodit.cyfrin.io/api/v1/solodit/findings \
  -H "Content-Type: application/json" \
  -H "X-Cyfrin-API-Key: $CYFRIN_API_KEY" \
  -d '{
    "page": 1,
    "pageSize": 20,
    "filters": {
      "keywords": "reentrancy",
      "impact": ["HIGH", "MEDIUM"],
      "sortField": "Quality",
      "sortDirection": "Desc"
    }
  }'

# Filter by audit firm
curl -X POST https://solodit.cyfrin.io/api/v1/solodit/findings \
  -H "Content-Type: application/json" \
  -H "X-Cyfrin-API-Key: $CYFRIN_API_KEY" \
  -d '{
    "page": 1,
    "pageSize": 20,
    "filters": {
      "firms": [{"value": "Cyfrin"}, {"value": "Sherlock"}],
      "impact": ["HIGH"]
    }
  }'
```

## Rate Limits

- **Limit:** 20 requests per 60-second window
- **Tracking:** The MCP server automatically tracks rate limits
- **Warnings:** Alerts when approaching the threshold (≤5 remaining)
- **Caching:** Reduces API calls significantly

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent (Claude/OpenCode)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Solodit MCP Server v2.0                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   8 Tools   │  │  TTL Cache  │  │  Rate Limit Tracker │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Cyfrin Solodit API (50,000+ findings)           │
└─────────────────────────────────────────────────────────────┘
```

## Common Tags

- Reentrancy
- Oracle
- Access Control
- Integer Overflow/Underflow
- Front-running
- Price Manipulation
- Flash Loan
- Griefing
- DOS
- Logic Error

## Common Audit Firms

- Cyfrin
- Sherlock
- Code4rena
- Trail of Bits
- OpenZeppelin
- Consensys Diligence
- Spearbit
- Pashov Audit Group
- Hacken
- ChainSecurity

## Protocol Categories

- DeFi
- NFT / NFT Marketplace
- Lending / NFT Lending
- DEX
- Staking / Liquid Staking
- Governance / DAO
- Bridge / Cross-Chain
- Yield Aggregator
- Options / Options Vault
- Oracles
- Gaming
- RWA (Real World Assets)

## Development

### Build from Source

```bash
git clone https://github.com/BowTiedSwan/solodit-api-skill.git
cd solodit-api-skill
npm install
npm run build
```

### Run Locally

```bash
export CYFRIN_API_KEY="sk_your_key"
npm start
```

## Changelog

### v2.0.0
- Added 7 new MCP tools (get_finding, list_audit_firms, list_tags, list_protocol_categories, list_languages, get_statistics, clear_cache)
- Implemented intelligent TTL-based caching (5min/1hr/24hr)
- Enhanced rate limit tracking with warnings
- Improved error handling and response formatting

### v1.0.0
- Initial release with search_vulnerabilities tool
- Basic rate limiting
- Markdown-formatted results

## Links

- [Solodit Platform](https://solodit.cyfrin.io)
- [API Documentation](https://cyfrin.notion.site/Cyfrin-Solodit-Findings-API-Specification)
- [Cyfrin Security](https://cyfrin.io)
- [Landing Page](https://BowTiedSwan.github.io/solodit-api-skill/)

## License

MIT

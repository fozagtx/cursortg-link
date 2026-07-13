---
id: seo
title: GEO + SEO pass
summary: AI-search citability + technical SEO foundations
---

# Cloud Agent Playbook — GEO / SEO

## Before changing content
Read `.cursor/skills/geo/SKILL.md` and the synced `geo-*` skills. GEO-first, SEO-supported.

## Rules
- Optimize for AI citation (ChatGPT/Perplexity/Gemini/AI Overviews), not keyword stuffing.
- Prefer quotable claims with real entity names from the repo — invent nothing.
- Fix title/meta/OG, JSON-LD, llms.txt/robots, sitemap as needed.
- Keep visual design intact unless structure requires layout tweaks.

## Done when
PR lists pages touched, schema/meta/crawler changes, and citability notes.

## Synced skills this playbook expects

Before launching the Cloud Agent, run:

```bash
./scripts/sync-skills-to-repo.sh /path/to/target-repo --playbook seo
```

Then commit `.cursor/` in the target repo.

- `.cursor/skills/geo/SKILL.md`
- `.cursor/skills/geo-audit/SKILL.md`
- `.cursor/skills/geo-citability/SKILL.md`
- `.cursor/skills/geo-technical/SKILL.md`
- `.cursor/skills/geo-schema/SKILL.md`
- `.cursor/skills/geo-llmstxt/SKILL.md`
- `.cursor/skills/geo-content/SKILL.md`
- `.cursor/skills/geo-crawlers/SKILL.md`
- `.cursor/skills/geo-brand-mentions/SKILL.md`
- `.cursor/skills/geo-platform-optimizer/SKILL.md`
- `.cursor/skills/geo-report/SKILL.md`
- `.cursor/skills/landing-page-rewrite/SKILL.md`

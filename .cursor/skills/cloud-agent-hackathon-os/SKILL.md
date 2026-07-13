---
name: cloud-agent-hackathon-os
description: >-
  Lead Cursor Cloud Agents launched from Telegram through playbook-mapped
  hackathon workflows. Use for /newagent playbooks (ui, seo, ship, hackathon,
  fullstack, solana, pitch, security), skills-pack sync, and efficient Cloud
  Agent launches. Read skills-catalog/CATALOG.md so nothing is forgotten.
---

# Cloud Agent Hackathon OS

## Decided policy

1. This repo is a **sync pack for hackathon target repos** (not for bloating itself).
2. Sync is **playbook-mapped only** — never dump all ~137 skills into a project.
3. **Commit** synced `.cursor/skills/` in the target repo (Cloud Agents clone clean).
4. Full inventory lives in `skills-catalog/` so nothing is forgotten; archived skills stay indexed.

## Launch loop

```bash
# 1) Sync only what this agent needs
./scripts/sync-skills-to-repo.sh /path/to/hackathon-repo --playbook ui
# or combine: --playbook solana,ui

# 2) Commit .cursor/ in the target repo

# 3) Telegram: /newagent → model → repo → branch → same playbook → short prompt
```

## Playbooks

| id | When |
|----|------|
| `ui` | Landing, dashboard, components, polish |
| `seo` | GEO/SEO, llms.txt, schema, citability |
| `ship` | Demo-critical vertical slice |
| `hackathon` | Sprint + submission + social |
| `fullstack` | One API+UI feature |
| `solana` | Solana program/app path |
| `pitch` | Deck / video / ads |
| `security` | Pre-demo review |
| `none` | Raw prompt |

## Prompt shape

```
Outcome: <wow moment in one sentence>
Constraints: <stack / files not to touch>
Done when: <demo steps>
```

One agent = one outcome. Split UI vs SEO vs pitch into separate agents + `/threadmode on`.

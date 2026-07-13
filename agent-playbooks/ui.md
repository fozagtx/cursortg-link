---
id: ui
title: Premium UI build
summary: Polished React/Next UI with design-promax + craft rules
---

# Cloud Agent Playbook — Premium UI

You are shipping production UI for a hackathon/demo.

## Before coding
1. Sync was supposed to put these under `.cursor/skills/` — read them.
2. For React UI: start with `design-promax/SKILL.md`, then read real files under `design-promax/sources/` for the pattern. Never invent HeroUI patterns.
3. Apply `frontend-design-guidelines` + `design-taste` / `gpt-taste` to kill generic AI slop.

## Rules
- One composition for the first viewport; brand is a hero-level signal.
- Expressive fonts; avoid Inter/Roboto/Arial/system defaults.
- Avoid purple-on-white / cream+terracotta / broadsheet AI-slop clusters unless brand requires it.
- 2–3 intentional motions max. Mobile + desktop both work.
- Diffs stay focused on requested screens.

## Done when
Requested UI runs, responsive, PR has preview steps.

## Synced skills this playbook expects

Before launching the Cloud Agent, run:

```bash
./scripts/sync-skills-to-repo.sh /path/to/target-repo --playbook ui
```

Then commit `.cursor/` in the target repo.

- `.cursor/skills/design-promax/SKILL.md`
- `.cursor/skills/frontend-design/SKILL.md`
- `.cursor/skills/frontend-design-guidelines/SKILL.md`
- `.cursor/skills/design-taste/SKILL.md`
- `.cursor/skills/design-taste-frontend/SKILL.md`
- `.cursor/skills/gpt-taste/SKILL.md`
- `.cursor/skills/high-end-visual-design/SKILL.md`
- `.cursor/skills/page-load-animations/SKILL.md`
- `.cursor/skills/web-animation-guidelines/SKILL.md`
- `.cursor/skills/number-formatting/SKILL.md`
- `.cursor/skills/transitions-dev/SKILL.md`
- `.cursor/skills/landing-page-rewrite/SKILL.md`
- `.cursor/skills/brand-design/SKILL.md`
- `.cursor/skills/redesign-existing-projects/SKILL.md`
- `.cursor/skills/minimalist-ui/SKILL.md`
- `.cursor/skills/stitch-design-taste/SKILL.md`

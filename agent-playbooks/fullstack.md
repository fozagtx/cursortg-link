---
id: fullstack
title: Fullstack feature
summary: API + UI + persistence for one feature
---

# Cloud Agent Playbook — Fullstack Feature

Match existing routes/services/DB/UI patterns. One feature, backend + frontend together.
Validate inputs; clear errors; minimal tests; update README only for new env/run steps.
Use design-promax when building React surfaces.

## Synced skills this playbook expects

Before launching the Cloud Agent, run:

```bash
./scripts/sync-skills-to-repo.sh /path/to/target-repo --playbook fullstack
```

Then commit `.cursor/` in the target repo.

- `.cursor/skills/design-promax/SKILL.md`
- `.cursor/skills/frontend-design-guidelines/SKILL.md`
- `.cursor/skills/design-taste/SKILL.md`
- `.cursor/skills/page-load-animations/SKILL.md`
- `.cursor/skills/number-formatting/SKILL.md`
- `.cursor/skills/diagnose/SKILL.md`
- `.cursor/skills/tdd/SKILL.md`
- `.cursor/skills/vibe-security/SKILL.md`
- `.cursor/skills/webapp-testing/SKILL.md`
- `.cursor/skills/prototype/SKILL.md`

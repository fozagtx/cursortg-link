---
id: ship
title: Ship-ready slice
summary: Tracer-bullet vertical slice — build, test, PR, demo
---

# Cloud Agent Playbook — Ship

## Goal
One end-to-end path: user action → system change → visible result.

## Rules
1. Read AGENTS.md / README / scripts first.
2. Smallest change that demos the path.
3. No unrelated refactors.
4. Minimal tests; run existing lint/test/build; fix what you break.
5. PR includes a 3–7 step demo script.

## Done when
Demo path works with documented steps.

## Synced skills this playbook expects

Before launching the Cloud Agent, run:

```bash
./scripts/sync-skills-to-repo.sh /path/to/target-repo --playbook ship
```

Then commit `.cursor/` in the target repo.

- `.cursor/skills/diagnose/SKILL.md`
- `.cursor/skills/tdd/SKILL.md`
- `.cursor/skills/review-and-iterate/SKILL.md`
- `.cursor/skills/vibe-security/SKILL.md`
- `.cursor/skills/webapp-testing/SKILL.md`
- `.cursor/skills/handoff/SKILL.md`
- `.cursor/skills/prototype/SKILL.md`
- `.cursor/skills/zoom-out/SKILL.md`

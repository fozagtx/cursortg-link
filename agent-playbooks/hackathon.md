---
id: hackathon
title: Hackathon sprint
summary: MVP → polish → submission → social in one pass
---

# Cloud Agent Playbook — Hackathon Sprint

## Phase order
1. Clarify slice (who / problem / wow) in one sentence.
2. Tracer-bullet build for the wow moment.
3. Polish demo UI if needed (prefer a separate `ui` agent if scope is large).
4. Submission pack via `submit-to-hackathon`.
5. Social seed via `hackathon-project-social-playbook` (do not auto-post).

## Hard constraints
Working demo > incomplete ambition. Secrets stay out of git.

## PR must include
What ships · how to demo · what was cut · judge one-liner.

## Synced skills this playbook expects

Before launching the Cloud Agent, run:

```bash
./scripts/sync-skills-to-repo.sh /path/to/target-repo --playbook hackathon
```

Then commit `.cursor/` in the target repo.

- `.cursor/skills/submit-to-hackathon/SKILL.md`
- `.cursor/skills/hackathon-project-social-playbook/SKILL.md`
- `.cursor/skills/bpfg-hackathon/SKILL.md`
- `.cursor/skills/create-pitch-deck/SKILL.md`
- `.cursor/skills/competitive-landscape/SKILL.md`
- `.cursor/skills/roast-my-product/SKILL.md`
- `.cursor/skills/product-review/SKILL.md`
- `.cursor/skills/validate-idea/SKILL.md`
- `.cursor/skills/scaffold-project/SKILL.md`
- `.cursor/skills/build-with-claude/SKILL.md`
- `.cursor/skills/colosseum-copilot/SKILL.md`
- `.cursor/skills/apply-grant/SKILL.md`

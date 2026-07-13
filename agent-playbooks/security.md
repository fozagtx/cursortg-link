---
id: security
title: Security pass
summary: Threat model, audit, and review before demo
---

# Cloud Agent Playbook — Security Pass

Threat-model and review before demo. Use `vibe-security` / `cso` / `x-ray` (and Solidity tools only if the repo has Solidity).
Report findings with severity + fix PRs for the critical path only.

## Synced skills this playbook expects

Before launching the Cloud Agent, run:

```bash
./scripts/sync-skills-to-repo.sh /path/to/target-repo --playbook security
```

Then commit `.cursor/` in the target repo.

- `.cursor/skills/vibe-security/SKILL.md`
- `.cursor/skills/cso/SKILL.md`
- `.cursor/skills/x-ray/SKILL.md`
- `.cursor/skills/solidity-auditor/SKILL.md`
- `.cursor/skills/solodit/SKILL.md`
- `.cursor/skills/review-and-iterate/SKILL.md`

---
id: solana
title: Solana build
summary: Scaffold, program, debug, review, deploy for Solana hackathons
---

# Cloud Agent Playbook — Solana

## Order
1. Scaffold/match existing workspace patterns (`scaffold-project` / repo conventions).
2. Implement the program or client path needed for the demo.
3. Debug failing txs with `debug-program` patterns.
4. Review with `review-and-iterate` / `x-ray` before claiming ready.
5. Only touch mainnet deployment docs if explicitly asked (`deploy-to-mainnet`).

## Rules
Prefer known Anchor/SDK patterns in-repo. No blind mainnet deploys. Keep keys local.

## Synced skills this playbook expects

Before launching the Cloud Agent, run:

```bash
./scripts/sync-skills-to-repo.sh /path/to/target-repo --playbook solana
```

Then commit `.cursor/` in the target repo.

- `.cursor/skills/scaffold-project/SKILL.md`
- `.cursor/skills/build-defi-protocol/SKILL.md`
- `.cursor/skills/build-data-pipeline/SKILL.md`
- `.cursor/skills/debug-program/SKILL.md`
- `.cursor/skills/review-and-iterate/SKILL.md`
- `.cursor/skills/deploy-to-mainnet/SKILL.md`
- `.cursor/skills/solana-beginner/SKILL.md`
- `.cursor/skills/launch-token/SKILL.md`
- `.cursor/skills/x-ray/SKILL.md`
- `.cursor/skills/defillama-research/SKILL.md`
- `.cursor/skills/find-next-crypto-idea/SKILL.md`
- `.cursor/skills/virtual-solana-incubator/SKILL.md`
- `.cursor/skills/spyzer-memecoin-guide/SKILL.md`
- `.cursor/skills/build-mobile/SKILL.md`

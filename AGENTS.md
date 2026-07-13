# Agents

## Cursor Cloud specific instructions

### Overview

Python 3.12 async Telegram ↔ Cursor Cloud Agents bridge (`cursor-tg-connector`). Single process, SQLite via `aiosqlite`.

### Development commands

- **Install**: `source .venv/bin/activate && pip install -e ".[dev]"`
- **Lint**: `ruff check .`
- **Test**: `pytest`
- **Run**: `python -m cursor_tg_connector`

### Hackathon skills pack (decided)

| Decision | Choice |
|----------|--------|
| Purpose | Sync pack for **hackathon target repos** |
| Sync mode | **Playbook-mapped only** |
| Inventory | **137** skills catalogued in `skills-catalog/` (nothing forgotten) |
| Vendored | **68** skills in `skills-pack/skills/` (~6MB; geo slimmed) |
| Target repos | **Commit** synced `.cursor/skills/` so Cloud Agents see them |

```bash
./scripts/sync-skills-to-repo.sh --list
./scripts/sync-skills-to-repo.sh /path/to/hackathon-repo --playbook ui
./scripts/sync-skills-to-repo.sh /path/to/hackathon-repo --playbook solana,ship
./scripts/refresh-skills-pack.sh   # re-vendor from ~/.agents + ~/.claude
```

Telegram: `/newagent` → model → repo → branch → **playbook** → prompt  
Also: `/playbooks`, `/useplaybook <id>`

Playbook ids: `ui`, `seo`, `ship`, `hackathon`, `fullstack`, `solana`, `pitch`, `security`, `none`

### Non-obvious caveats

- Cursor API key is validated on startup (`GET /v0/me`).
- Do not commit `.env`.
- `pytest` uses `asyncio_mode = auto`; HTTP is mocked via `respx`.
- Cloud Agents only load skills from the **target** repo — sync + commit before launch.
- Full `geo` tree is ~176MB; pack vendors `SKILL.md` only for geo entrypoints.

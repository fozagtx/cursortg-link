#!/usr/bin/env bash
# Re-vendor playbook-mapped skills from ~/.agents/skills and ~/.claude/skills.
# Rebuilds skills-pack/ + skills-catalog/ from the playbook map in this script's Python.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 <<'PY'
from __future__ import annotations
import json, shutil
from pathlib import Path

ROOT = Path('.').resolve()
AGENT = Path.home() / '.agents' / 'skills'
CLAUDE = Path.home() / '.claude' / 'skills'
PACK = ROOT / 'skills-pack' / 'skills'
CATALOG = ROOT / 'skills-catalog'
PLAYBOOKS_PATH = ROOT / 'skills-pack' / 'playbooks.json'

if not PLAYBOOKS_PATH.exists():
    raise SystemExit('skills-pack/playbooks.json missing')

PLAYBOOKS = json.loads(PLAYBOOKS_PATH.read_text())
SLIM = {
    'geo': ['SKILL.md'],
    'geo-audit': ['SKILL.md'],
    'geo-report': ['SKILL.md'],
    'geo-report-pdf': ['SKILL.md'],
    'pptx': ['SKILL.md'],
}

def resolve_src(name: str) -> Path | None:
    for root in (AGENT, CLAUDE):
        p = root / name
        if p.is_dir():
            return p
    return None

def copy_skill(name: str, src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    if name == 'design-promax' and (src / 'skill').is_dir():
        shutil.copytree(src / 'skill', dest, ignore=shutil.ignore_patterns('.git', '__pycache__', 'node_modules'))
        for extra in ('commands', 'agents', 'rules'):
            if (src / extra).is_dir():
                shutil.copytree(src / extra, dest / extra, dirs_exist_ok=True)
        return
    if name in SLIM:
        dest.mkdir(parents=True)
        for rel in SLIM[name]:
            s = src / rel
            if s.exists():
                d = dest / rel
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(s, d)
        return
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns('.git', '__pycache__', 'node_modules', '.venv'))

all_skills = {}
for root in (AGENT, CLAUDE):
    if not root.exists():
        continue
    for p in sorted(root.iterdir()):
        if p.is_dir() and not p.name.startswith('.') and p.name not in all_skills:
            all_skills[p.name] = str(p)

playbooked = sorted({s for pb in PLAYBOOKS.values() for s in pb['skills']})
PACK.mkdir(parents=True, exist_ok=True)
# remove skills no longer mapped
for existing in list(PACK.iterdir()):
    if existing.is_dir() and existing.name not in playbooked:
        shutil.rmtree(existing)

modes = {}
for name in playbooked:
    src = resolve_src(name)
    if src is None:
        raise SystemExit(f'Missing skill source: {name}')
    copy_skill(name, src, PACK / name)
    modes[name] = 'ok'

membership = {name: [] for name in all_skills}
for pb, meta in PLAYBOOKS.items():
    for s in meta['skills']:
        membership.setdefault(s, []).append(pb)

manifest = {
    'version': 1,
    'policy': {
        'purpose': 'sync-pack-for-hackathon-target-repos',
        'sync_mode': 'playbook-mapped-only',
        'commit_skills_in_target_repo': True,
    },
    'totals': {
        'inventory': len(all_skills),
        'playbooked': len(playbooked),
        'archived': len(all_skills) - len(set(playbooked) & set(all_skills)),
    },
    'playbooks': PLAYBOOKS,
    'skills': {
        name: {
            'source': all_skills[name],
            'playbooks': membership.get(name, []),
            'status': 'playbooked' if name in playbooked else 'archived',
            'vendored': name in playbooked,
        }
        for name in sorted(all_skills)
    },
}
CATALOG.mkdir(parents=True, exist_ok=True)
(CATALOG / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

lines = [
    '# Skills catalog (nothing forgotten)',
    '',
    f"Inventory: **{len(all_skills)}** unique skills.",
    f"Playbooked: **{len(playbooked)}**.",
    f"Archived: **{len(all_skills) - len(set(playbooked))}**.",
    '',
    '## Playbooks → skills',
    '',
]
for pb, meta in PLAYBOOKS.items():
    lines.append(f"### `{pb}` — {meta['title']}")
    lines.append(meta['summary'])
    lines.append('')
    for s in meta['skills'] or ['_none_']:
        lines.append(f'- `{s}`' if s != '_none_' else '_No skills synced._')
    lines.append('')
lines += ['## Archived', '']
for name, meta in sorted(manifest['skills'].items()):
    if meta['status'] == 'archived':
        lines.append(f'- `{name}`')
lines.append('')
(CATALOG / 'CATALOG.md').write_text('\n'.join(lines) + '\n')
print(f'Refreshed {len(playbooked)} playbooked skills; catalogued {len(all_skills)} total.')
PY

chmod +x "$ROOT/scripts/sync-skills-to-repo.sh" "$ROOT/scripts/refresh-skills-pack.sh"
du -sh skills-pack skills-catalog

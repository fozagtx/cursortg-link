#!/usr/bin/env bash
# Sync playbook-mapped skills into a hackathon target repo for Cursor Cloud Agents.
# Usage:
#   ./scripts/sync-skills-to-repo.sh /path/to/hackathon-repo --playbook ui
#   ./scripts/sync-skills-to-repo.sh /path/to/hackathon-repo --playbook hackathon,seo
#   ./scripts/sync-skills-to-repo.sh /path/to/hackathon-repo --list
set -euo pipefail

SRC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLAYBOOKS_JSON="$SRC_ROOT/skills-pack/playbooks.json"
SKILLS_DIR="$SRC_ROOT/skills-pack/skills"

TARGET=""
PLAYBOOK_ARGS=""
LIST_ONLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --playbook|-p)
      PLAYBOOK_ARGS="${2:-}"
      shift 2
      ;;
    --list|-l)
      LIST_ONLY=1
      shift
      ;;
    -h|--help)
      sed -n '2,7p' "$0"
      exit 0
      ;;
    *)
      if [[ -z "$TARGET" ]]; then
        TARGET="$1"
      else
        echo "Unexpected arg: $1" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ ! -f "$PLAYBOOKS_JSON" ]]; then
  echo "Missing $PLAYBOOKS_JSON — run ./scripts/refresh-skills-pack.sh first" >&2
  exit 1
fi

if [[ "$LIST_ONLY" -eq 1 ]]; then
  python3 - "$PLAYBOOKS_JSON" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
for pb, meta in data.items():
    print(f"{pb:12} {len(meta['skills']):2} skills  — {meta['title']}")
PY
  exit 0
fi

if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 /path/to/target-repo --playbook <id>[,id...]" >&2
  echo "       $0 --list" >&2
  exit 1
fi

if [[ ! -d "$TARGET" ]]; then
  echo "Target repo does not exist: $TARGET" >&2
  exit 1
fi

if [[ -z "$PLAYBOOK_ARGS" ]]; then
  echo "Pass --playbook <id> (try --list). Playbook-mapped sync only — no silent full dump." >&2
  exit 1
fi

python3 - "$PLAYBOOKS_JSON" "$SKILLS_DIR" "$TARGET" "$PLAYBOOK_ARGS" <<'PY'
import json, shutil, sys
from pathlib import Path

playbooks = json.load(open(sys.argv[1]))
skills_root = Path(sys.argv[2])
target = Path(sys.argv[3])
requested = [p.strip() for p in sys.argv[4].split(",") if p.strip()]

unknown = [p for p in requested if p not in playbooks]
if unknown:
    raise SystemExit(f"Unknown playbook(s): {', '.join(unknown)}. Run --list.")

skill_names: list[str] = []
seen: set[str] = set()
for pb in requested:
    for name in playbooks[pb]["skills"]:
        if name not in seen:
            seen.add(name)
            skill_names.append(name)

dest_root = target / ".cursor" / "skills"
dest_root.mkdir(parents=True, exist_ok=True)

# Optional: also copy playbook-linked commands/agents from design-promax if present
copied = []
missing = []
for name in skill_names:
    src = skills_root / name
    if not src.is_dir():
        missing.append(name)
        continue
    dest = dest_root / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    copied.append(name)

# Write a marker so Cloud Agents know what was synced
marker = target / ".cursor" / "skills-pack.json"
marker.write_text(
    json.dumps(
        {
            "playbooks": requested,
            "skills": copied,
            "source": "cursortg-link/skills-pack",
        },
        indent=2,
    )
    + "\n"
)

print(f"Synced {len(copied)} skills for playbook(s): {', '.join(requested)}")
print(f" -> {dest_root}")
if missing:
    print("Missing from skills-pack (run refresh): " + ", ".join(missing))
print("Next: commit .cursor/ in the target repo, then /newagent from Telegram with the same playbook.")
PY

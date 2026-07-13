from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Playbook:
    id: str
    title: str
    summary: str
    body: str

    def render_preamble(self) -> str | None:
        if self.id == "none":
            return None
        return self.body.strip()


def default_playbooks_dir() -> Path:
    candidates = [
        Path.cwd() / "agent-playbooks",
        Path("/app/agent-playbooks"),
        # Editable / source checkout: src/cursor_tg_connector/.. /..
        Path(__file__).resolve().parents[2] / "agent-playbooks",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return candidates[0]


class PlaybookService:
    def __init__(self, playbooks_dir: Path | None = None) -> None:
        self.playbooks_dir = playbooks_dir or default_playbooks_dir()
        self._cache: dict[str, Playbook] | None = None

    def list_playbooks(self) -> list[Playbook]:
        playbooks = list(self._load_all().values())
        # Keep "none" last for nicer Telegram UX
        playbooks.sort(key=lambda item: (item.id == "none", item.id))
        return playbooks

    def get(self, playbook_id: str) -> Playbook:
        playbook_id = playbook_id.strip().lower()
        playbooks = self._load_all()
        if playbook_id not in playbooks:
            available = ", ".join(sorted(playbooks))
            raise KeyError(f"Unknown playbook '{playbook_id}'. Available: {available}")
        return playbooks[playbook_id]

    def compose_prompt(self, playbook_id: str | None, user_prompt: str) -> str:
        user_prompt = user_prompt.strip()
        if not playbook_id or playbook_id == "none":
            return user_prompt

        playbook = self.get(playbook_id)
        preamble = playbook.render_preamble()
        if not preamble:
            return user_prompt
        return (
            f"{preamble}\n\n"
            "---\n\n"
            "## User task\n\n"
            f"{user_prompt}"
        )

    def format_catalog(self) -> str:
        lines = ["Available Cloud Agent playbooks:", ""]
        for playbook in self.list_playbooks():
            lines.append(f"• `{playbook.id}` — {playbook.title}: {playbook.summary}")
        lines.extend(
            [
                "",
                "During /newagent, pick a playbook after the branch step.",
                "Or run /useplaybook <id> while waiting for the prompt.",
                "",
                "Before launch, sync skills into the TARGET repo:",
                "./scripts/sync-skills-to-repo.sh /path/to/repo --playbook <id>",
                "Then commit .cursor/ so Cloud Agents can see the skills.",
            ]
        )
        return "\n".join(lines)

    def _load_all(self) -> dict[str, Playbook]:
        if self._cache is not None:
            return self._cache

        loaded: dict[str, Playbook] = {}
        if self.playbooks_dir.is_dir():
            for path in sorted(self.playbooks_dir.glob("*.md")):
                playbook = _parse_playbook(path)
                loaded[playbook.id] = playbook
        self._cache = loaded
        return loaded


def _parse_playbook(path: Path) -> Playbook:
    text = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2].lstrip("\n")
            for line in frontmatter.splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()

    playbook_id = meta.get("id") or path.stem
    return Playbook(
        id=playbook_id,
        title=meta.get("title") or playbook_id.replace("-", " ").title(),
        summary=meta.get("summary") or "",
        body=body,
    )

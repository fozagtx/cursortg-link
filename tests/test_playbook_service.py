from __future__ import annotations

from pathlib import Path

import pytest

from cursor_tg_connector.cursor_api_models import Agent, AgentConversation
from cursor_tg_connector.domain_types import WizardStep
from cursor_tg_connector.services_create_agent_service import CreateAgentError, CreateAgentService
from cursor_tg_connector.services_playbook_service import PlaybookService


class FakeCursorClient:
    def __init__(self) -> None:
        self.models = ["gpt-5.4", "opus-4.6-fast"]
        self.repositories = [
            "https://github.com/acme/repo-a",
            "https://github.com/acme/repo-b",
        ]
        self.agents: list[Agent] = []
        self.created_agent_calls: list[tuple[str, str, str, str]] = []
        self.conversations: dict[str, list[dict[str, str]]] = {}

    async def list_models(self) -> list[str]:
        return self.models

    async def list_repositories(self) -> list[str]:
        return self.repositories

    async def list_agents(self) -> list[Agent]:
        return self.agents

    async def create_agent(
        self,
        *,
        model: str,
        repository_url: str,
        base_branch: str,
        prompt_text: str,
        images=None,
        model_params=None,
    ) -> Agent:
        self.created_agent_calls.append((model, repository_url, base_branch, prompt_text))
        return Agent.model_validate(
            {
                "id": "agent-123",
                "name": "Build feature",
                "status": "CREATING",
                "source": {"repository": repository_url, "ref": base_branch},
                "target": {"url": "https://cursor.com/agent-123", "branchName": "cursor/branch"},
                "createdAt": "2024-01-01T00:00:00Z",
            }
        )

    async def get_conversation(self, agent_id: str) -> AgentConversation:
        return AgentConversation.model_validate(
            {
                "id": agent_id,
                "messages": self.conversations.get(agent_id, []),
            }
        )


def test_playbook_service_lists_expected_ids() -> None:
    service = PlaybookService()
    ids = [playbook.id for playbook in service.list_playbooks()]
    assert ids[-1] == "none"
    for expected in ("ui", "seo", "ship", "hackathon", "fullstack"):
        assert expected in ids


def test_compose_prompt_prepends_playbook() -> None:
    service = PlaybookService()
    composed = service.compose_prompt("ship", "Build the checkout flow")
    assert "## User task" in composed
    assert "Build the checkout flow" in composed
    assert "demo" in composed.lower() or "Ship" in composed

    assert service.compose_prompt("none", "Just this") == "Just this"


@pytest.mark.asyncio
async def test_finish_prompt_includes_playbook_preamble(state_repo) -> None:
    client = FakeCursorClient()
    service = CreateAgentService(client, state_repo)

    await service.start_wizard(1234, 5678)
    await service.choose_model(1234, "gpt-5.4")
    await service.choose_repository(1234, 0)
    await service.save_branch(1234, "main")
    await service.choose_playbook(1234, "ui")
    await service.finish_prompt(1234, "Build a pricing page")

    assert len(client.created_agent_calls) == 1
    _, _, _, prompt_text = client.created_agent_calls[0]
    assert "design-promax" in prompt_text
    assert "Build a pricing page" in prompt_text
    assert "## User task" in prompt_text


@pytest.mark.asyncio
async def test_choose_playbook_rejects_outside_wizard(state_repo) -> None:
    service = CreateAgentService(FakeCursorClient(), state_repo)
    with pytest.raises(CreateAgentError, match="only available"):
        await service.choose_playbook(1234, "ui")

    session = await service.get_session(1234)
    assert session.wizard_state == WizardStep.IDLE


def test_playbook_service_reads_from_custom_dir(tmp_path: Path) -> None:
    playbook = tmp_path / "demo.md"
    playbook.write_text(
        "---\nid: demo\ntitle: Demo\nsummary: Test playbook\n---\n\n# Demo body\n",
        encoding="utf-8",
    )
    service = PlaybookService(tmp_path)
    assert service.get("demo").title == "Demo"
    assert "Demo body" in service.compose_prompt("demo", "Do the thing")

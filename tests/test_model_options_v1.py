from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx

from cursor_tg_connector.cursor_api_client import CursorApiClient, _expand_v1_model_options
from cursor_tg_connector.cursor_api_models import ModelCatalogItem, ModelOption


def test_expand_v1_model_options_includes_effort_variants() -> None:
    items = [
        ModelCatalogItem.model_validate(
            {
                "id": "claude-4.6-opus",
                "displayName": "Claude 4.6 Opus",
                "parameters": [
                    {
                        "id": "reasoning",
                        "displayName": "Reasoning",
                        "values": [
                            {"value": "medium", "displayName": "Medium"},
                            {"value": "high", "displayName": "High"},
                        ],
                    }
                ],
            }
        ),
    ]

    options = _expand_v1_model_options(items)
    labels = [option.label for option in options]
    assert any("Grok 4.5" == label for label in labels)
    assert any("High" in label for label in labels)
    assert any("Medium" in label or "medium" in label for label in labels)
    assert all(isinstance(option, ModelOption) for option in options)


@pytest.mark.asyncio
async def test_create_agent_sends_v1_model_params() -> None:
    async with httpx.AsyncClient(base_url="https://api.cursor.com") as http_client:
        client = CursorApiClient(
            api_key="test-key",
            base_url="https://api.cursor.com",
            http_client=http_client,
        )
        with respx.mock(assert_all_called=True) as router:
            route = router.post("https://api.cursor.com/v1/agents").mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "agent": {
                            "id": "bc-1",
                            "name": "Demo",
                            "status": "ACTIVE",
                            "url": "https://cursor.com/agents/bc-1",
                            "createdAt": "2026-01-01T00:00:00Z",
                        }
                    },
                )
            )
            agent = await client.create_agent(
                model="claude-4.6-opus",
                repository_url="https://github.com/acme/repo",
                base_branch="main",
                prompt_text="ship it",
                model_params=[{"id": "reasoning", "value": "high"}],
            )

    assert agent.id == "bc-1"
    assert agent.status == "RUNNING"
    assert route.called
    body: dict[str, Any] = json.loads(route.calls.last.request.content.decode())
    assert body["model"]["id"] == "claude-4.6-opus"
    assert body["model"]["params"] == [{"id": "reasoning", "value": "high"}]

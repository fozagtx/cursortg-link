from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PromptImage(BaseModel):
    data: str
    dimension: dict[str, int] | None = None


class AgentSource(BaseModel):
    repository: str
    ref: str | None = None


class AgentTarget(BaseModel):
    url: str
    branch_name: str | None = Field(default=None, alias="branchName")
    pr_url: str | None = Field(default=None, alias="prUrl")


class Agent(BaseModel):
    id: str
    name: str
    status: str
    source: AgentSource
    target: AgentTarget
    summary: str | None = None
    created_at: str = Field(alias="createdAt")


class ListAgentsResponse(BaseModel):
    agents: list[Agent]
    next_cursor: str | None = Field(default=None, alias="nextCursor")


class ConversationMessage(BaseModel):
    id: str
    type: Literal["user_message", "assistant_message"]
    text: str


class AgentConversation(BaseModel):
    id: str
    messages: list[ConversationMessage]


class Repository(BaseModel):
    owner: str
    name: str
    repository: str


class ListRepositoriesResponse(BaseModel):
    repositories: list[Repository]


class ListModelsResponse(BaseModel):
    models: list[str]


class ModelParamValue(BaseModel):
    value: str
    display_name: str | None = Field(default=None, alias="displayName")


class ModelParameter(BaseModel):
    id: str
    display_name: str | None = Field(default=None, alias="displayName")
    values: list[ModelParamValue] = Field(default_factory=list)


class ModelVariant(BaseModel):
    params: list[dict[str, str]] = Field(default_factory=list)
    display_name: str | None = Field(default=None, alias="displayName")
    description: str | None = None
    is_default: bool | None = Field(default=None, alias="isDefault")


class ModelCatalogItem(BaseModel):
    id: str
    display_name: str | None = Field(default=None, alias="displayName")
    aliases: list[str] = Field(default_factory=list)
    parameters: list[ModelParameter] = Field(default_factory=list)
    variants: list[ModelVariant] = Field(default_factory=list)


class ListModelsV1Response(BaseModel):
    items: list[ModelCatalogItem] = Field(default_factory=list)


class ModelOption(BaseModel):
    """One Telegram-selectable model configuration."""

    label: str
    model_id: str
    params: list[dict[str, str]] = Field(default_factory=list)


class ApiKeyInfo(BaseModel):
    api_key_name: str = Field(alias="apiKeyName")
    created_at: str = Field(alias="createdAt")
    user_email: str | None = Field(default=None, alias="userEmail")


class ErrorBody(BaseModel):
    message: str | None = None


class ErrorEnvelope(BaseModel):
    error: ErrorBody | None = None
    code: str | None = None
    message: str | None = None

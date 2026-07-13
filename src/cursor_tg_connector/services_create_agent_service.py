from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from cursor_tg_connector.cursor_api_client import CursorApiClient
from cursor_tg_connector.cursor_api_models import Agent, ModelOption, PromptImage
from cursor_tg_connector.domain_types import SessionState, WizardStep
from cursor_tg_connector.persistence_state_repo import StateRepository
from cursor_tg_connector.services_playbook_service import PlaybookService
from cursor_tg_connector.utils_formatting import paginate

logger = logging.getLogger(__name__)


class CreateAgentError(RuntimeError):
    pass


@dataclass(slots=True)
class RepositoryPage:
    repositories: list[str]
    page: int
    total_pages: int


class CreateAgentService:
    def __init__(
        self,
        cursor_client: CursorApiClient,
        state_repo: StateRepository,
        playbook_service: PlaybookService | None = None,
    ) -> None:
        self.cursor_client = cursor_client
        self.state_repo = state_repo
        self.playbook_service = playbook_service or PlaybookService()

    async def start_wizard(self, telegram_user_id: int, chat_id: int) -> list[str]:
        session = await self.state_repo.update_chat_context(telegram_user_id, chat_id)
        if session.wizard_state != WizardStep.IDLE:
            raise CreateAgentError(
                "A create-agent wizard is already in progress. Use /cancel to exit it."
            )

        if self._is_rate_limited(session):
            raise CreateAgentError("You can only start /newagent once per minute.")

        options = await self._load_model_options()
        if not options:
            raise CreateAgentError("Cursor returned no available models.")

        labels = [option.label for option in options]
        await self.state_repo.set_last_create_agent_at(telegram_user_id, datetime.now(tz=UTC))
        await self.state_repo.set_wizard(
            telegram_user_id,
            WizardStep.WAITING_MODEL,
            {
                "models": labels,
                "model_options": [option.model_dump() for option in options],
            },
        )
        return labels

    async def get_model_page(
        self,
        telegram_user_id: int,
        page: int,
        per_page: int = 8,
    ) -> RepositoryPage:
        session = await self.state_repo.get_session(telegram_user_id)
        models = self._wizard_list(session, "models")
        items, current_page, total_pages = paginate(models, page, per_page)
        return RepositoryPage(repositories=items, page=current_page, total_pages=total_pages)

    async def choose_model(self, telegram_user_id: int, model_id: str) -> RepositoryPage:
        """Backward-compatible: accept label or model id string."""
        session = await self.state_repo.get_session(telegram_user_id)
        options = self._model_options(session)
        labels = [option.label for option in options]
        if session.wizard_state != WizardStep.WAITING_MODEL:
            raise CreateAgentError(
                "That model selection is no longer valid. Run /newagent again."
            )

        index = next((i for i, option in enumerate(options) if option.label == model_id), None)
        if index is None:
            index = next(
                (i for i, option in enumerate(options) if option.model_id == model_id),
                None,
            )
        if index is None and model_id in labels:
            index = labels.index(model_id)
        if index is None:
            raise CreateAgentError(
                "That model selection is no longer valid. Run /newagent again."
            )
        return await self.choose_model_index(telegram_user_id, index)

    async def choose_model_index(self, telegram_user_id: int, model_index: int) -> RepositoryPage:
        session = await self.state_repo.get_session(telegram_user_id)
        options = self._model_options(session)
        if session.wizard_state != WizardStep.WAITING_MODEL or model_index >= len(options):
            raise CreateAgentError(
                "That model selection is no longer valid. Run /newagent again."
            )

        selected = options[model_index]
        repositories = await self.cursor_client.list_repositories()
        if not repositories:
            raise CreateAgentError("Cursor returned no available repositories.")

        payload = {
            "model": selected.model_id,
            "model_label": selected.label,
            "model_params": selected.params,
            "repositories": repositories,
        }
        await self.state_repo.set_wizard(telegram_user_id, WizardStep.WAITING_REPOSITORY, payload)
        return self.get_repository_page_from_payload(repositories, 0)

    async def get_repository_page(
        self,
        telegram_user_id: int,
        page: int,
        per_page: int = 8,
    ) -> RepositoryPage:
        session = await self.state_repo.get_session(telegram_user_id)
        repositories = self._wizard_list(session, "repositories")
        return self.get_repository_page_from_payload(repositories, page, per_page)

    def get_repository_page_from_payload(
        self,
        repositories: list[str],
        page: int,
        per_page: int = 8,
    ) -> RepositoryPage:
        items, current_page, total_pages = paginate(repositories, page, per_page)
        return RepositoryPage(repositories=items, page=current_page, total_pages=total_pages)

    async def choose_repository(
        self, telegram_user_id: int, repository_index: int
    ) -> tuple[str, list[str]]:
        session = await self.state_repo.get_session(telegram_user_id)
        repositories = self._wizard_list(session, "repositories")
        if (
            session.wizard_state != WizardStep.WAITING_REPOSITORY
            or repository_index >= len(repositories)
        ):
            raise CreateAgentError(
                "That repository selection is no longer valid. Run /newagent again."
            )

        repository = repositories[repository_index]
        branches = await self._fetch_branches_for_repository(repository)

        payload = {
            "model": session.wizard_payload["model"],
            "model_label": session.wizard_payload.get("model_label"),
            "model_params": session.wizard_payload.get("model_params") or [],
            "repository": repository,
            "branches": branches,
        }
        await self.state_repo.set_wizard(telegram_user_id, WizardStep.WAITING_BRANCH, payload)
        return repository, branches

    async def get_branch_page(
        self,
        telegram_user_id: int,
        page: int,
        per_page: int = 8,
    ) -> RepositoryPage:
        session = await self.state_repo.get_session(telegram_user_id)
        branches = self._wizard_list(session, "branches")
        return self.get_branch_page_from_payload(branches, page, per_page)

    def get_branch_page_from_payload(
        self,
        branches: list[str],
        page: int,
        per_page: int = 8,
    ) -> RepositoryPage:
        items, current_page, total_pages = paginate(branches, page, per_page)
        return RepositoryPage(repositories=items, page=current_page, total_pages=total_pages)

    async def choose_branch(self, telegram_user_id: int, branch_index: int) -> None:
        session = await self.state_repo.get_session(telegram_user_id)
        branches = self._wizard_list(session, "branches")
        if (
            session.wizard_state != WizardStep.WAITING_BRANCH
            or branch_index >= len(branches)
        ):
            raise CreateAgentError(
                "That branch selection is no longer valid. Run /newagent again."
            )

        payload = dict(session.wizard_payload)
        payload["branch"] = branches[branch_index]
        del payload["branches"]
        await self.state_repo.set_wizard(telegram_user_id, WizardStep.WAITING_PLAYBOOK, payload)

    async def save_branch(self, telegram_user_id: int, branch_name: str) -> None:
        branch_name = branch_name.strip()
        if not branch_name:
            raise CreateAgentError("Base branch cannot be empty.")

        session = await self.state_repo.get_session(telegram_user_id)
        if session.wizard_state != WizardStep.WAITING_BRANCH:
            raise CreateAgentError("No branch input is expected right now.")

        payload = dict(session.wizard_payload)
        payload["branch"] = branch_name
        payload.pop("branches", None)
        await self.state_repo.set_wizard(telegram_user_id, WizardStep.WAITING_PLAYBOOK, payload)

    async def choose_playbook(self, telegram_user_id: int, playbook_id: str) -> str:
        session = await self.state_repo.get_session(telegram_user_id)
        if session.wizard_state not in {WizardStep.WAITING_PLAYBOOK, WizardStep.WAITING_PROMPT}:
            raise CreateAgentError(
                "Playbook selection is only available during /newagent after the branch step."
            )

        try:
            playbook = self.playbook_service.get(playbook_id)
        except KeyError as exc:
            raise CreateAgentError(str(exc)) from exc

        payload = dict(session.wizard_payload)
        payload["playbook"] = playbook.id
        await self.state_repo.set_wizard(telegram_user_id, WizardStep.WAITING_PROMPT, payload)
        return playbook.id

    async def finish_prompt(
        self,
        telegram_user_id: int,
        prompt_text: str,
        images: list[PromptImage] | None = None,
    ) -> Agent:
        prompt_text = prompt_text.strip()
        if not prompt_text:
            raise CreateAgentError("Prompt text cannot be empty.")

        session = await self.state_repo.get_session(telegram_user_id)
        if session.wizard_state != WizardStep.WAITING_PROMPT:
            raise CreateAgentError("No prompt input is expected right now.")

        payload = session.wizard_payload
        composed_prompt = self.playbook_service.compose_prompt(
            payload.get("playbook"),
            prompt_text,
        )
        previous_active_agent_id = session.active_agent_id
        model_params = payload.get("model_params")
        if not isinstance(model_params, list):
            model_params = []
        agent = await self.cursor_client.create_agent(
            model=payload["model"],
            repository_url=payload["repository"],
            base_branch=payload["branch"],
            prompt_text=composed_prompt,
            images=images,
            model_params=model_params,
        )
        await self.state_repo.set_delivery_cursor(agent.id, 0)
        if previous_active_agent_id and previous_active_agent_id != agent.id:
            await self._silence_agent(previous_active_agent_id)
        await self.state_repo.clear_wizard(telegram_user_id)
        await self.state_repo.set_active_agent(telegram_user_id, agent.id)
        return agent

    async def cancel(self, telegram_user_id: int) -> bool:
        session = await self.state_repo.get_session(telegram_user_id)
        if session.wizard_state == WizardStep.IDLE:
            return False
        await self.state_repo.clear_wizard(telegram_user_id)
        return True

    async def get_session(self, telegram_user_id: int) -> SessionState:
        return await self.state_repo.get_session(telegram_user_id)

    def _is_rate_limited(self, session: SessionState) -> bool:
        if not session.last_create_agent_at:
            return False
        last_start = datetime.fromisoformat(session.last_create_agent_at)
        return datetime.now(tz=UTC) - last_start < timedelta(minutes=1)

    async def _load_model_options(self) -> list[ModelOption]:
        if hasattr(self.cursor_client, "list_model_options"):
            return await self.cursor_client.list_model_options()
        models = await self.cursor_client.list_models()
        return [ModelOption(label=model, model_id=model, params=[]) for model in models]

    def _model_options(self, session: SessionState) -> list[ModelOption]:
        raw = session.wizard_payload.get("model_options")
        if isinstance(raw, list) and raw:
            options: list[ModelOption] = []
            for item in raw:
                if isinstance(item, dict):
                    options.append(ModelOption.model_validate(item))
            if options:
                return options
        labels = self._wizard_list(session, "models")
        return [ModelOption(label=label, model_id=label, params=[]) for label in labels]

    async def _fetch_branches_for_repository(self, repository_url: str) -> list[str]:
        try:
            agents = await self.cursor_client.list_agents()
        except Exception:
            agents = []

        seen: set[str] = set()
        branches: list[str] = []
        for agent in agents:
            ref = agent.source.ref
            if ref and agent.source.repository == repository_url and ref not in seen:
                seen.add(ref)
                branches.append(ref)

        if "main" not in seen:
            branches.insert(0, "main")

        return branches

    def _wizard_list(self, session: SessionState, key: str) -> list[str]:
        values = session.wizard_payload.get(key)
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise CreateAgentError(
                "Wizard state is missing required options. Run /newagent again."
            )
        return values

    async def _silence_agent(self, agent_id: str) -> None:
        try:
            conversation = await self.cursor_client.get_conversation(agent_id)
            assistant_messages = [
                message for message in conversation.messages if message.type == "assistant_message"
            ]
            last_message = assistant_messages[-1] if assistant_messages else None
            await self.state_repo.set_delivery_state(
                agent_id,
                len(assistant_messages),
                last_message_id=last_message.id if last_message else None,
                last_message_text_length=len(last_message.text) if last_message else 0,
            )
        except Exception:
            logger.warning(
                "Failed to silence unread state for previous active agent %s",
                agent_id,
                exc_info=True,
            )
        finally:
            await self.state_repo.clear_notice_state(agent_id)

from typing import Any

import httpx

from app.core.config import settings
from app.schemas.runtime import AstrBotReplyRequest, ChatwootMessagePayload


class AstrBotAdapterError(RuntimeError):
    pass


class AstrBotService:
    def generate_reply(self, payload: ChatwootMessagePayload, preset: dict[str, Any]) -> str:
        if settings.astrbot_mock_mode:
            return self._build_mock_reply(payload)

        body = AstrBotReplyRequest(
            conversation_id=str(payload.conversation_id),
            user_message=payload.content,
            contact_name=payload.contact_name,
            preset=preset,
            metadata=payload.metadata,
        ).model_dump()

        try:
            with httpx.Client(base_url=settings.astrbot_base_url, timeout=settings.astrbot_timeout_seconds) as client:
                response = client.post(
                    settings.astrbot_chat_path,
                    json=body,
                    headers=self._headers(),
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise AstrBotAdapterError(f"AstrBot request failed: {exc}") from exc

        reply = self._extract_reply(response.json())
        if not reply:
            raise AstrBotAdapterError("AstrBot response did not contain a usable reply")
        return reply

    def health_status(self) -> str:
        if settings.astrbot_mock_mode:
            return "mock"
        try:
            with httpx.Client(base_url=settings.astrbot_base_url, timeout=5.0) as client:
                response = client.get(settings.astrbot_health_path, headers=self._headers())
                response.raise_for_status()
            return "ok"
        except httpx.HTTPError:
            return "error"

    @staticmethod
    def _build_mock_reply(payload: ChatwootMessagePayload) -> str:
        prefix = f"{payload.contact_name}锛? if payload.contact_name else ""
        condensed = payload.content.strip().replace("\r", " ").replace("\n", " ")[:120]
        return f"{prefix}宸叉敹鍒颁綘鐨勯棶棰樸€傚綋鍓嶇敱 AI 鑷姩鎺ュ緟銆傞棶棰樻憳瑕侊細{condensed}銆?

    @staticmethod
    def _extract_reply(data: dict[str, Any]) -> str | None:
        direct_reply = data.get("reply")
        if isinstance(direct_reply, str) and direct_reply.strip():
            return direct_reply.strip()

        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            message = choices[0].get("message", {})
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()
        return None

    @staticmethod
    def _headers() -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if settings.astrbot_api_key and settings.astrbot_api_key != "replace_me":
            headers["Authorization"] = f"Bearer {settings.astrbot_api_key}"
        return headers


astrbot_service = AstrBotService()

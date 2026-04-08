import json
from typing import Any

import httpx

from app.core.config import settings
from app.core.security import verify_chatwoot_signature
from app.schemas.runtime import ChatwootMessagePayload, ChatwootWebhookPayload


class ChatwootWebhookError(ValueError):
    pass


class ChatwootDeliveryError(RuntimeError):
    pass


class ChatwootService:
    def verify_webhook(self, *, raw_body: bytes, timestamp: str | None, signature: str | None) -> None:
        if settings.chatwoot_mock_mode:
            return

        secret = settings.chatwoot_webhook_secret
        if not secret or secret == "replace_me":
            return
        if not timestamp or not signature:
            raise ChatwootWebhookError("Missing Chatwoot signature headers")
        if not verify_chatwoot_signature(
            secret=secret,
            timestamp=timestamp,
            raw_body=raw_body,
            received_signature=signature,
        ):
            raise ChatwootWebhookError("Invalid Chatwoot webhook signature")

    def parse_webhook(self, raw_body: bytes) -> ChatwootMessagePayload | None:
        payload = ChatwootWebhookPayload.model_validate(json.loads(raw_body.decode("utf-8")))
        if payload.event != "message_created":
            return None
        if payload.private:
            return None

        sender_type = (payload.sender.type if payload.sender else payload.sender_type) or ""
        normalized_sender_type = sender_type.lower()
        if normalized_sender_type and normalized_sender_type not in {"contact", "user", "visitor"}:
            return None

        message_type = payload.message_type
        if isinstance(message_type, str) and message_type.lower() == "outgoing":
            return None

        conversation_id = payload.conversation.id if payload.conversation and payload.conversation.id else payload.conversation_id
        if not conversation_id or not payload.content or not payload.content.strip():
            return None

        return ChatwootMessagePayload(
            conversation_id=conversation_id,
            content=payload.content,
            sender_type="user",
            contact_name=payload.sender.name if payload.sender else None,
            event=payload.event,
            metadata={
                "content_attributes": payload.content_attributes,
                "additional_attributes": payload.additional_attributes,
            },
        )

    def send_message(self, *, conversation_id: int, content: str) -> dict[str, Any]:
        if settings.chatwoot_mock_mode:
            return {"status": "mock", "conversation_id": conversation_id, "content": content}

        try:
            with httpx.Client(base_url=settings.chatwoot_base_url, timeout=settings.chatwoot_timeout_seconds) as client:
                response = client.post(
                    f"/api/v1/accounts/{settings.chatwoot_account_id}/conversations/{conversation_id}/messages",
                    json={
                        "content": content,
                        "message_type": "outgoing",
                        "private": False,
                        "content_type": "text",
                        "content_attributes": {},
                    },
                    headers=self._headers(),
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ChatwootDeliveryError(f"Chatwoot delivery failed: {exc}") from exc
        return response.json()

    def health_status(self) -> str:
        if settings.chatwoot_mock_mode:
            return "mock"
        try:
            with httpx.Client(base_url=settings.chatwoot_base_url, timeout=5.0) as client:
                response = client.get("/", headers=self._headers())
                response.raise_for_status()
            return "ok"
        except httpx.HTTPError:
            return "error"

    @staticmethod
    def _headers() -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if settings.chatwoot_api_token and settings.chatwoot_api_token != "replace_me":
            headers["api_access_token"] = settings.chatwoot_api_token
        return headers


chatwoot_service = ChatwootService()

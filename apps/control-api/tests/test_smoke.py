import json

from fastapi.testclient import TestClient

from app.core.security import build_chatwoot_signature
from app.db.base import Base
from app.db.bootstrap import init_db
from app.db.session import engine
from app.main import app
from app.services.astrbot_service import astrbot_service
from app.services.chatwoot_service import chatwoot_service


Base.metadata.drop_all(bind=engine)
init_db()
client = TestClient(app)


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "AI Customer Platform Control API"


def test_create_preset_and_route_message() -> None:
    create_response = client.post(
        "/api/admin/presets",
        json={
            "name": "night-shift",
            "system_prompt": "night mode auto service",
            "welcome_message": "hello",
            "fallback_message": "handover",
            "tone": "friendly",
            "knowledge_base_enabled": True,
            "plugins_enabled": False,
            "max_reply_chars": 800,
            "multi_turn_enabled": True,
            "is_active": True,
        },
    )
    assert create_response.status_code == 200

    route_response = client.post(
        "/api/runtime/route-message",
        json={
            "conversation_id": 1001,
            "content": "when will my order ship",
            "sender_type": "user",
            "contact_name": "Lilei",
        },
    )
    assert route_response.status_code == 200
    assert route_response.json()["action"] == "ai_reply"


def test_handover_blocks_ai() -> None:
    handover_response = client.post(
        "/api/admin/conversations/2002/handover",
        json={"reason": "manual takeover", "operator_name": "ops"},
    )
    assert handover_response.status_code == 200

    route_response = client.post(
        "/api/runtime/route-message",
        json={
            "conversation_id": 2002,
            "content": "I want a refund",
            "sender_type": "user",
        },
    )
    assert route_response.status_code == 200
    assert route_response.json()["action"] == "human"


def test_chatwoot_webhook_signature_and_delivery(monkeypatch) -> None:
    sent_messages: list[dict] = []

    def fake_generate_reply(payload, preset):
        return f"auto reply: {payload.content}"

    def fake_send_message(*, conversation_id: int, content: str):
        sent_messages.append({"conversation_id": conversation_id, "content": content})
        return {"status": "mock"}

    monkeypatch.setattr("app.core.config.settings.chatwoot_mock_mode", False)
    monkeypatch.setattr("app.core.config.settings.chatwoot_webhook_secret", "test-secret")
    monkeypatch.setattr(astrbot_service, "generate_reply", fake_generate_reply)
    monkeypatch.setattr(chatwoot_service, "send_message", fake_send_message)

    body = {
        "event": "message_created",
        "content": "I need an invoice",
        "message_type": "incoming",
        "private": False,
        "conversation": {"id": 3003},
        "sender": {"name": "Hanmeimei", "type": "contact"},
    }
    raw_body = json.dumps(body).encode("utf-8")
    timestamp = "1712553600"
    signature = build_chatwoot_signature(secret="test-secret", timestamp=timestamp, raw_body=raw_body)

    response = client.post(
        "/api/runtime/chatwoot/webhook",
        content=raw_body,
        headers={
            "Content-Type": "application/json",
            "X-Chatwoot-Timestamp": timestamp,
            "X-Chatwoot-Signature": signature,
        },
    )

    assert response.status_code == 200
    assert response.json()["action"] == "ai_reply"
    assert sent_messages == [{"conversation_id": 3003, "content": "auto reply: I need an invoice"}]


def test_chatwoot_webhook_rejects_invalid_signature(monkeypatch) -> None:
    monkeypatch.setattr("app.core.config.settings.chatwoot_mock_mode", False)
    monkeypatch.setattr("app.core.config.settings.chatwoot_webhook_secret", "test-secret")

    response = client.post(
        "/api/runtime/chatwoot/webhook",
        json={
            "event": "message_created",
            "content": "test",
            "message_type": "incoming",
            "private": False,
            "conversation": {"id": 4004},
            "sender": {"name": "tester", "type": "contact"},
        },
        headers={
            "X-Chatwoot-Timestamp": "1712553600",
            "X-Chatwoot-Signature": "sha256=invalid",
        },
    )

    assert response.status_code == 401

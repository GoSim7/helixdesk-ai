from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.time import utc_now
from app.db.models import ConversationStateModel
from app.db.session import engine
from app.schemas.runtime import ChatwootMessagePayload, RouteMessageResponse
from app.services.astrbot_service import AstrBotAdapterError, astrbot_service
from app.services.audit_service import audit_service
from app.services.chatwoot_service import ChatwootDeliveryError, chatwoot_service
from app.services.handover_service import handover_service
from app.services.preset_service import preset_service
from app.services.settings_service import settings_service


class RoutingService:
    def route_chatwoot_message(
        self,
        payload: ChatwootMessagePayload,
        *,
        deliver_reply: bool = False,
    ) -> RouteMessageResponse:
        if payload.sender_type != "user":
            return RouteMessageResponse(action="ignore", reason="non-user message")

        system_settings = settings_service.get_system_settings()
        state = handover_service.get_or_create_state(payload.conversation_id)
        if state.state == "HUMAN_ACTIVE":
            return RouteMessageResponse(action="human", reason="conversation under manual handover")

        if not settings_service.refresh_runtime_flags():
            return RouteMessageResponse(action="human", reason="global ai disabled")

        preset = preset_service.get_default()
        if preset is None or not preset.is_active:
            if system_settings.fallback_to_human_on_error:
                return RouteMessageResponse(action="human", reason="no active preset")
            return RouteMessageResponse(action="ignore", reason="no active preset")

        try:
            reply = astrbot_service.generate_reply(
                payload,
                {
                    "id": preset.id,
                    "name": preset.name,
                    "system_prompt": preset.system_prompt,
                    "welcome_message": preset.welcome_message,
                    "fallback_message": preset.fallback_message,
                    "tone": preset.tone,
                    "knowledge_base_enabled": preset.knowledge_base_enabled,
                    "plugins_enabled": preset.plugins_enabled,
                    "max_reply_chars": preset.max_reply_chars,
                    "multi_turn_enabled": preset.multi_turn_enabled,
                },
            )
        except AstrBotAdapterError as exc:
            if system_settings.fallback_to_human_on_error:
                handover_service.handover_to_human(payload.conversation_id, "system", str(exc))
                return RouteMessageResponse(action="human", reason=str(exc))
            return RouteMessageResponse(action="ignore", reason=str(exc))

        with Session(engine) as db:
            row = db.scalar(
                select(ConversationStateModel).where(
                    ConversationStateModel.chatwoot_conversation_id == payload.conversation_id
                )
            )
            if row is None:
                row = ConversationStateModel(chatwoot_conversation_id=payload.conversation_id)
                db.add(row)
            row.state = "AI_ACTIVE"
            row.current_preset_id = preset.id
            row.updated_at = utc_now()
            db.commit()

        if deliver_reply:
            try:
                chatwoot_service.send_message(conversation_id=payload.conversation_id, content=reply)
            except ChatwootDeliveryError as exc:
                if system_settings.fallback_to_human_on_error:
                    handover_service.handover_to_human(payload.conversation_id, "system", str(exc))
                    return RouteMessageResponse(action="human", reason=str(exc))
                return RouteMessageResponse(action="ignore", reason=str(exc))

        audit_service.write(
            actor_name="system",
            action="conversation.ai_replied",
            target_type="conversation",
            target_id=str(payload.conversation_id),
            after_data={"preset_id": preset.id, "reply": reply},
        )
        return RouteMessageResponse(action="ai_reply", reason="ai reply generated", reply=reply)


routing_service = RoutingService()

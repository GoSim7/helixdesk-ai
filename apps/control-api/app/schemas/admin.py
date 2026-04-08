from datetime import datetime, time

from pydantic import BaseModel, Field


class SystemSettingsPayload(BaseModel):
    ai_enabled: bool = True
    auto_reply_enabled: bool = True
    default_preset_id: int | None = None
    fallback_to_human_on_error: bool = True
    restore_ai_on_conversation_reopen: bool = True
    timezone: str = "Asia/Shanghai"


class SystemSettingsResponse(SystemSettingsPayload):
    updated_at: datetime
    runtime_ai_enabled: bool


class BusinessHourPayload(BaseModel):
    weekday: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    ai_enabled_in_slot: bool


class AIPresetPayload(BaseModel):
    name: str
    system_prompt: str
    welcome_message: str | None = None
    fallback_message: str | None = None
    tone: str | None = None
    knowledge_base_enabled: bool = True
    plugins_enabled: bool = False
    max_reply_chars: int = 800
    multi_turn_enabled: bool = True
    is_active: bool = True


class AIPresetResponse(AIPresetPayload):
    id: int
    is_default: bool


class ConversationActionPayload(BaseModel):
    reason: str | None = None
    operator_name: str = "admin"


class ConversationStateResponse(BaseModel):
    chatwoot_conversation_id: int
    state: str
    current_preset_id: int | None
    handover_reason: str | None
    updated_at: datetime


class AuditLogResponse(BaseModel):
    actor_name: str
    action: str
    target_type: str
    target_id: str | None
    before_data: dict | None
    after_data: dict | None
    created_at: datetime

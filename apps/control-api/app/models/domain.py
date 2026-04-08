from dataclasses import dataclass, field
from datetime import datetime, time

from app.core.time import utc_now


@dataclass
class SystemSettings:
    ai_enabled: bool = True
    auto_reply_enabled: bool = True
    default_preset_id: int | None = None
    fallback_to_human_on_error: bool = True
    restore_ai_on_conversation_reopen: bool = True
    timezone: str = "Asia/Shanghai"
    updated_at: datetime = field(default_factory=utc_now)


@dataclass
class BusinessHourSlot:
    weekday: int
    start_time: time
    end_time: time
    ai_enabled_in_slot: bool


@dataclass
class AIPreset:
    id: int
    name: str
    system_prompt: str
    welcome_message: str | None = None
    fallback_message: str | None = None
    tone: str | None = None
    knowledge_base_enabled: bool = True
    plugins_enabled: bool = False
    max_reply_chars: int = 800
    multi_turn_enabled: bool = True
    is_default: bool = False
    is_active: bool = True


@dataclass
class ConversationState:
    chatwoot_conversation_id: int
    state: str = "AI_ACTIVE"
    current_preset_id: int | None = None
    handover_reason: str | None = None
    updated_at: datetime = field(default_factory=utc_now)


@dataclass
class AuditLog:
    actor_name: str
    action: str
    target_type: str
    target_id: str | None
    before_data: dict | None
    after_data: dict | None
    created_at: datetime = field(default_factory=utc_now)

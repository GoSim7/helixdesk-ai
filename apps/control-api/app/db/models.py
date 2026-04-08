from datetime import time

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.core.time import utc_now
from app.db.base import Base


class SystemSettingsModel(Base):
    __tablename__ = "system_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    ai_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    auto_reply_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    default_preset_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fallback_to_human_on_error: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    restore_ai_on_conversation_reopen: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Shanghai", nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)


class BusinessHourModel(Base):
    __tablename__ = "business_hours"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    weekday: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    ai_enabled_in_slot: Mapped[bool] = mapped_column(Boolean, nullable=False)


class AIPresetModel(Base):
    __tablename__ = "ai_presets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    welcome_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    fallback_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    tone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    knowledge_base_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    plugins_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    max_reply_chars: Mapped[int] = mapped_column(Integer, default=800, nullable=False)
    multi_turn_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ConversationStateModel(Base):
    __tablename__ = "conversation_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chatwoot_conversation_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    state: Mapped[str] = mapped_column(String(32), default="AI_ACTIVE", nullable=False)
    current_preset_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    handover_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_name: Mapped[str] = mapped_column(String(128), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    target_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    before_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    after_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

from fastapi import APIRouter, HTTPException

from app.schemas.admin import (
    AIPresetPayload,
    AIPresetResponse,
    AuditLogResponse,
    BusinessHourPayload,
    ConversationActionPayload,
    ConversationStateResponse,
    SystemSettingsPayload,
    SystemSettingsResponse,
)
from app.services.audit_service import audit_service
from app.services.handover_service import handover_service
from app.services.health_service import health_service
from app.services.preset_service import preset_service
from app.services.settings_service import settings_service

router = APIRouter()


@router.get("/system-settings", response_model=SystemSettingsResponse)
async def get_system_settings() -> SystemSettingsResponse:
    data = settings_service.get_system_settings()
    return SystemSettingsResponse(**data.__dict__, runtime_ai_enabled=settings_service.refresh_runtime_flags())


@router.put("/system-settings", response_model=SystemSettingsResponse)
async def update_system_settings(payload: SystemSettingsPayload) -> SystemSettingsResponse:
    data = settings_service.update_system_settings(payload)
    return SystemSettingsResponse(**data.__dict__, runtime_ai_enabled=settings_service.refresh_runtime_flags())


@router.get("/business-hours", response_model=list[BusinessHourPayload])
async def list_business_hours() -> list[BusinessHourPayload]:
    return [BusinessHourPayload(**item.__dict__) for item in settings_service.list_business_hours()]


@router.put("/business-hours", response_model=list[BusinessHourPayload])
async def replace_business_hours(payload: list[BusinessHourPayload]) -> list[BusinessHourPayload]:
    slots = settings_service.replace_business_hours(payload)
    return [BusinessHourPayload(**item.__dict__) for item in slots]


@router.get("/presets", response_model=list[AIPresetResponse])
async def list_presets() -> list[AIPresetResponse]:
    return [AIPresetResponse(**item.__dict__) for item in preset_service.list_presets()]


@router.post("/presets", response_model=AIPresetResponse)
async def create_preset(payload: AIPresetPayload) -> AIPresetResponse:
    preset = preset_service.create_preset(payload)
    return AIPresetResponse(**preset.__dict__)


@router.put("/presets/{preset_id}", response_model=AIPresetResponse)
async def update_preset(preset_id: int, payload: AIPresetPayload) -> AIPresetResponse:
    if preset_id not in {item.id for item in preset_service.list_presets()}:
        raise HTTPException(status_code=404, detail="Preset not found")
    preset = preset_service.update_preset(preset_id, payload)
    return AIPresetResponse(**preset.__dict__)


@router.post("/presets/{preset_id}/set-default", response_model=AIPresetResponse)
async def set_default_preset(preset_id: int) -> AIPresetResponse:
    if preset_id not in {item.id for item in preset_service.list_presets()}:
        raise HTTPException(status_code=404, detail="Preset not found")
    preset = preset_service.set_default(preset_id)
    return AIPresetResponse(**preset.__dict__)


@router.get("/conversations/handover", response_model=list[ConversationStateResponse])
async def list_handover_states() -> list[ConversationStateResponse]:
    return [ConversationStateResponse(**item.__dict__) for item in handover_service.list_states()]


@router.post("/conversations/{conversation_id}/handover", response_model=ConversationStateResponse)
async def handover_conversation(conversation_id: int, payload: ConversationActionPayload) -> ConversationStateResponse:
    state = handover_service.handover_to_human(conversation_id, payload.operator_name, payload.reason)
    return ConversationStateResponse(**state.__dict__)


@router.post("/conversations/{conversation_id}/restore-ai", response_model=ConversationStateResponse)
async def restore_ai(conversation_id: int, payload: ConversationActionPayload) -> ConversationStateResponse:
    state = handover_service.restore_to_ai(conversation_id, payload.operator_name, payload.reason)
    return ConversationStateResponse(**state.__dict__)


@router.get("/audit-logs", response_model=list[AuditLogResponse])
async def list_audit_logs() -> list[AuditLogResponse]:
    return [AuditLogResponse(**item.__dict__) for item in audit_service.list_logs()]


@router.get("/health")
async def get_admin_health():
    return health_service.get_health()

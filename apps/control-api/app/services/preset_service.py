from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AIPresetModel, SystemSettingsModel
from app.db.session import engine
from app.models.domain import AIPreset
from app.schemas.admin import AIPresetPayload
from app.services.audit_service import audit_service


class PresetService:
    def list_presets(self) -> list[AIPreset]:
        with Session(engine) as db:
            rows = db.scalars(select(AIPresetModel).order_by(AIPresetModel.id.asc())).all()
            return [self._to_domain(row) for row in rows]

    def create_preset(self, payload: AIPresetPayload) -> AIPreset:
        with Session(engine) as db:
            row = AIPresetModel(
                name=payload.name,
                system_prompt=payload.system_prompt,
                welcome_message=payload.welcome_message,
                fallback_message=payload.fallback_message,
                tone=payload.tone,
                knowledge_base_enabled=payload.knowledge_base_enabled,
                plugins_enabled=payload.plugins_enabled,
                max_reply_chars=payload.max_reply_chars,
                multi_turn_enabled=payload.multi_turn_enabled,
                is_active=payload.is_active,
                is_default=False,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            preset = self._to_domain(row)
        audit_service.write(
            actor_name="admin",
            action="preset.created",
            target_type="ai_preset",
            target_id=str(preset.id),
            after_data={"name": preset.name},
        )
        return preset

    def update_preset(self, preset_id: int, payload: AIPresetPayload) -> AIPreset:
        with Session(engine) as db:
            row = db.get(AIPresetModel, preset_id)
            before = self._to_domain(row).__dict__.copy()
            row.name = payload.name
            row.system_prompt = payload.system_prompt
            row.welcome_message = payload.welcome_message
            row.fallback_message = payload.fallback_message
            row.tone = payload.tone
            row.knowledge_base_enabled = payload.knowledge_base_enabled
            row.plugins_enabled = payload.plugins_enabled
            row.max_reply_chars = payload.max_reply_chars
            row.multi_turn_enabled = payload.multi_turn_enabled
            row.is_active = payload.is_active
            db.commit()
            db.refresh(row)
            preset = self._to_domain(row)
        audit_service.write(
            actor_name="admin",
            action="preset.updated",
            target_type="ai_preset",
            target_id=str(preset_id),
            before_data=before,
            after_data=preset.__dict__.copy(),
        )
        return preset

    def set_default(self, preset_id: int) -> AIPreset:
        with Session(engine) as db:
            rows = db.scalars(select(AIPresetModel)).all()
            for item in rows:
                item.is_default = item.id == preset_id
            settings = db.get(SystemSettingsModel, 1)
            settings.default_preset_id = preset_id
            db.commit()
            row = db.get(AIPresetModel, preset_id)
        audit_service.write(
            actor_name="admin",
            action="preset.set_default",
            target_type="ai_preset",
            target_id=str(preset_id),
            after_data={"default_preset_id": preset_id},
        )
        return self._to_domain(row)

    def get_default(self) -> AIPreset | None:
        with Session(engine) as db:
            settings = db.get(SystemSettingsModel, 1)
            if settings and settings.default_preset_id:
                explicit = db.get(AIPresetModel, settings.default_preset_id)
                if explicit and explicit.is_active:
                    return self._to_domain(explicit)
            row = db.scalar(select(AIPresetModel).where(AIPresetModel.is_default.is_(True), AIPresetModel.is_active.is_(True)))
            return self._to_domain(row) if row else None

    @staticmethod
    def _to_domain(row: AIPresetModel) -> AIPreset:
        return AIPreset(
            id=row.id,
            name=row.name,
            system_prompt=row.system_prompt,
            welcome_message=row.welcome_message,
            fallback_message=row.fallback_message,
            tone=row.tone,
            knowledge_base_enabled=row.knowledge_base_enabled,
            plugins_enabled=row.plugins_enabled,
            max_reply_chars=row.max_reply_chars,
            multi_turn_enabled=row.multi_turn_enabled,
            is_default=row.is_default,
            is_active=row.is_active,
        )


preset_service = PresetService()

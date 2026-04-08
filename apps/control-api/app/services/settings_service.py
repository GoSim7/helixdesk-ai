from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.time import utc_now
from app.db.models import BusinessHourModel, SystemSettingsModel
from app.db.session import engine
from app.models.domain import BusinessHourSlot, SystemSettings
from app.schemas.admin import BusinessHourPayload, SystemSettingsPayload
from app.services.audit_service import audit_service


class SettingsService:
    def get_system_settings(self) -> SystemSettings:
        with Session(engine) as db:
            row = db.get(SystemSettingsModel, 1)
            return self._settings_to_domain(row)

    def update_system_settings(self, payload: SystemSettingsPayload) -> SystemSettings:
        with Session(engine) as db:
            row = db.get(SystemSettingsModel, 1)
            before = self._settings_to_domain(row).__dict__.copy()
            row.ai_enabled = payload.ai_enabled
            row.auto_reply_enabled = payload.auto_reply_enabled
            row.default_preset_id = payload.default_preset_id
            row.fallback_to_human_on_error = payload.fallback_to_human_on_error
            row.restore_ai_on_conversation_reopen = payload.restore_ai_on_conversation_reopen
            row.timezone = payload.timezone
            row.updated_at = utc_now()
            db.commit()
        self.refresh_runtime_flags()
        audit_service.write(
            actor_name="admin",
            action="settings.updated",
            target_type="system_settings",
            target_id="default",
            before_data=before,
            after_data=self.get_system_settings().__dict__.copy(),
        )
        return self.get_system_settings()

    def list_business_hours(self) -> list[BusinessHourSlot]:
        with Session(engine) as db:
            rows = db.scalars(select(BusinessHourModel).order_by(BusinessHourModel.weekday.asc(), BusinessHourModel.start_time.asc())).all()
            return [self._hours_to_domain(row) for row in rows]

    def replace_business_hours(self, payload: list[BusinessHourPayload]) -> list[BusinessHourSlot]:
        before = [slot.__dict__.copy() for slot in self.list_business_hours()]
        with Session(engine) as db:
            db.query(BusinessHourModel).delete()
            for item in payload:
                db.add(
                    BusinessHourModel(
                        weekday=item.weekday,
                        start_time=item.start_time,
                        end_time=item.end_time,
                        ai_enabled_in_slot=item.ai_enabled_in_slot,
                    )
                )
            db.commit()
        self.refresh_runtime_flags()
        audit_service.write(
            actor_name="admin",
            action="business_hours.replaced",
            target_type="business_hours",
            target_id="global",
            before_data={"slots": before},
            after_data={"slots": [slot.__dict__.copy() for slot in self.list_business_hours()]},
        )
        return self.list_business_hours()

    def refresh_runtime_flags(self) -> bool:
        settings = self.get_system_settings()
        current = self._is_ai_enabled_by_schedule()
        self.runtime_ai_enabled = settings.ai_enabled and settings.auto_reply_enabled and current
        self.last_runtime_refresh = utc_now()
        return self.runtime_ai_enabled

    def _is_ai_enabled_by_schedule(self) -> bool:
        now = datetime.now()
        weekday = now.weekday()
        current_time = now.time().replace(tzinfo=None)
        slots = [slot for slot in self.list_business_hours() if slot.weekday == weekday]
        if not slots:
            return True
        for slot in slots:
            if slot.start_time <= current_time <= slot.end_time:
                return slot.ai_enabled_in_slot
        return True

    @staticmethod
    def _settings_to_domain(row: SystemSettingsModel) -> SystemSettings:
        return SystemSettings(
            ai_enabled=row.ai_enabled,
            auto_reply_enabled=row.auto_reply_enabled,
            default_preset_id=row.default_preset_id,
            fallback_to_human_on_error=row.fallback_to_human_on_error,
            restore_ai_on_conversation_reopen=row.restore_ai_on_conversation_reopen,
            timezone=row.timezone,
            updated_at=row.updated_at,
        )

    @staticmethod
    def _hours_to_domain(row: BusinessHourModel) -> BusinessHourSlot:
        return BusinessHourSlot(
            weekday=row.weekday,
            start_time=row.start_time,
            end_time=row.end_time,
            ai_enabled_in_slot=row.ai_enabled_in_slot,
        )


settings_service = SettingsService()
settings_service.runtime_ai_enabled = True
settings_service.last_runtime_refresh = utc_now()

from datetime import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.time import utc_now
from app.db.base import Base
from app.db.models import AIPresetModel, BusinessHourModel, SystemSettingsModel
from app.db.session import engine


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        settings = db.scalar(select(SystemSettingsModel).where(SystemSettingsModel.id == 1))
        if settings is None:
            db.add(
                SystemSettingsModel(
                    id=1,
                    ai_enabled=True,
                    auto_reply_enabled=True,
                    default_preset_id=1,
                    fallback_to_human_on_error=True,
                    restore_ai_on_conversation_reopen=True,
                    timezone="Asia/Shanghai",
                    updated_at=utc_now(),
                )
            )

        default_preset = db.scalar(select(AIPresetModel).where(AIPresetModel.id == 1))
        if default_preset is None:
            db.add(
                AIPresetModel(
                    id=1,
                    name="榛樿瀹㈡湇",
                    system_prompt="浣犳槸浼佷笟 AI 瀹㈡湇锛屽洖绛旀竻鏅般€佸噯纭€佺畝娲併€?,
                    welcome_message="鎮ㄥソ锛屾垜鏄櫤鑳藉鏈嶏紝寰堥珮鍏翠负鎮ㄦ湇鍔°€?,
                    fallback_message="鎶辨瓑锛岃繖涓棶棰樻垜鍏堣浆缁欎汉宸ュ鏈嶅鐞嗐€?,
                    is_default=True,
                    is_active=True,
                )
            )

        has_hours = db.scalar(select(BusinessHourModel.id).limit(1))
        if has_hours is None:
            for weekday in range(5):
                db.add(
                    BusinessHourModel(
                        weekday=weekday,
                        start_time=time(9, 0),
                        end_time=time(18, 0),
                        ai_enabled_in_slot=True,
                    )
                )
        db.commit()

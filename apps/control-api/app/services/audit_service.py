from app.core.serialization import make_json_safe
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AuditLogModel
from app.db.session import engine
from app.models.domain import AuditLog


class AuditService:
    def write(
        self,
        *,
        actor_name: str,
        action: str,
        target_type: str,
        target_id: str | None = None,
        before_data: dict | None = None,
        after_data: dict | None = None,
    ) -> None:
        with Session(engine) as db:
            db.add(
                AuditLogModel(
                    actor_name=actor_name,
                    action=action,
                    target_type=target_type,
                    target_id=target_id,
                    before_data=make_json_safe(before_data),
                    after_data=make_json_safe(after_data),
                )
            )
            db.commit()

    def list_logs(self) -> list[AuditLog]:
        with Session(engine) as db:
            rows = db.scalars(select(AuditLogModel).order_by(AuditLogModel.created_at.desc())).all()
            return [
                AuditLog(
                    actor_name=row.actor_name,
                    action=row.action,
                    target_type=row.target_type,
                    target_id=row.target_id,
                    before_data=row.before_data,
                    after_data=row.after_data,
                    created_at=row.created_at,
                )
                for row in rows
            ]


audit_service = AuditService()

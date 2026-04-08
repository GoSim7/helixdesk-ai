from app.core.time import utc_now
from app.db.models import ConversationStateModel
from app.db.session import engine
from app.models.domain import ConversationState
from app.services.audit_service import audit_service
from sqlalchemy import select
from sqlalchemy.orm import Session


class HandoverService:
    def get_or_create_state(self, conversation_id: int) -> ConversationState:
        with Session(engine) as db:
            row = db.scalar(
                select(ConversationStateModel).where(
                    ConversationStateModel.chatwoot_conversation_id == conversation_id
                )
            )
            if row is None:
                row = ConversationStateModel(chatwoot_conversation_id=conversation_id)
                db.add(row)
                db.commit()
                db.refresh(row)
            return self._to_domain(row)

    def list_states(self) -> list[ConversationState]:
        with Session(engine) as db:
            rows = db.scalars(select(ConversationStateModel).order_by(ConversationStateModel.updated_at.desc())).all()
            return [self._to_domain(row) for row in rows]

    def handover_to_human(self, conversation_id: int, operator_name: str, reason: str | None) -> ConversationState:
        with Session(engine) as db:
            row = self._get_or_create_row(db, conversation_id)
            before = self._to_domain(row).__dict__.copy()
            row.state = "HUMAN_ACTIVE"
            row.handover_reason = reason
            row.updated_at = utc_now()
            db.commit()
            db.refresh(row)
            state = self._to_domain(row)
        audit_service.write(
            actor_name=operator_name,
            action="conversation.handover_to_human",
            target_type="conversation",
            target_id=str(conversation_id),
            before_data=before,
            after_data=state.__dict__.copy(),
        )
        return state

    def restore_to_ai(self, conversation_id: int, operator_name: str, reason: str | None = None) -> ConversationState:
        with Session(engine) as db:
            row = self._get_or_create_row(db, conversation_id)
            before = self._to_domain(row).__dict__.copy()
            row.state = "AI_ACTIVE"
            row.handover_reason = reason
            row.updated_at = utc_now()
            db.commit()
            db.refresh(row)
            state = self._to_domain(row)
        audit_service.write(
            actor_name=operator_name,
            action="conversation.restore_to_ai",
            target_type="conversation",
            target_id=str(conversation_id),
            before_data=before,
            after_data=state.__dict__.copy(),
        )
        return state

    @staticmethod
    def _get_or_create_row(db: Session, conversation_id: int) -> ConversationStateModel:
        row = db.scalar(
            select(ConversationStateModel).where(
                ConversationStateModel.chatwoot_conversation_id == conversation_id
            )
        )
        if row is None:
            row = ConversationStateModel(chatwoot_conversation_id=conversation_id)
            db.add(row)
            db.flush()
        return row

    @staticmethod
    def _to_domain(row: ConversationStateModel) -> ConversationState:
        return ConversationState(
            chatwoot_conversation_id=row.chatwoot_conversation_id,
            state=row.state,
            current_preset_id=row.current_preset_id,
            handover_reason=row.handover_reason,
            updated_at=row.updated_at,
        )


handover_service = HandoverService()

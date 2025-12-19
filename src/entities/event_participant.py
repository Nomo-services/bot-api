from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid import uuid7

from src.core.database.base_class import Base
from src.entities.enums import EventParticipantRoleEnum, EventParticipationStatusEnum


class EventParticipant(Base):
    __tablename__ = "event_participants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)

    event_id = Column(
        UUID,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    role = Column(
        EventParticipantRoleEnum,
        nullable=False,
        default="participant",
    )
    status = Column(
        EventParticipationStatusEnum,
        nullable=False,
        default="invited",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "user_id",
            name="uq_event_participant",
        ),
    )

    # relationships
    event = relationship("Event", back_populates="participants")
    user = relationship("User", back_populates="event_participations")

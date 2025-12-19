from sqlalchemy import CheckConstraint, Column, DateTime, Index, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid import uuid7

from src.core.database.base_class import Base
from src.entities.enums import ReminderChannelEnum, ReminderStatusEnum


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)

    user_id = Column(
        UUID,
        ForeignKey("users.id"),
        nullable=False,
    )

    note_id = Column(
        UUID,
        ForeignKey("notes.id"),
        nullable=True,
    )
    event_id = Column(
        UUID,
        ForeignKey("events.id"),
        nullable=True,
    )

    fire_at = Column(DateTime(timezone=True), nullable=False)

    status = Column(
        ReminderStatusEnum,
        nullable=False,
        default="pending",
    )
    channel = Column(
        ReminderChannelEnum,
        nullable=False,
        default="telegram",
    )

    payload = Column(JSONB, nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_reminders_pending", "status", "fire_at"),
        CheckConstraint(
            "(note_id IS NOT NULL AND event_id IS NULL) OR "
            "(note_id IS NULL AND event_id IS NOT NULL)",
            name="ck_reminders_note_or_event",
        ),
    )

    # relationships
    user = relationship("User", back_populates="reminders")
    note = relationship("Note", back_populates="reminders")
    event = relationship("Event", back_populates="reminders")
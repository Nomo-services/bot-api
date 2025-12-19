from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid import uuid7

from src.core.database.base_class import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)

    space_id = Column(
        UUID,
        ForeignKey("spaces.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=True)
    all_day = Column(Boolean, nullable=False, default=False)
    location = Column(Text, nullable=True)

    recurrence_rule = Column(Text, nullable=True)  # RRULE string

    created_by = Column(
        UUID,
        ForeignKey("users.id"),
        nullable=False,
    )
    updated_by = Column(
        UUID,
        ForeignKey("users.id"),
        nullable=True,
    )

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
        Index("idx_events_space_start", "space_id", "starts_at"),
    )

    # relationships
    space = relationship("Space", back_populates="events")

    creator = relationship(
        "User",
        back_populates="events_created",
        foreign_keys=[created_by],
    )
    updater = relationship(
        "User",
        back_populates="events_updated",
        foreign_keys=[updated_by],
    )

    participants = relationship(
        "EventParticipant",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    reminders = relationship(
        "Reminder",
        back_populates="event",
        cascade="all, delete-orphan",
    )
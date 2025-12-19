from sqlalchemy import Boolean, Column, DateTime, Index, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid import uuid7

from src.core.database.base_class import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)

    space_id = Column(
        UUID,
        ForeignKey("spaces.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(Text, nullable=True)
    content = Column(Text, nullable=False)

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

    is_archived = Column(Boolean, nullable=False, default=False)
    main_due_at = Column(DateTime(timezone=True), nullable=True)

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
        Index("idx_notes_space", "space_id", "updated_at"),
    )

    # relationships
    space = relationship("Space", back_populates="notes")

    creator = relationship(
        "User",
        back_populates="notes_created",
        foreign_keys=[created_by],
    )
    updater = relationship(
        "User",
        back_populates="notes_updated",
        foreign_keys=[updated_by],
    )

    reminders = relationship(
        "Reminder",
        back_populates="note",
        cascade="all, delete-orphan",
    )
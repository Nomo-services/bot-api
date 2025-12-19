from sqlalchemy import BigInteger, Column, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid import uuid7

from src.core.database.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    telegram_user_id = Column(BigInteger, nullable=False, unique=True)
    telegram_username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    timezone = Column(String, nullable=False, default="UTC")
    locale = Column(String, nullable=False, default="ru")

    telegram_chat_id = Column(
        UUID,
        ForeignKey("telegram_chats.chat_id"),
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

    # relationships
    telegram_chat = relationship("TelegramChat", back_populates="users")

    spaces_created = relationship(
        "Space",
        back_populates="creator",
        foreign_keys="Space.created_by",
    )

    space_memberships = relationship(
        "SpaceMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    notes_created = relationship(
        "Note",
        back_populates="creator",
        foreign_keys="Note.created_by",
    )
    notes_updated = relationship(
        "Note",
        back_populates="updater",
        foreign_keys="Note.updated_by",
    )

    events_created = relationship(
        "Event",
        back_populates="creator",
        foreign_keys="Event.created_by",
    )
    events_updated = relationship(
        "Event",
        back_populates="updater",
        foreign_keys="Event.updated_by",
    )

    event_participations = relationship(
        "EventParticipant",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    reminders = relationship(
        "Reminder",
        back_populates="user",
        cascade="all, delete-orphan",
    )

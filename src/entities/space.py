from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid import uuid7

from src.core.database.base_class import Base
from src.entities.enums import SpaceTypeEnum

class Space(Base):
    __tablename__ = "spaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    name = Column(Text, nullable=False)
    type = Column(SpaceTypeEnum, nullable=False)

    created_by = Column(
        UUID,
        ForeignKey("users.id"),
        nullable=False,
    )

    telegram_chat_id = Column(
        UUID,
        ForeignKey("telegram_chats.chat_id"),
        nullable=True,
    )

    is_default_personal = Column(Boolean, nullable=False, default=False)

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

    creator = relationship("User", back_populates="spaces_created")
    telegram_chat = relationship("TelegramChat", back_populates="spaces")
    members = relationship("SpaceMember", back_populates="space")
    notes = relationship("Note", back_populates="space")
    events = relationship("Event", back_populates="space")

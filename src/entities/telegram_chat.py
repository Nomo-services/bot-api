from sqlalchemy import Column, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.core.database.base_class import Base
from src.entities.enums import TelegramChatTypeEnum


class TelegramChat(Base):
    __tablename__ = "telegram_chats"

    chat_id = Column(UUID, primary_key=True)  # Telegram chat_id
    type = Column(TelegramChatTypeEnum, nullable=False)
    title = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # relationships
    users = relationship("User", back_populates="telegram_chat")
    spaces = relationship("Space", back_populates="telegram_chat")

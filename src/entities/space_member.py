from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid import uuid7

from src.core.database.base_class import Base
from src.entities.enums import SpaceRoleEnum


class SpaceMember(Base):
    __tablename__ = "space_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)

    space_id = Column(
        UUID,
        ForeignKey("spaces.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    role = Column(SpaceRoleEnum, nullable=False, default="editor")
    notification_settings = Column(JSONB, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("space_id", "user_id", name="uq_space_member"),
    )

    # relationships
    space = relationship("Space", back_populates="members")
    user = relationship("User", back_populates="space_memberships")

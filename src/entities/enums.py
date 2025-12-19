from sqlalchemy import Enum

SpaceTypeEnum = Enum(
    "personal",
    "shared",
    "public",
    name="space_type",
)

SpaceRoleEnum = Enum(
    "owner",
    "editor",
    "viewer",
    name="space_role",
)

EventParticipationStatusEnum = Enum(
    "invited",
    "going",
    "maybe",
    "declined",
    name="event_participation_status",
)

EventParticipantRoleEnum = Enum(
    "organizer",
    "participant",
    name="event_participant_role",
)

ReminderStatusEnum = Enum(
    "pending",
    "sent",
    "canceled",
    "failed",
    name="reminder_status",
)

ReminderChannelEnum = Enum(
    "telegram",
    name="reminder_channel",
)

TelegramChatTypeEnum = Enum(
    "private",
    "group",
    "supergroup",
    "channel",
    name="telegram_chat_type",
)

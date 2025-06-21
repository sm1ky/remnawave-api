from datetime import datetime
from typing import Annotated, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, constr

from remnawave_api.enums import UserStatus
from remnawave_api.enums.users import TrafficLimitStrategy


class BulkUpdateUsersInboundsRequestDto(BaseModel):
    uuids: List[UUID]
    active_user_inbounds: List[UUID] = Field(serialization_alias="activeUserInbounds")

TagStr = Annotated[
    str,
    Field(min_length=1, max_length=16, pattern=r"^[A-Z0-9_]+$")
]

class UpdateUserFields(BaseModel):
    status: Optional[UserStatus] = None
    traffic_limit_bytes: Optional[int] = Field(
        None, serialization_alias="trafficLimitBytes", strict=True, ge=0
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None, serialization_alias="trafficLimitStrategy"
    )
    expire_at: Optional[datetime] = Field(None, serialization_alias="expireAt")
    description: Optional[str] = None
    tag: Optional[TagStr] = Field(
        None,
        description="Tag for user. Must be uppercase, alphanumeric, and can include underscores. Max length 16 characters."
    )
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None


class BulkAllUpdateUsersRequestDto(BaseModel):
    status: Optional[Literal["ACTIVE", "DISABLED", "LIMITED", "EXPIRED"]] = Field(
        "ACTIVE"
    )

    traffic_limit_bytes: Optional[int] = Field(
        None,
        serialization_alias="trafficLimitBytes",
        ge=0,
        description="Traffic limit in bytes. 0 - unlimited"
    )

    traffic_limit_strategy: Optional[Literal["NO_RESET", "DAY", "WEEK", "MONTH"]] = Field(
        None,
        serialization_alias="trafficLimitStrategy",
        description="Traffic limit reset strategy"
    )

    expire_at: Optional[datetime] = Field(
        None,
        serialization_alias="expireAt",
        description="Expiration date"
    )

    description: Optional[str] = None

    telegram_id: Optional[int] = Field(
        None,
        serialization_alias="telegramId"
    )

    email: Optional[str] = None

    tag: Optional[TagStr] = Field(
        None,
        description="Tag for user. Must be uppercase, alphanumeric, and can include underscores. Max length 16 characters."
    )


class BulkResponseDto(BaseModel):
    affected_rows: int = Field(alias="affectedRows")


class BulkAllResetTrafficUsersResponseDto(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class BulkAllUpdateUsersResponseDto(BaseModel):
    event_sent: bool = Field(alias="eventSent")

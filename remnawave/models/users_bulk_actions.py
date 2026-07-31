from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from remnawave.enums import UserStatus, TrafficLimitStrategy


# Type alias for tag validation
TagStr = Annotated[
    str,
    Field(min_length=1, max_length=16, pattern=r"^[A-Z0-9_]+$")
]


# Request DTOs
class BulkDeleteUsersByStatusRequestDto(BaseModel):
    """Request to delete users by status"""
    status: UserStatus = Field(default=UserStatus.ACTIVE)


class BulkDeleteUsersRequestDto(BaseModel):
    """Request to delete users by UUIDs"""
    user_ids: List[int] = Field(min_length=1, max_length=1000, serialization_alias="userIds")


class BulkRevokeUsersSubscriptionRequestDto(BaseModel):
    """Request to revoke users subscription"""
    user_ids: List[int] = Field(min_length=1, max_length=1000, serialization_alias="userIds")


class BulkResetTrafficUsersRequestDto(BaseModel):
    """Request to reset traffic for users"""
    user_ids: List[int] = Field(min_length=1, max_length=1000, serialization_alias="userIds")


class UpdateUserFields(BaseModel):
    """Fields to update for users"""
    status: Optional[UserStatus] = None
    traffic_limit_bytes: Optional[float] = Field(
        None,
        serialization_alias="trafficLimitBytes",
        ge=0,
        description="Traffic limit in bytes. 0 - unlimited"
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None, 
        serialization_alias="trafficLimitStrategy",
        description="Traffic limit reset strategy"
    )
    expire_at: Optional[datetime] = Field(
        None, 
        serialization_alias="expireAt",
        description="Expiration date: 2025-01-17T15:38:45.065Z"
    )
    description: Optional[str] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None
    tag: Optional[TagStr] = Field(
        None,
        description="Tag for user. Must be uppercase, alphanumeric, and can include underscores. Max length 16 characters."
    )
    hwid_device_limit: Optional[int] = Field(
        None, 
        serialization_alias="hwidDeviceLimit", 
        ge=0
    )
    external_squad_uuid: Optional[UUID] = Field(
        None,
        serialization_alias="externalSquadUuid",
        description="Optional. External squad UUID."
    )


class BulkUpdateUsersRequestDto(BaseModel):
    """Request to bulk update users"""
    user_ids: List[int] = Field(min_length=1, max_length=1000, serialization_alias="userIds")
    fields: UpdateUserFields


class BulkUpdateUsersSquadsRequestDto(BaseModel):
    """Request to update users internal squads"""
    user_ids: List[int] = Field(min_length=1, max_length=1000, serialization_alias="userIds")
    active_internal_squads: List[UUID] = Field(serialization_alias="activeInternalSquads")


class BulkExtendExpirationDateRequestDto(BaseModel):
    """Request to extend expiration date for selected users"""
    user_ids: List[int] = Field(min_length=1, max_length=1000, serialization_alias="userIds")
    extend_days: int = Field(
        serialization_alias="extendDays",
        ge=1,
        le=9999
    )


class BulkAllUpdateUsersRequestDto(BaseModel):
    """Request to update all users"""
    status: Optional[UserStatus] = Field(default=UserStatus.ACTIVE)
    traffic_limit_bytes: Optional[float] = Field(
        None,
        serialization_alias="trafficLimitBytes",
        ge=0,
        description="Traffic limit in bytes. 0 - unlimited"
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None,
        serialization_alias="trafficLimitStrategy",
        description="Traffic limit reset strategy"
    )
    expire_at: Optional[datetime] = Field(
        None,
        serialization_alias="expireAt",
        description="Expiration date: 2025-01-17T15:38:45.065Z"
    )
    description: Optional[str] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None
    tag: Optional[TagStr] = Field(
        None,
        description="Tag for user. Must be uppercase, alphanumeric, and can include underscores. Max length 16 characters."
    )
    hwid_device_limit: Optional[int] = Field(
        None, 
        serialization_alias="hwidDeviceLimit", 
        ge=0
    )


class BulkAllExtendExpirationDateRequestDto(BaseModel):
    """Request to extend expiration date for all users"""
    extend_days: int = Field(
        serialization_alias="extendDays",
        ge=1
    )


# Base Response DTOs (без обертки response)
class BulkResponseData(BaseModel):
    """Common bulk response with affected rows"""
    affected_rows: float = Field(alias="affectedRows")


class BulkEventResponseData(BaseModel):
    """Common bulk response with event sent flag"""
    event_sent: bool = Field(alias="eventSent")


# Response DTOs - наследуются от базовых
class BulkDeleteUsersByStatusResponseDto(BulkResponseData):
    """Response for bulk delete by status"""
    pass


class BulkDeleteUsersResponseDto(BulkResponseData):
    """Response for bulk delete users"""
    pass


class BulkRevokeUsersSubscriptionResponseDto(BulkResponseData):
    """Response for bulk revoke subscription"""
    pass


class BulkResetTrafficUsersResponseDto(BulkResponseData):
    """Response for bulk reset traffic"""
    pass


class BulkUpdateUsersResponseDto(BulkResponseData):
    """Response for bulk update users"""
    pass


class BulkUpdateUsersSquadsResponseDto(BulkResponseData):
    """Response for bulk update squads"""
    pass


class BulkExtendExpirationDateResponseDto(BulkResponseData):
    """Response for bulk extend expiration date"""
    pass


class BulkAllUpdateUsersResponseDto(BulkEventResponseData):
    """Response for bulk update all users"""
    pass


class BulkAllResetTrafficUsersResponseDto(BulkEventResponseData):
    """Response for bulk reset all users traffic"""
    pass


class BulkAllExtendExpirationDateResponseDto(BulkEventResponseData):
    """Response for bulk extend all users expiration date"""
    pass


# Legacy compatibility
BulkResponseDto = BulkResponseData
BulkUpdateUsersInternalSquadsRequestDto = BulkUpdateUsersSquadsRequestDto
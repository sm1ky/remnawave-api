from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    StringConstraints,
)

from remnawave_api.enums import TrafficLimitStrategy, UserStatus


class UserActiveInboundsDto(BaseModel):
    uuid: UUID
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None


class UserLastConnectedNodeDto(BaseModel):
    connected_at: datetime = Field(alias="connectedAt")
    node_name: str = Field(alias="nodeName")

class HappCrypto(BaseModel):
    cryptoLink: str

class CreateUserRequestDto(BaseModel):
    username: Annotated[
        str, StringConstraints(pattern=r"^[a-zA-Z0-9_-]+$", min_length=6, max_length=36)
    ]
    status: Optional[UserStatus] = None
    subscription_uuid: Optional[str] = Field(
        None, serialization_alias="subscriptionUuid"
    )
    short_uuid: Optional[str] = Field(None, serialization_alias="shortUuid")
    trojan_password: Annotated[
        Optional[str], StringConstraints(min_length=8, max_length=32)
    ] = Field(None, serialization_alias="trojanPassword")
    vless_uuid: Optional[str] = Field(None, serialization_alias="vlessUuid")
    ss_password: Annotated[
        Optional[str], StringConstraints(min_length=8, max_length=32)
    ] = Field(None, serialization_alias="ssPassword")
    traffic_limit_bytes: Optional[int] = Field(
        None, serialization_alias="trafficLimitBytes", strict=True, ge=0
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None, serialization_alias="trafficLimitStrategy"
    )
    active_user_inbounds: Optional[List[str]] = Field(
        None, serialization_alias="activeUserInbounds"
    )
    expire_at: datetime = Field(..., serialization_alias="expireAt")
    created_at: Optional[datetime] = Field(None, serialization_alias="createdAt")
    last_traffic_reset_at: Optional[datetime] = Field(
        None, serialization_alias="lastTrafficResetAt"
    )
    description: Optional[str] = None
    tag: Optional[str] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None
    hwidDeviceLimit: Optional[int] = Field(
        None, serialization_alias="hwidDeviceLimit", strict=True, ge=0
    )
    activate_all_inbounds: Optional[bool] = Field(
        None, serialization_alias="activateAllInbounds"
    )


class UpdateUserRequestDto(BaseModel):
    uuid: UUID
    status: Optional[UserStatus] = None
    traffic_limit_bytes: Optional[int] = Field(
        None, serialization_alias="trafficLimitBytes", strict=True, ge=0
    )
    traffic_limit_strategy: Optional[TrafficLimitStrategy] = Field(
        None, serialization_alias="trafficLimitStrategy"
    )
    active_user_inbounds: Optional[List[str]] = Field(
        None, serialization_alias="activeUserInbounds"
    )
    expire_at: Optional[datetime] = Field(None, serialization_alias="expireAt")
    last_traffic_reset_at: Optional[datetime] = Field(
        None, serialization_alias="lastTrafficResetAt"
    )
    description: Optional[str] = None
    tag: Optional[str] = None
    telegram_id: Optional[int] = Field(None, serialization_alias="telegramId")
    email: Optional[str] = None
    hwidDeviceLimit: Optional[int] = Field(
        None, serialization_alias="hwidDeviceLimit", strict=True, ge=0
    )


class UserResponseDto(BaseModel):
    uuid: UUID
    subscription_uuid: UUID = Field(alias="subscriptionUuid")
    short_uuid: str = Field(alias="shortUuid")
    username: str
    status: Optional[UserStatus] = None
    used_traffic_bytes: float = Field(alias="usedTrafficBytes")
    lifetime_used_traffic_bytes: float = Field(alias="lifetimeUsedTrafficBytes")
    traffic_limit_bytes: Optional[int] = Field(None, alias="trafficLimitBytes")
    traffic_limit_strategy: Optional[str] = Field(None, alias="trafficLimitStrategy")
    sub_last_user_agent: Optional[str] = Field(None, alias="subLastUserAgent")
    sub_last_opened_at: Optional[datetime] = Field(None, alias="subLastOpenedAt")
    expire_at: Optional[datetime] = Field(None, alias="expireAt")
    online_at: Optional[datetime] = Field(None, alias="onlineAt")
    sub_revoked_at: Optional[datetime] = Field(None, alias="subRevokedAt")
    last_traffic_reset_at: Optional[datetime] = Field(None, alias="lastTrafficResetAt")
    trojan_password: str = Field(alias="trojanPassword")
    vless_uuid: UUID = Field(alias="vlessUuid")
    ss_password: str = Field(alias="ssPassword")
    description: Optional[str] = None
    telegram_id: Optional[int] = Field(None, alias="telegramId")
    email: Optional[str] = None
    hwidDeviceLimit: Optional[int] = Field(
        None, serialization_alias="hwidDeviceLimit", strict=True, ge=0
    )
    active_user_inbounds: List[UserActiveInboundsDto] = Field(
        alias="activeUserInbounds"
    )
    subscription_url: str = Field(alias="subscriptionUrl")
    first_connected: Optional[datetime] = Field(None, alias="firstConnectedAt")
    last_trigger_threshold: Optional[int] = Field(
        None, alias="lastTriggeredThreshold"
    )
    last_connected_node: Optional[UserLastConnectedNodeDto] = Field(
        None, alias="lastConnectedNode"
    )
    happ: Optional[HappCrypto] = Field(None, alias="happ")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class EmailUserResponseDto(BaseModel):
    response: List[UserResponseDto]


class TelegramUserResponseDto(BaseModel):
    response: List[UserResponseDto]


class UsersResponseDto(BaseModel):
    users: List[UserResponseDto]
    total: float


class DeleteUserResponseDto(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")

class TagsResponseDto(BaseModel):
    tags: List[str]
    
class RevokeUserRequestDto(BaseModel):
    short_uuid: Optional[str] = Field(
        None,
        serialization_alias="shortUuid",
        description="Optional. If not provided, a new short UUID will be generated by Remnawave. Please note that it is strongly recommended to allow Remnawave to generate the short UUID.",
        min_length=6,
        max_length=48,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )
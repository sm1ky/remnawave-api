from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints


class SubscriptionSettingsResponseDto(BaseModel):
    uuid: UUID
    profile_title: str = Field(alias="profileTitle")
    support_link: str = Field(alias="supportLink")
    profile_update_interval: int = Field(
        alias="profileUpdateInterval", strict=True, ge=1
    )
    is_profile_webpage_url_enabled: bool = Field(alias="isProfileWebpageUrlEnabled")
    serve_json_at_base_subscription: bool = Field(alias="serveJsonAtBaseSubscription")
    add_username_to_base_subscription: bool = Field(
        alias="addUsernameToBaseSubscription"
    )
    happ_announce: Optional[str] = Field(None, alias="happAnnounce")
    happ_routing: Optional[str] = Field(None, alias="happRouting")
    expired_users_remarks: List[str] = Field(alias="expiredUsersRemarks")
    limited_users_remarks: List[str] = Field(alias="limitedUsersRemarks")
    disabled_users_remarks: List[str] = Field(alias="disabledUsersRemarks")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

class UpdateSubscriptionSettingsRequestDto(BaseModel):
    uuid: UUID
    profile_title: Optional[str] = Field(None, serialization_alias="profileTitle")
    support_link: Optional[str] = Field(None, serialization_alias="supportLink")
    profile_update_interval: Optional[int] = Field(
        None, serialization_alias="profileUpdateInterval"
    )
    is_profile_webpage_url_enabled: Optional[bool] = Field(
        None, serialization_alias="isProfileWebpageUrlEnabled"
    )
    serve_json_at_base_subscription: Optional[bool] = Field(
        None, serialization_alias="serveJsonAtBaseSubscription"
    )
    add_username_to_base_subscription: Optional[bool] = Field(
        None, serialization_alias="addUsernameToBaseSubscription"
    )
    is_show_custom_remarks: Optional[bool] = Field(
        None, serialization_alias="isShowCustomRemarks"
    )
    happ_announce: Annotated[Optional[str], StringConstraints(max_length=200)] = Field(
        None, serialization_alias="happAnnounce"
    )
    happ_routing: Optional[str] = Field(None, serialization_alias="happRouting")
    expired_users_remarks: Optional[List[str]] = Field(
        None, serialization_alias="expiredUsersRemarks"
    )
    limited_users_remarks: Optional[List[str]] = Field(
        None, serialization_alias="limitedUsersRemarks"
    )
    disabled_users_remarks: Optional[List[str]] = Field(
        None, serialization_alias="disabledUsersRemarks"
    )
    custom_response_headers: Optional[dict] = Field(
        None, serialization_alias="customResponseHeaders"
    )
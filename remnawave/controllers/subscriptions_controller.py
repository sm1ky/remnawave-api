from typing import Annotated

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.models.subscription import GetRawSubscriptionByShortUuidResponseDto
from remnawave.rapid import BaseController, get
from remnawave.models import (
    GetAllSubscriptionsResponseDto,
    GetSubscriptionByUsernameResponseDto,
    GetSubscriptionByShortUUIDResponseDto,
    GetSubscriptionByUUIDResponseDto,
    GetSubpageConfigByShortUuidRequestBodyDto,
    GetSubpageConfigByShortUuidResponseDto,
    GetConnectionKeysByUuidResponseDto,
)


class SubscriptionsController(BaseController):
    # Protected endpoints below
    @get("/subscriptions", response_class=GetAllSubscriptionsResponseDto)
    async def get_all_subscriptions(
        self,
        start: Annotated[
            int, Query(default=0, ge=0, description="Index to start pagination from")
        ],
        size: Annotated[
            int, Query(default=25, ge=1, description="Number of users per page")
        ],
    ) -> GetAllSubscriptionsResponseDto:
        """None"""
        ...

    @get("/subscriptions/by-username/{username}", response_class=GetSubscriptionByUsernameResponseDto)
    async def get_subscription_by_username(
        self,
        username: Annotated[str, Path(description="Username of the user")],
    ) -> GetSubscriptionByUsernameResponseDto:
        """None"""
        ...
        
    @get("/subscriptions/by-short-uuid/{shortUuid}", response_class=GetSubscriptionByShortUUIDResponseDto)
    async def get_subscription_by_short_uuid(
        self,
        short_uuid: Annotated[str, Path(description="Short UUID of the subscription", alias="shortUuid")],
    ) -> GetSubscriptionByShortUUIDResponseDto:
        """None"""
        ...
        
    @get("/subscriptions/by-id/{userId}", response_class=GetSubscriptionByUUIDResponseDto)
    async def get_subscription_by_id(
        self,
        user_id: Annotated[int, Path(description="Numeric id of the user", alias="userId")],
    ) -> GetSubscriptionByUUIDResponseDto:
        """Get subscription by numeric user id"""
        ...

    @get("/subscriptions/subpage-config/{shortUuid}", response_class=GetSubpageConfigByShortUuidResponseDto)
    async def get_subpage_config(
        self,
        short_uuid: Annotated[str, Path(description="Short UUID of the subscription", alias="shortUuid")],
        body: Annotated[GetSubpageConfigByShortUuidRequestBodyDto, PydanticBody()],
    ) -> GetSubpageConfigByShortUuidResponseDto:
        """Get subscription page config by short UUID"""
        ...

    @get("/subscriptions/by-short-uuid/{shortUuid}/raw", response_class=GetRawSubscriptionByShortUuidResponseDto)
    async def get_raw_subscription(
        self,
        short_uuid: Annotated[str, Path(description="Short UUID of the user", alias="shortUuid")],
        with_disabled_hosts: Annotated[str, Query(default="false", alias="withDisabledHosts", description="Include disabled hosts")] = "false",
    ) -> GetRawSubscriptionByShortUuidResponseDto:
        """None"""
        ...

    @get("/subscriptions/connection-keys/{userId}", response_class=GetConnectionKeysByUuidResponseDto)
    async def get_connection_keys_by_user_id(
        self,
        user_id: Annotated[int, Path(description="Numeric id of the user", alias="userId")],
    ) -> GetConnectionKeysByUuidResponseDto:
        """Get connection keys (base64 format) by uuid"""
        ...
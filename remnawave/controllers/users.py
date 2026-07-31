from typing import Annotated, Optional

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.enums import TrafficLimitStrategy, UserStatus
from remnawave.models import (
    CreateUserBodyDto,
    ExtendUserBodyDto,
    GetUsersResponseDto,
    GetUsersTagsResponseDto,
    GetUserAccessibleNodesResponseDto,
    GetUserSubscriptionRequestHistoryResponseDto,
    GetUsersStreamResponseDto,
    ResolveUserBodyDto,
    ResolveUserResponseDto,
    RevokeUserSubscriptionBodyDto,
    UpdateUserBodyDto,
    UserResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class UsersController(BaseController):
    @post("/users", response_class=UserResponseDto)
    async def create_user(
        self,
        body: Annotated[CreateUserBodyDto, PydanticBody()],
    ) -> UserResponseDto:
        """Create a new user"""
        ...

    @patch("/users", response_class=UserResponseDto)
    async def update_user(
        self,
        body: Annotated[UpdateUserBodyDto, PydanticBody()],
    ) -> UserResponseDto:
        """Update a user by numeric id"""
        ...

    @get("/users", response_class=GetUsersResponseDto)
    async def get_all_users(
        self,
        start: Annotated[Optional[int], Query(default=None, description="Offset for pagination")] = None,
        size: Annotated[Optional[int], Query(default=None, description="Page size (default 25, max 1000)")] = None,
    ) -> GetUsersResponseDto:
        """Get all users"""
        ...

    @get("/users/stream", response_class=GetUsersStreamResponseDto)
    async def get_users_stream(
        self,
        size: Annotated[Optional[int], Query(default=None, description="Page size, max 1000 (default 250)")] = None,
        cursor: Annotated[Optional[int], Query(default=None, description="Numeric cursor from the previous response (nextCursor)")] = None,
        status: Annotated[Optional[UserStatus], Query(default=None, description="Filter by user status")] = None,
        traffic_limit_strategy: Annotated[
            Optional[TrafficLimitStrategy],
            Query(default=None, alias="trafficLimitStrategy", description="Filter by traffic limit strategy"),
        ] = None,
        telegram_id: Annotated[Optional[str], Query(default=None, alias="telegramId", description="Filter by Telegram id")] = None,
        email: Annotated[Optional[str], Query(default=None, description="Filter by email")] = None,
        tag: Annotated[Optional[str], Query(default=None, description="Filter by tag")] = None,
        external_squad_uuid: Annotated[
            Optional[str],
            Query(default=None, alias="externalSquadUuid", description="Filter by external squad uuid"),
        ] = None,
    ) -> GetUsersStreamResponseDto:
        """Get all users using cursor-based (keyset) pagination"""
        ...

    @delete("/users/{userId}", response_class=None)
    async def delete_user(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
    ) -> None:
        """Delete user (204 No Content)"""
        ...

    @post("/users/{userId}/actions/extend", response_class=UserResponseDto)
    async def extend_user(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
        body: Annotated[ExtendUserBodyDto, PydanticBody()],
    ) -> UserResponseDto:
        """Extend a user's expiration date"""
        ...

    @post("/users/{userId}/actions/revoke", response_class=UserResponseDto)
    async def revoke_user_subscription(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
        body: Annotated[Optional[RevokeUserSubscriptionBodyDto], PydanticBody()] = None,
    ) -> UserResponseDto:
        """Revoke User Subscription"""
        ...

    @post("/users/{userId}/actions/disable", response_class=UserResponseDto)
    async def disable_user(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
    ) -> UserResponseDto:
        """Disable User"""
        ...

    @post("/users/{userId}/actions/enable", response_class=UserResponseDto)
    async def enable_user(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
    ) -> UserResponseDto:
        """Enable User"""
        ...

    @post("/users/{userId}/actions/reset-traffic", response_class=UserResponseDto)
    async def reset_user_traffic(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
    ) -> UserResponseDto:
        """Reset User Traffic"""
        ...

    @get("/users/tags", response_class=GetUsersTagsResponseDto)
    async def get_all_tags(
        self,
    ) -> GetUsersTagsResponseDto:
        """Get all existing user tags"""
        ...

    @get("/users/{userId}", response_class=UserResponseDto)
    async def get_user_by_id(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
    ) -> UserResponseDto:
        """Get user by numeric id"""
        ...

    @get("/users/{userId}/accessible-nodes", response_class=GetUserAccessibleNodesResponseDto)
    async def get_user_accessible_nodes(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
    ) -> GetUserAccessibleNodesResponseDto:
        """Get user accessible nodes"""
        ...

    @get(
        "/users/{userId}/subscription-request-history",
        response_class=GetUserSubscriptionRequestHistoryResponseDto,
    )
    async def get_user_subscription_request_history(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
    ) -> GetUserSubscriptionRequestHistoryResponseDto:
        """Get user subscription request history, recent 24 records"""
        ...

    @get("/users/by-short-uuid/{shortUuid}", response_class=UserResponseDto)
    async def get_user_by_short_uuid(
        self,
        short_uuid: Annotated[str, Path(description="Short UUID of the user", alias="shortUuid")],
    ) -> UserResponseDto:
        """Get user by Short UUID"""
        ...

    @get("/users/by-username/{username}", response_class=UserResponseDto)
    async def get_user_by_username(
        self,
        username: Annotated[str, Path(description="Username of the user")],
    ) -> UserResponseDto:
        """Get user by username"""
        ...

    @post("/users/resolve", response_class=ResolveUserResponseDto)
    async def resolve_user(
        self,
        body: Annotated[ResolveUserBodyDto, PydanticBody()],
    ) -> ResolveUserResponseDto:
        """Resolve user by any identifier (id, shortUuid, username)"""
        ...

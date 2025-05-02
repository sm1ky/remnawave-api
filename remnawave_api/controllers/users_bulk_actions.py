from typing import Annotated, List
from uuid import UUID

from rapid_api_client.annotations import PydanticBody

from remnawave_api.enums import UserStatus
from remnawave_api.models import (
    BulkAllResetTrafficUsersResponseDto,
    BulkAllUpdateUsersRequestDto,
    BulkAllUpdateUsersResponseDto,
    BulkResponseDto,
    BulkUpdateUsersInboundsRequestDto,
    UpdateUserFields,
)
from remnawave_api.rapid import AttributeBody, BaseController, patch, post


class UsersBulkActionsController(BaseController):
    @post(
        "/users/bulk/delete-by-status",
        response_class=BulkResponseDto,
    )
    async def bulk_delete_users_by_status(
        self, status: Annotated[UserStatus, AttributeBody()]
    ) -> BulkResponseDto:
        """Bulk Delete Users By Status"""
        ...

    @post("/users/bulk/delete", response_class=BulkResponseDto)
    async def bulk_delete_users(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> BulkResponseDto:
        """Bulk Delete Users By UUIDs"""
        ...

    @post(
        "/users/bulk/revoke-subscription",
        response_class=BulkResponseDto,
    )
    async def bulk_revoke_users_subscription(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> BulkResponseDto:
        """Bulk Revoke Users Subscription"""
        ...

    @post("/users/bulk/reset-traffic", response_class=BulkResponseDto)
    async def bulk_reset_user_traffic(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> BulkResponseDto:
        """Bulk Reset User Traffic"""
        ...

    @post("/users/bulk/update", response_class=BulkResponseDto)
    async def bulk_update_users(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
        fields: Annotated[UpdateUserFields, AttributeBody()],
    ) -> BulkResponseDto:
        """Bulk Update Users"""
        ...

    @post("/users/bulk/update-inbounds", response_class=BulkResponseDto)
    async def bulk_update_users_inbounds(
        self,
        body: Annotated[BulkUpdateUsersInboundsRequestDto, PydanticBody()],
    ) -> BulkResponseDto:
        """Bulk Update Users Inbounds"""
        ...

    @post("/users/bulk/all/update", response_class=BulkAllUpdateUsersResponseDto)
    async def bulk_update_all_users(
        self,
        body: Annotated[BulkAllUpdateUsersRequestDto, PydanticBody()],
    ) -> BulkAllUpdateUsersResponseDto:
        """Bulk Update All Users"""
        ...

    @post(
        "/users/bulk/all/reset-traffic",
        response_class=BulkAllResetTrafficUsersResponseDto,
    )
    async def bulk_all_reset_user_traffic(
        self,
    ) -> BulkAllResetTrafficUsersResponseDto:
        """Bulk Reset All Users Traffic"""
        ...

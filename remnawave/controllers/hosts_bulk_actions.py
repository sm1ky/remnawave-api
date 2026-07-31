from typing import Annotated, List
from uuid import UUID

from rapid_api_client import PydanticBody

from remnawave.models import (
    BulkDeleteHostsResponseDto,
    BulkDisableHostsResponseDto,
    BulkEnableHostsResponseDto,
    UpdateManyHostsRequestDto,
    UpdateManyHostsResponseDto,
)
from remnawave.rapid import AttributeBody, BaseController, patch, post


class HostsBulkActionsController(BaseController):
    @post("/hosts/bulk/delete", response_class=None)
    async def delete_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> BulkDeleteHostsResponseDto:
        """Delete many hosts"""
        ...

    @post("/hosts/bulk/disable", response_class=None)
    async def disable_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> BulkDisableHostsResponseDto:
        """Disable many hosts"""
        ...

    @post("/hosts/bulk/enable", response_class=None)
    async def enable_hosts(
        self,
        uuids: Annotated[List[UUID], AttributeBody()],
    ) -> BulkEnableHostsResponseDto:
        """Enable many hosts"""
        ...

    @patch("/hosts/bulk/update", response_class=None)
    async def update_hosts(
        self,
        body: Annotated[UpdateManyHostsRequestDto, PydanticBody()],
    ) -> UpdateManyHostsResponseDto:
        """Update many hosts"""
        ...

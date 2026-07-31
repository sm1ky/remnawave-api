from typing import Annotated, List

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateHostRequestDto,
    CreateHostResponseDto,
    DeleteHostResponseDto,
    GetAllHostsResponseDto,
    GetOneHostResponseDto,
    ReorderHostRequestDto,
    ReorderHostResponseDto,
    UpdateHostRequestDto,
    UpdateHostResponseDto,
    GetAllHostTagsResponseDto,
)
from remnawave.rapid import AttributeBody, BaseController, delete, get, post, patch


class HostsController(BaseController):
    @post("/hosts", response_class=CreateHostResponseDto)
    async def create_host(
        self,
        body: Annotated[CreateHostRequestDto, PydanticBody()],
    ) -> CreateHostResponseDto:
        """Create Host"""
        ...

    @patch("/hosts", response_class=UpdateHostResponseDto)
    async def update_host(
        self,
        body: Annotated[UpdateHostRequestDto, PydanticBody()],
    ) -> UpdateHostResponseDto:
        """Update Host"""
        ...

    @get("/hosts", response_class=GetAllHostsResponseDto)
    async def get_all_hosts(
        self,
    ) -> GetAllHostsResponseDto:
        """Get All Hosts"""
        ...

    @get("/hosts/tags", response_class=GetAllHostTagsResponseDto)
    async def get_hosts_tags(
        self,
    ) -> GetAllHostTagsResponseDto:
        """Get Hosts Tags"""
        ...

    @delete("/hosts/{uuid}", response_class=None)
    async def delete_host(
        self,
        uuid: Annotated[str, Path(description="UUID of the host")],
    ) -> DeleteHostResponseDto:
        """Delete Host"""
        ...

    @get("/hosts/{uuid}", response_class=GetOneHostResponseDto)
    async def get_one_host(
        self,
        uuid: Annotated[str, Path(description="UUID of the host")],
    ) -> GetOneHostResponseDto:
        """Get One Host"""
        ...

    @post("/hosts/actions/reorder", response_class=ReorderHostResponseDto)
    async def reorder_hosts(
        self,
        body: Annotated[ReorderHostRequestDto, PydanticBody()],
    ) -> ReorderHostResponseDto:
        """Reorder Hosts"""
        ...

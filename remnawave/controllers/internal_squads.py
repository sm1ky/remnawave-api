from typing import Annotated, Optional

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    AddUsersToInternalSquadRequestDto,
    AddUsersToInternalSquadResponseDto,
    CreateInternalSquadRequestDto,
    CreateInternalSquadResponseDto,
    DeleteInternalSquadResponseDto,
    DeleteUsersFromInternalSquadRequestDto,
    DeleteUsersFromInternalSquadResponseDto,
    GetAllInternalSquadsResponseDto,
    GetInternalSquadByUuidResponseDto,
    ReorderInternalSquadsRequestDto,
    ReorderInternalSquadsResponseDto,
    UpdateInternalSquadRequestDto,
    UpdateInternalSquadResponseDto,
    GetInternalSquadAccessibleNodesResponseDto,
    GetInternalSquadsTagsResponseDto,
    SetInternalSquadsTagsRequestDto,
    SetInternalSquadsTagsResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


from remnawave.models.internal_squads import (
    AddManyUsersToInternalSquadBodyDto,
    DeleteManyUsersFromInternalSquadBodyDto,
)
from remnawave.models.bandwidthstats import GetInternalSquadUsageResponseDto


class InternalSquadsController(BaseController):
    @get("/internal-squads", response_class=GetAllInternalSquadsResponseDto)
    async def get_internal_squads(self) -> GetAllInternalSquadsResponseDto:
        """Get all internal squads"""
        ...

    @post("/internal-squads", response_class=CreateInternalSquadResponseDto)
    async def create_internal_squad(
        self,
        body: Annotated[CreateInternalSquadRequestDto, PydanticBody()],
    ) -> CreateInternalSquadResponseDto:
        """Create internal squad"""
        ...

    @patch("/internal-squads", response_class=UpdateInternalSquadResponseDto)
    async def update_internal_squad(
        self,
        body: Annotated[UpdateInternalSquadRequestDto, PydanticBody()],
    ) -> UpdateInternalSquadResponseDto:
        """Update internal squad"""
        ...

    @get("/internal-squads/{uuid}", response_class=GetInternalSquadByUuidResponseDto)
    async def get_internal_squad_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> GetInternalSquadByUuidResponseDto:
        """Get internal squad by uuid"""
        ...

    @delete("/internal-squads/{uuid}", response_class=None)
    async def delete_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> DeleteInternalSquadResponseDto:
        """Delete internal squad"""
        ...

    @post(
        "/internal-squads/{uuid}/bulk-actions/add-users",
        response_class=None,
    )
    async def add_users_to_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> AddUsersToInternalSquadResponseDto:
        """Add users to internal squad"""
        ...

    @delete(
        "/internal-squads/{uuid}/bulk-actions/remove-users",
        response_class=None,
    )
    async def remove_users_from_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> DeleteUsersFromInternalSquadResponseDto:
        """Delete users from internal squad"""
        ...

    @get(
        "/internal-squads/{uuid}/accessible-nodes",
        response_class=GetInternalSquadAccessibleNodesResponseDto,
    )
    async def get_accessible_nodes(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
    ) -> GetInternalSquadAccessibleNodesResponseDto:
        """Get accessible nodes for internal squad"""
        ...

    @post("/internal-squads/actions/reorder", response_class=ReorderInternalSquadsResponseDto)
    async def reorder_internal_squads(
        self,
        body: Annotated[ReorderInternalSquadsRequestDto, PydanticBody()],
    ) -> ReorderInternalSquadsResponseDto:
        """Reorder internal squads"""
        ...

    @post("/internal-squads/{uuid}/bulk-actions/add-many-users", response_class=None)
    async def add_many_users_to_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
        body: Annotated[AddManyUsersToInternalSquadBodyDto, PydanticBody()],
    ) -> None:
        """Add a specific list of users to an internal squad (202 Accepted)"""
        ...

    @delete("/internal-squads/{uuid}/bulk-actions/remove-many-users", response_class=None)
    async def remove_many_users_from_internal_squad(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
        body: Annotated[DeleteManyUsersFromInternalSquadBodyDto, PydanticBody()],
    ) -> None:
        """Remove a specific list of users from an internal squad (202 Accepted)"""
        ...

    @get("/internal-squads/{uuid}/usage", response_class=GetInternalSquadUsageResponseDto)
    async def get_internal_squad_usage(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
        limit: Annotated[Optional[int], Query(default=None, description="Page size (default 250)")] = None,
        cursor: Annotated[Optional[int], Query(default=None, description="Keyset cursor")] = None,
        min_total_bytes: Annotated[Optional[int], Query(default=None, alias="minTotalBytes")] = None,
    ) -> GetInternalSquadUsageResponseDto:
        """Per-user traffic usage on the internal squad nodes."""
        ...

    @get("/internal-squads/tags", response_class=GetInternalSquadsTagsResponseDto)
    async def get_internal_squads_tags(self) -> GetInternalSquadsTagsResponseDto:
        """Get tags of Internal Squads"""
        ...

    @patch("/internal-squads/tags", response_class=SetInternalSquadsTagsResponseDto)
    async def set_internal_squad_tags(
        self,
        body: Annotated[SetInternalSquadsTagsRequestDto, PydanticBody()],
    ) -> SetInternalSquadsTagsResponseDto:
        """Set tags of Internal Squad"""
        ...

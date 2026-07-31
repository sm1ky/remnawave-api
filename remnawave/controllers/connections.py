from typing import Annotated

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    DropConnectionsRequestDto,
    FetchIpsResponseDto,
    FetchIpsResultResponseDto,
    FetchUsersIpsResponseDto,
    FetchUsersIpsResultResponseDto,
)
from remnawave.rapid import BaseController, get, post


class ConnectionsController(BaseController):
    """Connections module (Remnawave API v3.0.0, formerly ``ip-control``)."""

    @post("/connections/by-user/{userId}", response_class=FetchIpsResponseDto)
    async def fetch_connections_by_user(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
    ) -> FetchIpsResponseDto:
        """Start a background job to fetch the IPs used by a user (returns a jobId)."""
        ...

    @get("/connections/by-user/{jobId}", response_class=FetchIpsResultResponseDto)
    async def get_connections_by_user(
        self,
        job_id: Annotated[str, Path(alias="jobId", description="Job id returned by fetch_connections_by_user")],
    ) -> FetchIpsResultResponseDto:
        """Get the result of a by-user connections job."""
        ...

    @post("/connections/by-node/{nodeUuid}", response_class=FetchUsersIpsResponseDto)
    async def fetch_connections_by_node(
        self,
        node_uuid: Annotated[str, Path(alias="nodeUuid", description="UUID of the node")],
    ) -> FetchUsersIpsResponseDto:
        """Start a background job to fetch the IPs of all users on a node (returns a jobId)."""
        ...

    @get("/connections/by-node/{jobId}", response_class=FetchUsersIpsResultResponseDto)
    async def get_connections_by_node(
        self,
        job_id: Annotated[str, Path(alias="jobId", description="Job id returned by fetch_connections_by_node")],
    ) -> FetchUsersIpsResultResponseDto:
        """Get the result of a by-node connections job."""
        ...

    @post("/connections/drop", response_class=None)
    async def drop_connections(
        self,
        body: Annotated[DropConnectionsRequestDto, PydanticBody()],
    ) -> None:
        """Drop active connections by user ids or IP addresses (202 Accepted)."""
        ...

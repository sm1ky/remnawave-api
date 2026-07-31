from typing import Annotated, Optional

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.models.bandwidthstats import (
    FetchNodesUsageBodyDto,
    FetchNodesUsageResponseDto,
    GetInternalSquadUsageResponseDto,
    GetInternalSquadUserUsageResponseDto,
    GetStatsNodesUsageResponseDto,
    GetStatsNodeUsersUsageResponseDto,
    GetStatsNodesUsersUsageRequestDto,
    GetStatsNodesUsersUsageResponseDto,
    GetStatsUserUsageResponseDto,
)
from remnawave.rapid import BaseController, get, post


class BandWidthStatsController(BaseController):
    @get("/bandwidth-stats/nodes", response_class=GetStatsNodesUsageResponseDto)
    async def get_stats_nodes_usage(
        self,
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        top_nodes_limit: Annotated[Optional[int], Query(default=None, alias="topNodesLimit", description="Limit of top nodes (default 20)")] = None,
    ) -> GetStatsNodesUsageResponseDto:
        """Get Nodes Usage by Range"""
        ...

    @get("/bandwidth-stats/nodes/{uuid}/users", response_class=GetStatsNodeUsersUsageResponseDto)
    async def get_stats_node_users_usage(
        self,
        uuid: Annotated[str, Path(description="UUID of the node")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        top_users_limit: Annotated[Optional[int], Query(default=None, alias="topUsersLimit", description="Limit of top users (default 100)")] = None,
    ) -> GetStatsNodeUsersUsageResponseDto:
        """Get Node Users Usage by Node UUID"""
        ...

    @post("/bandwidth-stats/nodes/users", response_class=GetStatsNodesUsersUsageResponseDto)
    async def get_stats_nodes_users_usage(
        self,
        body: Annotated[GetStatsNodesUsersUsageRequestDto, PydanticBody()],
        start: Annotated[str, Query(description="Start date (YYYY-MM-DD)")],
        end: Annotated[str, Query(description="End date (YYYY-MM-DD)")],
        top_users_limit: Annotated[Optional[int], Query(default=None, alias="topUsersLimit", description="Limit of top users (default 100)")] = None,
    ) -> GetStatsNodesUsersUsageResponseDto:
        """Get Nodes Users Usage by Nodes UUIDs"""
        ...

    @post("/bandwidth-stats/nodes/usage", response_class=FetchNodesUsageResponseDto)
    async def fetch_nodes_usage(
        self,
        body: Annotated[FetchNodesUsageBodyDto, PydanticBody()],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        min_total_bytes: Annotated[Optional[int], Query(default=None, alias="minTotalBytes", description="Minimum total bytes filter")] = None,
    ) -> FetchNodesUsageResponseDto:
        """Get users whose total usage on the given nodes over the period is >= minTotalBytes"""
        ...

    @get("/bandwidth-stats/users/{userId}", response_class=GetStatsUserUsageResponseDto)
    async def get_stats_user_usage(
        self,
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
        top_nodes_limit: Annotated[Optional[int], Query(default=None, alias="topNodesLimit", description="Limit of top nodes (default 20)")] = None,
    ) -> GetStatsUserUsageResponseDto:
        """Get User Usage by Range"""
        ...

    @get("/bandwidth-stats/internal-squads/{uuid}/usage", response_class=GetInternalSquadUsageResponseDto)
    async def get_internal_squad_usage(
        self,
        uuid: Annotated[str, Path(description="UUID of the internal squad")],
        limit: Annotated[Optional[int], Query(default=None, description="Page size (default 250)")] = None,
        cursor: Annotated[Optional[int], Query(default=None, description="Keyset cursor")] = None,
        min_total_bytes: Annotated[Optional[int], Query(default=None, alias="minTotalBytes", description="Minimum total bytes filter")] = None,
    ) -> GetInternalSquadUsageResponseDto:
        """Per-user traffic usage on the internal squad nodes (cursor-paginated)."""
        ...

    @get(
        "/bandwidth-stats/internal-squads/{squadUuid}/users/{userId}/usage",
        response_class=GetInternalSquadUserUsageResponseDto,
    )
    async def get_internal_squad_user_usage(
        self,
        squad_uuid: Annotated[str, Path(alias="squadUuid", description="UUID of the internal squad")],
        user_id: Annotated[int, Path(alias="userId", description="Numeric id of the user")],
        start: Annotated[str, Query(description="Start date")],
        end: Annotated[str, Query(description="End date")],
    ) -> GetInternalSquadUserUsageResponseDto:
        """Daily (zero-filled) usage of a single user on the internal squad nodes."""
        ...

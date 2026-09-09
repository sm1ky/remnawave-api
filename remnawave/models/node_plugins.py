from datetime import datetime
from typing import Any, Annotated, Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from remnawave.models.tags import GetTagsResponseDto, SetTagsRequestDto, SetTagsResponseDto


class TorrentBlockerUserDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str
    uuid: Optional[UUID] = None


class TorrentBlockerNodeDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class TorrentBlockerActionReportDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    blocked: bool
    ip: str
    block_duration: float = Field(alias="blockDuration")
    will_unblock_at: datetime = Field(alias="willUnblockAt")
    user_id: str = Field(alias="userId")
    processed_at: datetime = Field(alias="processedAt")


class TorrentBlockerXrayReportDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: Optional[str] = None
    level: Optional[float] = None
    protocol: Optional[str] = None
    network: str
    source: Optional[str] = None
    destination: str
    route_target: Optional[str] = Field(default=None, alias="routeTarget")
    original_target: Optional[str] = Field(default=None, alias="originalTarget")
    inbound_tag: Optional[str] = Field(default=None, alias="inboundTag")
    inbound_name: Optional[str] = Field(default=None, alias="inboundName")
    inbound_local: Optional[str] = Field(default=None, alias="inboundLocal")
    outbound_tag: Optional[str] = Field(default=None, alias="outboundTag")
    ts: float


class TorrentBlockerReportPayloadDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    action_report: TorrentBlockerActionReportDto = Field(alias="actionReport")
    xray_report: TorrentBlockerXrayReportDto = Field(alias="xrayReport")


class TorrentBlockerReportRecordDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: float
    user_id: float = Field(alias="userId")
    node_id: float = Field(alias="nodeId")
    user: TorrentBlockerUserDto
    node: TorrentBlockerNodeDto
    report: TorrentBlockerReportPayloadDto
    created_at: datetime = Field(alias="createdAt")


class TorrentBlockerReportsData(BaseModel):
    records: List[TorrentBlockerReportRecordDto]
    total: float


class GetTorrentBlockerReportsResponseDto(TorrentBlockerReportsData):
    pass


class TruncateTorrentBlockerReportsResponseDto(TorrentBlockerReportsData):
    pass


class TorrentBlockerStatsDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    distinct_nodes: float = Field(alias="distinctNodes")
    distinct_users: float = Field(alias="distinctUsers")
    total_reports: float = Field(alias="totalReports")
    reports_last_24_hours: float = Field(alias="reportsLast24Hours")


class TorrentBlockerTopUserDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    color: str
    username: str
    total: float
    user_id: Optional[int] = Field(default=None, alias="userId")
    uuid: Optional[UUID] = None


class TorrentBlockerTopNodeDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    country_code: str = Field(alias="countryCode")
    color: str
    name: str
    total: float


class GetTorrentBlockerReportsStatsResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    stats: TorrentBlockerStatsDto
    top_users: List[TorrentBlockerTopUserDto] = Field(alias="topUsers")
    top_nodes: List[TorrentBlockerTopNodeDto] = Field(alias="topNodes")


class NodePluginDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    name: str
    tags: List[str] = Field(default_factory=list)
    plugin_config: Any | None = Field(alias="pluginConfig")


class GetNodePluginsResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total: float
    node_plugins: List[NodePluginDto] = Field(alias="nodePlugins")


class GetNodePluginResponseDto(NodePluginDto):
    pass


class UpdateNodePluginRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: Optional[
        Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]
    ] = None
    plugin_config: Optional[Any] = Field(default=None, alias="pluginConfig")


class UpdateNodePluginResponseDto(NodePluginDto):
    pass


class DeleteNodePluginResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    is_deleted: bool = Field(alias="isDeleted")


class CreateNodePluginRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]


class CreateNodePluginResponseDto(NodePluginDto):
    pass


class ReorderNodePluginItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    view_position: int = Field(alias="viewPosition")
    uuid: UUID


class ReorderNodePluginsRequestDto(BaseModel):
    items: List[ReorderNodePluginItem]


class ReorderNodePluginsResponseDto(GetNodePluginsResponseDto):
    pass


class CloneNodePluginRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    clone_from_uuid: UUID = Field(alias="cloneFromUuid")


class CloneNodePluginResponseDto(NodePluginDto):
    pass


class BlockIpItemDto(BaseModel):
    ip: str
    timeout: float


class BlockIpsCommandDto(BaseModel):
    command: Literal["blockIps"]
    ips: List[BlockIpItemDto]


class UnblockIpsCommandDto(BaseModel):
    command: Literal["unblockIps"]
    ips: List[str]


class RecreateTablesCommandDto(BaseModel):
    command: Literal["recreateTables"]


PluginCommandDto = Union[BlockIpsCommandDto, UnblockIpsCommandDto, RecreateTablesCommandDto]


class TargetAllNodesDto(BaseModel):
    target: Literal["allNodes"]


class TargetSpecificNodesDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    target: Literal["specificNodes"]
    node_uuids: List[UUID] = Field(alias="nodeUuids")


PluginTargetNodesDto = Union[TargetAllNodesDto, TargetSpecificNodesDto]


class PluginExecutorRequestDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    command: PluginCommandDto
    target_nodes: PluginTargetNodesDto = Field(alias="targetNodes")


class PluginExecutorResponseDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_sent: bool = Field(alias="eventSent")


# ─────────────────────────────────────────────────────────────────────────────
# Sync (Remnawave API v3.4.0+)
# ─────────────────────────────────────────────────────────────────────────────

class SyncNodePluginRequestDto(BaseModel):
    """Request body for ``POST /api/node-plugins/actions/sync``."""

    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID


# ─────────────────────────────────────────────────────────────────────────────
# Shared lists (Remnawave API v3.4.0+)
# ─────────────────────────────────────────────────────────────────────────────

# Shared list names support "folders" but, unlike snippets, no spaces.
SharedListName = Annotated[
    str,
    StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_-]+(\/[A-Za-z0-9_-]+)*$"),
]


class SharedListPreviewDto(BaseModel):
    """Shared list without its items — name, type and item count only."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    type: str
    items_count: float = Field(alias="itemsCount")


class GetSharedListsResponseDto(BaseModel):
    """Response for ``GET /api/node-plugins/shared-lists``."""

    model_config = ConfigDict(populate_by_name=True)

    total: float
    shared_lists: List[SharedListPreviewDto] = Field(alias="sharedLists")


class SharedListDto(BaseModel):
    """A shared list together with its full config."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    config: Dict[str, Any] = Field(default_factory=dict)


class GetSharedListResponseDto(SharedListDto):
    """Response for ``GET /api/node-plugins/shared-lists/by-name``."""

    pass


class CreateSharedListRequestDto(BaseModel):
    """Request body for ``POST /api/node-plugins/shared-lists``."""

    model_config = ConfigDict(populate_by_name=True)

    name: SharedListName
    config: Dict[str, Any]


class CreateSharedListResponseDto(SharedListDto):
    """Response for ``POST /api/node-plugins/shared-lists``."""

    pass


class UpdateSharedListRequestDto(BaseModel):
    """Request body for ``PATCH /api/node-plugins/shared-lists``."""

    model_config = ConfigDict(populate_by_name=True)

    name: SharedListName
    config: Dict[str, Any]


class UpdateSharedListResponseDto(SharedListDto):
    """Response for ``PATCH /api/node-plugins/shared-lists``."""

    pass


class DeleteSharedListRequestDto(BaseModel):
    """Request body for ``DELETE /api/node-plugins/shared-lists``."""

    model_config = ConfigDict(populate_by_name=True)

    name: SharedListName


class DeleteSharedListResponseDto(BaseModel):
    """Response for ``DELETE /api/node-plugins/shared-lists`` (204 No Content)."""

    model_config = ConfigDict(populate_by_name=True)

    is_deleted: bool = Field(alias="isDeleted")


class SyncSharedListRequestDto(BaseModel):
    """Request body for ``POST /api/node-plugins/shared-lists/actions/sync``."""

    model_config = ConfigDict(populate_by_name=True)

    name: SharedListName


# ─────────────────────────────────────────────────────────────────────────────
# Tags (Remnawave API v3.4.0+)
# ─────────────────────────────────────────────────────────────────────────────

class GetNodePluginsTagsResponseDto(GetTagsResponseDto):
    """Response for ``GET /api/node-plugins/tags``."""

    pass


class SetNodePluginsTagsRequestDto(SetTagsRequestDto):
    """Request body for ``PATCH /api/node-plugins/tags``."""

    pass


class SetNodePluginsTagsResponseDto(SetTagsResponseDto):
    """Response for ``PATCH /api/node-plugins/tags``."""

    pass

from typing import Annotated, Optional

from rapid_api_client import Path, PydanticBody, Query


from remnawave.models import (
    CloneNodePluginRequestDto,
    CloneNodePluginResponseDto,
    CreateNodePluginRequestDto,
    CreateNodePluginResponseDto,
    CreateSharedListRequestDto,
    CreateSharedListResponseDto,
    DeleteNodePluginResponseDto,
    DeleteSharedListRequestDto,
    DeleteSharedListResponseDto,
    GetNodePluginResponseDto,
    GetNodePluginsResponseDto,
    GetNodePluginsTagsResponseDto,
    GetSharedListResponseDto,
    GetSharedListsResponseDto,
    GetTorrentBlockerReportsResponseDto,
    GetTorrentBlockerReportsStatsResponseDto,
    PluginExecutorRequestDto,
    PluginExecutorResponseDto,
    ReorderNodePluginsRequestDto,
    ReorderNodePluginsResponseDto,
    SetNodePluginsTagsRequestDto,
    SetNodePluginsTagsResponseDto,
    SyncNodePluginRequestDto,
    SyncSharedListRequestDto,
    TruncateTorrentBlockerReportsResponseDto,
    UpdateNodePluginRequestDto,
    UpdateNodePluginResponseDto,
    UpdateSharedListRequestDto,
    UpdateSharedListResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class NodePluginsController(BaseController):
    @get("/node-plugins/torrent-blocker", response_class=GetTorrentBlockerReportsResponseDto)
    async def get_torrent_blocker_reports(
        self,
        size: Annotated[Optional[int], Query(default=None, ge=1, description="Page size")] = None,
        start: Annotated[Optional[int], Query(default=None, ge=0, description="Offset")] = None,
    ) -> GetTorrentBlockerReportsResponseDto:
        """Get Torrent Blocker Reports"""
        ...

    @get("/node-plugins/torrent-blocker/stats", response_class=GetTorrentBlockerReportsStatsResponseDto)
    async def get_torrent_blocker_reports_stats(
        self,
    ) -> GetTorrentBlockerReportsStatsResponseDto:
        """Get Torrent Blocker Reports Stats"""
        ...

    @delete("/node-plugins/torrent-blocker/truncate", response_class=None)
    async def truncate_torrent_blocker_reports(
        self,
    ) -> TruncateTorrentBlockerReportsResponseDto:
        """Truncate Torrent Blocker Reports"""
        ...

    @get("/node-plugins", response_class=GetNodePluginsResponseDto)
    async def get_all_node_plugins(self) -> GetNodePluginsResponseDto:
        """Get all Node Plugins"""
        ...

    @patch("/node-plugins", response_class=UpdateNodePluginResponseDto)
    async def update_node_plugin(
        self,
        body: Annotated[UpdateNodePluginRequestDto, PydanticBody()],
    ) -> UpdateNodePluginResponseDto:
        """Update Node Plugin"""
        ...

    @post("/node-plugins", response_class=CreateNodePluginResponseDto)
    async def create_node_plugin(
        self,
        body: Annotated[CreateNodePluginRequestDto, PydanticBody()],
    ) -> CreateNodePluginResponseDto:
        """Create Node Plugin"""
        ...

    @get("/node-plugins/{uuid}", response_class=GetNodePluginResponseDto)
    async def get_node_plugin_by_uuid(
        self,
        uuid: Annotated[str, Path(description="Node plugin UUID")],
    ) -> GetNodePluginResponseDto:
        """Get Node Plugin by uuid"""
        ...

    @delete("/node-plugins/{uuid}", response_class=None)
    async def delete_node_plugin(
        self,
        uuid: Annotated[str, Path(description="Node plugin UUID")],
    ) -> DeleteNodePluginResponseDto:
        """Delete Node Plugin"""
        ...

    @post("/node-plugins/actions/reorder", response_class=ReorderNodePluginsResponseDto)
    async def reorder_node_plugins(
        self,
        body: Annotated[ReorderNodePluginsRequestDto, PydanticBody()],
    ) -> ReorderNodePluginsResponseDto:
        """Reorder Node Plugins"""
        ...

    @post("/node-plugins/actions/clone", response_class=CloneNodePluginResponseDto)
    async def clone_node_plugin(
        self,
        body: Annotated[CloneNodePluginRequestDto, PydanticBody()],
    ) -> CloneNodePluginResponseDto:
        """Clone Node Plugin"""
        ...

    @post("/node-plugins/executor", response_class=None)
    async def plugin_executor(
        self,
        body: Annotated[PluginExecutorRequestDto, PydanticBody()],
    ) -> PluginExecutorResponseDto:
        """Execute command on node plugins"""
        ...

    @post("/node-plugins/actions/sync", response_class=None)
    async def sync_node_plugin(
        self,
        body: Annotated[SyncNodePluginRequestDto, PydanticBody()],
    ) -> None:
        """Push the plugin config, including its shared lists, to every node it is active on (202 Accepted)"""
        ...

    @get("/node-plugins/tags", response_class=GetNodePluginsTagsResponseDto)
    async def get_node_plugins_tags(self) -> GetNodePluginsTagsResponseDto:
        """Get tags of Node Plugins"""
        ...

    @patch("/node-plugins/tags", response_class=SetNodePluginsTagsResponseDto)
    async def set_node_plugin_tags(
        self,
        body: Annotated[SetNodePluginsTagsRequestDto, PydanticBody()],
    ) -> SetNodePluginsTagsResponseDto:
        """Set tags of Node Plugin"""
        ...

    @get("/node-plugins/shared-lists", response_class=GetSharedListsResponseDto)
    async def get_all_shared_lists(self) -> GetSharedListsResponseDto:
        """Get Shared Lists (name, type and item count only)"""
        ...

    @get("/node-plugins/shared-lists/by-name", response_class=GetSharedListResponseDto)
    async def get_shared_list_by_name(
        self,
        name: Annotated[str, Query(description="Shared list name")],
    ) -> GetSharedListResponseDto:
        """Get Shared List by name (with its items)"""
        ...

    @post("/node-plugins/shared-lists", response_class=CreateSharedListResponseDto)
    async def create_shared_list(
        self,
        body: Annotated[CreateSharedListRequestDto, PydanticBody()],
    ) -> CreateSharedListResponseDto:
        """Create Shared List"""
        ...

    @patch("/node-plugins/shared-lists", response_class=UpdateSharedListResponseDto)
    async def update_shared_list(
        self,
        body: Annotated[UpdateSharedListRequestDto, PydanticBody()],
    ) -> UpdateSharedListResponseDto:
        """Update Shared List"""
        ...

    @delete("/node-plugins/shared-lists", response_class=None)
    async def delete_shared_list_by_name(
        self,
        body: Annotated[DeleteSharedListRequestDto, PydanticBody()],
    ) -> DeleteSharedListResponseDto:
        """Delete Shared List by name (204 No Content)"""
        ...

    @post("/node-plugins/shared-lists/actions/sync", response_class=None)
    async def sync_shared_list(
        self,
        body: Annotated[SyncSharedListRequestDto, PydanticBody()],
    ) -> None:
        """Push every plugin referencing this shared list to its nodes (202 Accepted)"""
        ...

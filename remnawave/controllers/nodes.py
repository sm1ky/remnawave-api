from typing import Annotated

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateNodeRequestDto,
    CreateNodeResponseDto,
    DeleteNodeResponseDto,
    DisableNodeResponseDto,
    EnableNodeResponseDto,
    GetAllNodesResponseDto,
    GetAllNodesTagsResponseDto,
    GetOneNodeResponseDto,
    ReorderNodeRequestDto,
    ReorderNodeResponseDto,
    RestartAllNodesResponseDto,
    RestartNodeResponseDto,
    UpdateNodeRequestDto,
    UpdateNodeResponseDto,
    RestartAllNodesRequestBodyDto,
    RestartNodeRequestBodyDto,
    ResetNodeTrafficRequestDto,
    ResetNodeTrafficResponseDto,
    ProfileModificationRequestDto,
    ProfileModificationResponseDto,
    NodesBulkActionsRequestDto,
    NodesBulkActionsResponseDto,
    BulkNodesUpdateRequestDto,
    BulkNodesUpdateResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class NodesController(BaseController):
    @get("/nodes/tags", response_class=GetAllNodesTagsResponseDto)
    async def get_all_nodes_tags(
        self,
    ) -> GetAllNodesTagsResponseDto:
        """Get all nodes tags"""
        ...

    @post("/nodes", response_class=CreateNodeResponseDto)
    async def create_node(
        self,
        body: Annotated[CreateNodeRequestDto, PydanticBody()],
    ) -> CreateNodeResponseDto:
        """Create Node"""
        ...

    @get("/nodes", response_class=GetAllNodesResponseDto)
    async def get_all_nodes(
        self,
    ) -> GetAllNodesResponseDto:
        """Get All Nodes"""
        ...

    @get("/nodes/{uuid}", response_class=GetOneNodeResponseDto)
    async def get_one_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> GetOneNodeResponseDto:
        """Get One Node"""
        ...

    @delete("/nodes/{uuid}", response_class=None)
    async def delete_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> DeleteNodeResponseDto:
        """Delete Node"""
        ...

    @patch("/nodes", response_class=UpdateNodeResponseDto)
    async def update_node(
        self,
        body: Annotated[UpdateNodeRequestDto, PydanticBody()],
    ) -> UpdateNodeResponseDto:
        """Update Node"""
        ...

    @post("/nodes/{uuid}/actions/enable", response_class=EnableNodeResponseDto)
    async def enable_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> EnableNodeResponseDto:
        """Enable Node"""
        ...

    @post("/nodes/{uuid}/actions/disable", response_class=DisableNodeResponseDto)
    async def disable_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> DisableNodeResponseDto:
        """Disable Node"""
        ...

    @post("/nodes/{uuid}/actions/restart", response_class=None)
    async def restart_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
        body: Annotated[RestartNodeRequestBodyDto | None, PydanticBody()] = None,
    ) -> RestartNodeResponseDto:
        """Restart Node"""
        ...

    @post("/nodes/actions/restart-all", response_class=None)
    async def restart_all_nodes(
        self,
        body: Annotated[RestartAllNodesRequestBodyDto, PydanticBody()],
    ) -> RestartAllNodesResponseDto:
        """Restart All Nodes"""
        ...

    @post("/nodes/actions/reorder", response_class=ReorderNodeResponseDto)
    async def reorder_nodes(
        self,
        body: Annotated[ReorderNodeRequestDto, PydanticBody()],
    ) -> ReorderNodeResponseDto:
        """Reorder Nodes"""
        ...
    
    @post("/nodes/{uuid}/actions/reset-traffic", response_class=None)
    async def reset_node_traffic(
        self,
        uuid: Annotated[str, Path(description="UUID of the node")],
    ) -> ResetNodeTrafficResponseDto:
        """Reset traffic for individual node"""
        ...
        
        
    @post("/nodes/bulk-actions/profile-modification", response_class=None)
    async def profile_modification(
        self,
        body: Annotated[ProfileModificationRequestDto, PydanticBody()],
    ) -> ProfileModificationResponseDto:
        """Modify Inbounds & Profile for many nodes"""
        ...

    @post("/nodes/bulk-actions", response_class=None)
    async def nodes_bulk_actions(
        self,
        body: Annotated[NodesBulkActionsRequestDto, PydanticBody()],
    ) -> NodesBulkActionsResponseDto:
        """Perform actions for many nodes (ENABLE, DISABLE, RESTART, RESET_TRAFFIC)"""
        ...

    @post("/nodes/bulk-actions/update", response_class=None)
    async def bulk_nodes_update(
        self,
        body: Annotated[BulkNodesUpdateRequestDto, PydanticBody()],
    ) -> BulkNodesUpdateResponseDto:
        """Update many nodes"""
        ...
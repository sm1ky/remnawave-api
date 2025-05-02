from typing import Annotated, List

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave_api.models import (
    CreateNodeRequestDto,
    DeleteNodeResponseDto,
    NodeResponseDto,
    NodesResponseDto,
    ReorderNodeRequestDto,
    RestartNodeResponseDto,
    UpdateNodeRequestDto,
)
from remnawave_api.rapid import AttributeBody, BaseController, delete, get, patch, post


class NodesController(BaseController):
    @post("/nodes", response_class=NodeResponseDto)
    async def create_node(
        self,
        body: Annotated[CreateNodeRequestDto, PydanticBody()],
    ) -> NodeResponseDto:
        """Create Node"""
        ...

    @get("/nodes", response_class=NodesResponseDto)
    async def get_all_nodes(
        self,
    ) -> NodesResponseDto:
        """Get All Nodes"""
        ...

    @get("/nodes/{uuid}", response_class=NodeResponseDto)
    async def get_one_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> NodeResponseDto:
        """Get One Node"""
        ...
        
    @delete("/nodes/{uuid}", response_class=DeleteNodeResponseDto)
    async def delete_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> DeleteNodeResponseDto:
        """Delete Node"""
        ...
        
    @patch("/nodes", response_class=NodeResponseDto)
    async def update_node(
        self,
        body: Annotated[UpdateNodeRequestDto, PydanticBody()],
    ) -> NodeResponseDto:
        """Update Node"""
        ...

    @post("/nodes/{uuid}/actions/enable", response_class=NodeResponseDto)
    async def enable_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> NodeResponseDto:
        """Enable Node"""
        ...

    @post("/nodes/{uuid}/actions/disable", response_class=NodeResponseDto)
    async def disable_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> NodeResponseDto:
        """Disable Node"""
        ...

    @post("/nodes/{uuid}/actions/restart", response_class=RestartNodeResponseDto)
    async def restart_node(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> RestartNodeResponseDto:
        """Restart Node"""
        ...

    @post("/nodes/actions/restart-all", response_class=RestartNodeResponseDto)
    async def restart_all_nodes(
        self,
    ) -> RestartNodeResponseDto:
        """Restart All Nodes"""
        ...

    @post("/nodes/actions/reorder", response_class=NodesResponseDto)
    async def reorder_nodes(
        self,
        nodes: Annotated[List[ReorderNodeRequestDto], AttributeBody()],
    ) -> NodesResponseDto:
        """Reorder Nodes"""
        ...

"""Node Integrations models (Remnawave API v3.4.0+)."""

from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class NodeIntegrationDto(BaseModel):
    """A single node integration."""

    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: str
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)


class GetNodeIntegrationsResponseDto(BaseModel):
    """Response for ``GET /api/node-integrations``."""

    model_config = ConfigDict(populate_by_name=True)

    total: float
    node_integrations: List[NodeIntegrationDto] = Field(alias="nodeIntegrations")


class GetNodeIntegrationResponseDto(NodeIntegrationDto):
    """Response for ``GET /api/node-integrations/{uuid}``."""

    pass


class CreateNodeIntegrationRequestDto(BaseModel):
    """Request body for ``POST /api/node-integrations``."""

    model_config = ConfigDict(populate_by_name=True)

    name: Annotated[str, StringConstraints(min_length=2, max_length=30)]
    description: Annotated[Optional[str], StringConstraints(max_length=255)] = None
    config: Dict[str, Any]


class CreateNodeIntegrationResponseDto(NodeIntegrationDto):
    """Response for ``POST /api/node-integrations``."""

    pass


class UpdateNodeIntegrationRequestDto(BaseModel):
    """Request body for ``PATCH /api/node-integrations``."""

    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    name: Annotated[Optional[str], StringConstraints(min_length=2, max_length=30)] = None
    description: Annotated[Optional[str], StringConstraints(max_length=255)] = None
    config: Optional[Dict[str, Any]] = None
    restart_nodes: Optional[bool] = Field(None, serialization_alias="restartNodes")


class UpdateNodeIntegrationResponseDto(NodeIntegrationDto):
    """Response for ``PATCH /api/node-integrations``."""

    pass


class DeleteNodeIntegrationResponseDto(BaseModel):
    """Response for ``DELETE /api/node-integrations/{uuid}`` (204 No Content)."""

    model_config = ConfigDict(populate_by_name=True)

    is_deleted: bool = Field(alias="isDeleted")

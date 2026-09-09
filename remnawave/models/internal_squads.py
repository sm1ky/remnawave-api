from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

from remnawave.models.tags import GetTagsResponseDto, SetTagsRequestDto, SetTagsResponseDto


class InboundsDto(BaseModel):
    uuid: UUID
    profile_uuid: UUID = Field(alias="profileUuid")
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None
    port: Optional[float] = None
    raw_inbound: Optional[dict] = Field(None, alias="rawInbound")


class InfoDto(BaseModel):
    members_count: float = Field(alias="membersCount")
    inbounds_count: float = Field(alias="inboundsCount")


class InternalSquadDto(BaseModel):
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    name: str
    tags: List[str] = Field(default_factory=list)
    info: Optional[InfoDto] = Field(default=None)
    inbounds: List[InboundsDto] = Field(default_factory=list)
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CreateInternalSquadRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]
    inbounds: List[UUID] = Field(default_factory=list)


class CreateInternalSquadResponseDto(InternalSquadDto):
    pass


class UpdateInternalSquadRequestDto(BaseModel):
    uuid: UUID
    inbounds: List[UUID] = Field(default_factory=list)
    name: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]] = None


class UpdateInternalSquadResponseDto(InternalSquadDto):
    pass


class GetAllInternalSquadsResponse(BaseModel):
    total: float
    internal_squads: List[InternalSquadDto] = Field(alias="internalSquads")


class GetAllInternalSquadsResponseDto(GetAllInternalSquadsResponse):
    pass


class GetInternalSquadByUuidResponseDto(InternalSquadDto):
    pass


class DeleteInternalSquadResponseDto(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")


class AddUsersToInternalSquadRequestDto(BaseModel):
    user_uuids: List[UUID] = Field(alias="userUuids")


class BulkActionsResponseDto(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class AddUsersToInternalSquadResponseDto(BulkActionsResponseDto):
    pass


class DeleteUsersFromInternalSquadRequestDto(BaseModel):
    user_uuids: List[UUID] = Field(alias="userUuids")


class DeleteUsersFromInternalSquadResponseDto(BulkActionsResponseDto):
    pass


class AccessibleNodeDto(BaseModel):
    uuid: UUID
    name: str = Field(alias="nodeName")
    country_code: Optional[str] = Field(default=None, alias="countryCode")
    config_profile_uuid: Optional[UUID] = Field(default=None, alias="configProfileUuid")
    config_profile_name: Optional[str] = Field(default=None, alias="configProfileName")
    active_inbounds: List[Optional[UUID]] = Field(
        default_factory=list, alias="activeInbounds"
    )


class GetInternalSquadAccessibleNodesResponseDto(BaseModel):
    squad_uuid: UUID = Field(alias="squadUuid")
    accessible_nodes: List[AccessibleNodeDto] = Field(alias="accessibleNodes")


class ReorderInternalSquadItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderInternalSquadsRequestDto(BaseModel):
    items: List[ReorderInternalSquadItem]


class ReorderInternalSquadsResponseDto(GetAllInternalSquadsResponse):
    pass


# ===== v3.0.0 targeted bulk membership =====
class AddManyUsersToInternalSquadBodyDto(BaseModel):
    user_ids: List[int] = Field(serialization_alias="userIds", min_length=1, max_length=1000)


class DeleteManyUsersFromInternalSquadBodyDto(BaseModel):
    user_ids: List[int] = Field(serialization_alias="userIds", min_length=1, max_length=1000)


# ===== Tags (Remnawave API v3.4.0+) =====
class GetInternalSquadsTagsResponseDto(GetTagsResponseDto):
    """Response for ``GET /api/internal-squads/tags``."""

    pass


class SetInternalSquadsTagsRequestDto(SetTagsRequestDto):
    """Request body for ``PATCH /api/internal-squads/tags``."""

    pass


class SetInternalSquadsTagsResponseDto(SetTagsResponseDto):
    """Response for ``PATCH /api/internal-squads/tags``."""

    pass

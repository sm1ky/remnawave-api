from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

from remnawave.models.tags import GetTagsResponseDto, SetTagsRequestDto, SetTagsResponseDto


class InboundDto(BaseModel):
    uuid: UUID
    profile_uuid: UUID = Field(alias="profileUuid")
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None
    port: Optional[float] = None
    raw_inbound: Optional[Any] = Field(None, alias="rawInbound")

class NodesProfileDto(BaseModel):
    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")

class ConfigProfileDto(BaseModel):
    uuid: UUID
    name: str
    view_position: int = Field(alias="viewPosition")
    tags: List[str] = Field(default_factory=list)
    config: Dict[str, Any]
    inbounds: List[InboundDto]
    nodes: List[NodesProfileDto] = []
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CreateConfigProfileRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]
    config: Dict[str, Any]


class CreateConfigProfileResponseDto(ConfigProfileDto):
    pass


class UpdateConfigProfileRequestDto(BaseModel):
    uuid: UUID
    name: Optional[Annotated[str, StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")]] = None
    config: Optional[Dict[str, Any]] = None


class UpdateConfigProfileResponseDto(ConfigProfileDto):
    pass


class GetAllConfigProfilesResponsePaginated(BaseModel):
    total: float
    config_profiles: List[ConfigProfileDto] = Field(alias="configProfiles")


class GetAllConfigProfilesResponseDto(GetAllConfigProfilesResponsePaginated):
    pass


class GetConfigProfileByUuidResponseDto(ConfigProfileDto):
    pass


class DeleteConfigProfileResponseDto(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")


class GetAllInboundsResponseDto(List[InboundDto]):
    pass


class GetInboundsByProfileUuidResponseDto(List[InboundDto]):
    pass


class ReorderConfigProfileItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderConfigProfilesRequestDto(BaseModel):
    items: List[ReorderConfigProfileItem]


class ReorderConfigProfilesResponseDto(GetAllConfigProfilesResponsePaginated):
    pass


# ===== Tags (Remnawave API v3.4.0+) =====
class GetConfigProfilesTagsResponseDto(GetTagsResponseDto):
    """Response for ``GET /api/config-profiles/tags``."""

    pass


class SetConfigProfilesTagsRequestDto(SetTagsRequestDto):
    """Request body for ``PATCH /api/config-profiles/tags``."""

    pass


class SetConfigProfilesTagsResponseDto(SetTagsResponseDto):
    """Response for ``PATCH /api/config-profiles/tags``."""

    pass

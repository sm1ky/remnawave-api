from typing import Annotated, Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from remnawave.models.tags import GetTagsResponseDto, SetTagsRequestDto, SetTagsResponseDto


class SubscriptionPageConfigDto(BaseModel):
    """Subscription page config data model"""
    model_config = ConfigDict(populate_by_name=True)
    
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    name: str
    tags: List[str] = Field(default_factory=list)
    config: Any | None


class GetSubscriptionPageConfigsData(BaseModel):
    """Data for getting all subscription page configs"""
    total: float
    configs: List[SubscriptionPageConfigDto]


class GetSubscriptionPageConfigsResponseDto(GetSubscriptionPageConfigsData):
    """Response with all subscription page configs"""
    pass


class GetSubscriptionPageConfigResponseDto(BaseModel):
    """Response with single subscription page config"""
    model_config = ConfigDict(populate_by_name=True)
    
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    name: str
    tags: List[str] = Field(default_factory=list)
    config: Any


class CreateSubscriptionPageConfigRequestDto(BaseModel):
    """Request to create subscription page config"""
    name: Annotated[
        str,
        StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")
    ]


class CreateSubscriptionPageConfigResponseDto(SubscriptionPageConfigDto):
    """Response after creating subscription page config"""
    pass


class UpdateSubscriptionPageConfigRequestDto(BaseModel):
    """Request to update subscription page config"""
    model_config = ConfigDict(populate_by_name=True)
    
    uuid: UUID
    name: Optional[Annotated[
        str,
        StringConstraints(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_\s-]+$")
    ]] = None
    config: Optional[Any] = None


class UpdateSubscriptionPageConfigResponseDto(SubscriptionPageConfigDto):
    """Response after updating subscription page config"""
    pass


class DeleteSubscriptionPageConfigData(BaseModel):
    """Data for delete response"""
    model_config = ConfigDict(populate_by_name=True)
    
    is_deleted: bool = Field(alias="isDeleted")


class DeleteSubscriptionPageConfigResponseDto(DeleteSubscriptionPageConfigData):
    """Response after deleting subscription page config"""
    pass


class ReorderSubscriptionPageConfigItem(BaseModel):
    """Item for reordering subscription page configs"""
    model_config = ConfigDict(populate_by_name=True)
    
    view_position: int = Field(alias="viewPosition")
    uuid: UUID


class ReorderSubscriptionPageConfigsRequestDto(BaseModel):
    """Request to reorder subscription page configs"""
    items: List[ReorderSubscriptionPageConfigItem]


class ReorderSubscriptionPageConfigsResponseDto(GetSubscriptionPageConfigsData):
    """Response after reordering subscription page configs"""
    pass


class CloneSubscriptionPageConfigRequestDto(BaseModel):
    """Request to clone subscription page config"""
    model_config = ConfigDict(populate_by_name=True)
    
    clone_from_uuid: UUID = Field(alias="cloneFromUuid")


class CloneSubscriptionPageConfigResponseDto(SubscriptionPageConfigDto):
    """Response after cloning subscription page config"""
    pass


class GetSubpageConfigByShortUuidRequestBodyDto(BaseModel):
    """Request body for getting subpage config by short UUID"""
    model_config = ConfigDict(populate_by_name=True)
    
    request_headers: dict[str, str] = Field(default_factory=dict, serialization_alias="requestHeaders")


class SubpageConfigData(BaseModel):
    """Data inside GetSubpageConfigByShortUuidResponseDto"""
    model_config = ConfigDict(populate_by_name=True)
    
    subpage_config_uuid: UUID | None = Field(alias="subpageConfigUuid")
    webpage_allowed: bool = Field(alias="webpageAllowed")


class GetSubpageConfigByShortUuidResponseDto(SubpageConfigData):
    """Response for getting subpage config by short UUID"""
    pass

# ===== Tags (Remnawave API v3.4.0+) =====
class GetSubpageConfigsTagsResponseDto(GetTagsResponseDto):
    """Response for ``GET /api/subscription-page-configs/tags``."""

    pass


class SetSubpageConfigsTagsRequestDto(SetTagsRequestDto):
    """Request body for ``PATCH /api/subscription-page-configs/tags``."""

    pass


class SetSubpageConfigsTagsResponseDto(SetTagsResponseDto):
    """Response for ``PATCH /api/subscription-page-configs/tags``."""

    pass

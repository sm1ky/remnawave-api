from typing import Annotated, Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

from remnawave.enums import TemplateType
from remnawave.models.tags import GetTagsResponseDto, SetTagsRequestDto, SetTagsResponseDto


class TemplateResponseDto(BaseModel):
    uuid: UUID
    name: str
    tags: List[str] = Field(default_factory=list)
    view_position: int = Field(alias="viewPosition")
    template_type: TemplateType = Field(alias="templateType")
    template_json: Any | None = Field(alias="templateJson")
    encoded_template_yaml: str | None = Field(alias="encodedTemplateYaml")


class TemplateInfoDto(BaseModel):
    """Template info without content - used in list responses"""
    uuid: UUID
    name: str
    tags: List[str] = Field(default_factory=list)
    view_position: int = Field(alias="viewPosition")
    template_type: TemplateType = Field(alias="templateType")
    template_json: Optional[Any] = Field(None, alias="templateJson")
    encoded_template_yaml: Optional[str] = Field(None, alias="encodedTemplateYaml")


class GetTemplateResponseDto(TemplateResponseDto):
    pass

class GetTemplatesData(BaseModel):
    total: float
    templates: List[TemplateInfoDto]

class GetTemplatesResponseDto(GetTemplatesData):
    pass


class CreateSubscriptionTemplateRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_\s-]+$")]
    template_type: TemplateType = Field(serialization_alias="templateType")


class CreateSubscriptionTemplateResponseDto(TemplateResponseDto):
    pass


class UpdateTemplateRequestDto(BaseModel):
    uuid: UUID
    name: Optional[Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=r"^[A-Za-z0-9_\s-]+$")]] = None
    template_json: Optional[dict] = Field(None, serialization_alias="templateJson")
    encoded_template_yaml: Optional[str] = Field(
        None, serialization_alias="encodedTemplateYaml"
    )


class UpdateTemplateResponseDto(TemplateResponseDto):
    pass

class DeleteTemplateData(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")


class DeleteSubscriptionTemplateResponseDto(DeleteTemplateData):
    pass


class ReorderTemplateItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderSubscriptionTemplatesRequestDto(BaseModel):
    items: List[ReorderTemplateItem]


class ReorderSubscriptionTemplatesResponseDto(GetTemplatesData):
    pass


# Legacy aliases for backward compatibility
class UpdateTemplateRequestDtoLegacy(BaseModel):
    template_type: TemplateType = Field(serialization_alias="templateType")
    template_json: Optional[dict] = Field(None, serialization_alias="templateJson")
    encoded_template_yaml: Optional[str] = Field(
        None, serialization_alias="encodedTemplateYaml"
    )


class UpdateTemplateResponseDtoLegacy(TemplateResponseDto):
    pass

# ===== Tags (Remnawave API v3.4.0+) =====
class GetSubscriptionTemplatesTagsResponseDto(GetTagsResponseDto):
    """Response for ``GET /api/subscription-templates/tags``."""

    pass


class SetSubscriptionTemplatesTagsRequestDto(SetTagsRequestDto):
    """Request body for ``PATCH /api/subscription-templates/tags``."""

    pass


class SetSubscriptionTemplatesTagsResponseDto(SetTagsResponseDto):
    """Response for ``PATCH /api/subscription-templates/tags``."""

    pass

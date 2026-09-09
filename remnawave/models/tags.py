"""Shared DTOs for the per-resource ``/tags`` endpoints (Remnawave API v3.4.0+).

Config profiles, internal/external squads, node plugins, subscription page
configs and subscription templates all expose the very same pair of routes
(``GET .../tags`` and ``PATCH .../tags``), so the payload shapes live here once
and every resource module subclasses them under its OpenAPI name.
"""

from typing import Annotated, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

# Same constraints as host/node tags: uppercase alphanumerics, underscores and colons.
EntityTag = Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]


class GetTagsResponseDto(BaseModel):
    """Distinct tags used across every entity of a resource."""

    tags: List[str] = Field(default_factory=list)


class SetTagsRequestDto(BaseModel):
    """Replace the tag list of a single entity."""

    model_config = ConfigDict(populate_by_name=True)

    uuid: UUID
    tags: List[EntityTag] = Field(default_factory=list, max_length=10)


class SetTagsResponseDto(BaseModel):
    """Entity uuid together with its tags after the update."""

    uuid: UUID
    tags: List[str] = Field(default_factory=list)

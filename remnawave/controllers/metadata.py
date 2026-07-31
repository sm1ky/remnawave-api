from typing import Annotated

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    GetNodeMetadataResponseDto,
    GetUserMetadataResponseDto,
    UpsertNodeMetadataRequestBodyDto,
    UpsertNodeMetadataResponseDto,
    UpsertUserMetadataRequestBodyDto,
    UpsertUserMetadataResponseDto,
)
from remnawave.rapid import BaseController, get, put


class MetadataController(BaseController):
    @get("/metadata/user/{userId}", response_class=GetUserMetadataResponseDto)
    async def get_user_metadata(
        self,
        user_id: Annotated[int, Path(description="Numeric id of the user", alias="userId")],
    ) -> GetUserMetadataResponseDto:
        """Get user metadata"""
        ...

    @put("/metadata/user/{userId}", response_class=UpsertUserMetadataResponseDto)
    async def upsert_user_metadata(
        self,
        user_id: Annotated[int, Path(description="Numeric id of the user", alias="userId")],
        body: Annotated[UpsertUserMetadataRequestBodyDto, PydanticBody()],
    ) -> UpsertUserMetadataResponseDto:
        """Update or create User Metadata"""
        ...

    @get("/metadata/node/{uuid}", response_class=GetNodeMetadataResponseDto)
    async def get_node_metadata(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
    ) -> GetNodeMetadataResponseDto:
        """Get node metadata"""
        ...

    @put("/metadata/node/{uuid}", response_class=UpsertNodeMetadataResponseDto)
    async def upsert_node_metadata(
        self,
        uuid: Annotated[str, Path(description="Node UUID")],
        body: Annotated[UpsertNodeMetadataRequestBodyDto, PydanticBody()],
    ) -> UpsertNodeMetadataResponseDto:
        """Update or create Node Metadata"""
        ...

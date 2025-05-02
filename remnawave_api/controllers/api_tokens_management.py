from typing import Annotated

from httpx import Response
from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave_api.models import (
    CreateApiTokenRequestDto,
    CreateApiTokenResponseDto,
    DeleteApiTokenResponseDto,
    FindAllApiTokensResponseDto,
)
from remnawave_api.rapid import BaseController, delete, get, post


class APITokensManagementController(BaseController):
    @post("/tokens", response_class=CreateApiTokenResponseDto)
    async def create(
        self,
        body: Annotated[CreateApiTokenRequestDto, PydanticBody()],
    ) -> CreateApiTokenResponseDto:
        """Create new API token"""
        ...

    @delete("/tokens/{uuid}", response_class=DeleteApiTokenResponseDto)
    async def delete(
        self,
        uuid: Annotated[str, Path(description="UUID of the API token")],
    ) -> DeleteApiTokenResponseDto:
        """Delete API token"""
        ...

    @get("/tokens", response_class=FindAllApiTokensResponseDto)
    async def find_all(
        self,
    ) -> FindAllApiTokensResponseDto:
        """Get all API tokens"""
        ...

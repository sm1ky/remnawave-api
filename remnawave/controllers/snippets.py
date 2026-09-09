from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateSnippetRequestDto,
    CreateSnippetResponseDto,
    DeleteSnippetRequestDto,
    DeleteSnippetResponseDto,
    GetSnippetsResponseDto,
    SyncSnippetRequestDto,
    UpdateSnippetRequestDto,
    UpdateSnippetResponseDto,
)
from remnawave.rapid import BaseController, delete, get, post, patch


class SnippetsController(BaseController):
    @get("/snippets", response_class=GetSnippetsResponseDto)
    async def get_snippets(self) -> GetSnippetsResponseDto:
        """Get snippets"""
        ...

    @post("/snippets", response_class=CreateSnippetResponseDto)
    async def create_snippet(
        self,
        body: Annotated[CreateSnippetRequestDto, PydanticBody()],
    ) -> CreateSnippetResponseDto:
        """Create snippet"""
        ...

    @patch("/snippets", response_class=UpdateSnippetResponseDto)
    async def update_snippet(
        self,
        body: Annotated[UpdateSnippetRequestDto, PydanticBody()],
    ) -> UpdateSnippetResponseDto:
        """Update snippet"""
        ...

    @delete("/snippets", response_class=None)
    async def delete_snippet_by_name(
        self,
        body: Annotated[DeleteSnippetRequestDto, PydanticBody()],
    ) -> DeleteSnippetResponseDto:
        """Delete snippet"""
        ...

    @post("/snippets/actions/sync", response_class=None)
    async def sync_snippet(
        self,
        body: Annotated[SyncSnippetRequestDto, PydanticBody()],
    ) -> None:
        """Sync a snippet to every config profile that references it (202 Accepted)"""
        ...

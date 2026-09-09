from typing import Annotated, Any, List

from pydantic import BaseModel, Field, StringConstraints, RootModel

# Snippet names may address a "folder" with "/" separators (Remnawave API v3.4.0+)
SNIPPET_NAME_PATTERN = r"^[A-Za-z0-9_ -]+(\/[A-Za-z0-9_ -]+)*$"


class SnippetItem(BaseModel):
    """Individual snippet item"""
    name: str
    snippet: Any  # Can be any JSON object or array


class SnippetsData(BaseModel):
    """Snippets response data"""
    total: int
    snippets: List[SnippetItem]


# Изменяем структуру - API возвращает данные напрямую
class GetSnippetsResponseDto(SnippetsData):
    """Get all snippets response - extends SnippetsData directly"""
    pass


class CreateSnippetResponseDto(SnippetsData):
    """Create snippet response - extends SnippetsData directly"""
    pass


class UpdateSnippetResponseDto(SnippetsData):
    """Update snippet response - extends SnippetsData directly"""
    pass


class DeleteSnippetResponseDto(SnippetsData):
    """Delete snippet response - extends SnippetsData directly"""
    pass


class CreateSnippetRequestDto(BaseModel):
    """Create snippet request"""
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=SNIPPET_NAME_PATTERN)]
    snippet: List[dict]  # Array of objects


class UpdateSnippetRequestDto(BaseModel):
    """Update snippet request"""
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=SNIPPET_NAME_PATTERN)]
    snippet: List[dict]  # Array of objects


class DeleteSnippetRequestDto(BaseModel):
    """Delete snippet request"""
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=SNIPPET_NAME_PATTERN)]


class SyncSnippetRequestDto(BaseModel):
    """Request body for ``POST /api/snippets/actions/sync``."""
    name: Annotated[str, StringConstraints(min_length=2, max_length=255, pattern=SNIPPET_NAME_PATTERN)]

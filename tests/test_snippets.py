import pytest

from remnawave.models import (
    CreateSnippetRequestDto,
    DeleteSnippetRequestDto,
    GetSnippetsResponseDto,
    UpdateSnippetRequestDto,
)

def random_string(length=10):
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@pytest.mark.asyncio
async def test_snippets_full_workflow(remnawave):
    # Test getting all snippets
    snippets = await remnawave.snippets.get_snippets()
    assert isinstance(snippets, GetSnippetsResponseDto)
    initial_count = snippets.total

    # Test creating a snippet with unique name
    rand_name = random_string()
    create_request = CreateSnippetRequestDto(
        name=rand_name,
        snippet=[
            {"type": "vmess", "port": 443},
            {"type": "vless", "encryption": "none"}
        ]
    )
    created = await remnawave.snippets.create_snippet(create_request)
    assert created.total == initial_count + 1
    
    # Verify snippet was created
    snippets_after_create = await remnawave.snippets.get_snippets()
    snippet_names = [s.name for s in snippets_after_create.snippets]
    assert rand_name in snippet_names

    # Test updating the snippet
    update_request = UpdateSnippetRequestDto(
        name=rand_name,
        snippet=[
            {"type": "shadowsocks", "method": "aes-256-gcm"},
            {"type": "trojan", "password": "test-password"}
        ]
    )
    updated = await remnawave.snippets.update_snippet(update_request)
    assert updated.total == initial_count + 1
    
    # Test deleting the snippet
    delete_request = DeleteSnippetRequestDto(name=rand_name)
    deleted = await remnawave.snippets.delete_snippet_by_name(delete_request)
    assert deleted is None
    
    # Verify snippet was deleted
    snippets_after_delete = await remnawave.snippets.get_snippets()
    snippet_names_after = [s.name for s in snippets_after_delete.snippets]
    assert rand_name not in snippet_names_after


@pytest.mark.asyncio
async def test_snippet_name_validation(remnawave):
    """Test that snippet names are properly validated"""
    # Valid names
    valid_names = ["Test Snippet", "My_Snippet", "Snippet-123", "A B C"]
    
    for name in valid_names:
        request = CreateSnippetRequestDto(name=name, snippet=[{"test": "data"}])
        # Should not raise validation error
        assert request.name == name
    
    # Invalid names would be caught by Pydantic validation
    with pytest.raises(ValueError):
        CreateSnippetRequestDto(name="x", snippet=[])  # Too short
        
    with pytest.raises(ValueError):
        CreateSnippetRequestDto(name="", snippet=[])  # Empty name
"""Tests for the API Tokens controller.

The panel restricts token management to an admin session, so a suite authenticated
with an API token gets 403 here — those tests skip instead of failing.
"""
import pytest

from remnawave.exceptions import ForbiddenError
from remnawave.models import (
    CreateApiTokenRequestDto,
    CreateApiTokenResponseDto,
    FindAllApiTokensResponseDto,
    GetApiTokenScopesResponseDto,
)
from tests.utils import generate_random_string


def _skip_if_forbidden(exc: ForbiddenError) -> None:
    pytest.skip(
        "Управление API-токенами доступно только админ-сессии, "
        f"текущий токен получает {exc}"
    )


class TestApiTokens:
    @pytest.mark.asyncio
    async def test_find_all(self, remnawave):
        """Список токенов разбирается моделью"""
        try:
            response = await remnawave.api_tokens_management.find_all()
        except ForbiddenError as exc:
            _skip_if_forbidden(exc)

        assert isinstance(response, FindAllApiTokensResponseDto)
        assert isinstance(response.api_keys, list)
        for token in response.api_keys:
            assert token.uuid is not None
            assert token.token_name

    @pytest.mark.asyncio
    async def test_get_scopes(self, remnawave):
        """Панель отдаёт непустой каталог скоупов"""
        try:
            response = await remnawave.api_tokens_management.get_scopes()
        except ForbiddenError as exc:
            _skip_if_forbidden(exc)

        assert isinstance(response, GetApiTokenScopesResponseDto)
        assert response.resources

    @pytest.mark.asyncio
    async def test_create_and_delete(self, remnawave):
        """Созданный токен появляется в списке и пропадает после удаления"""
        name = f"sdk_test_{generate_random_string(length=8)}"
        try:
            created = await remnawave.api_tokens_management.create(
                CreateApiTokenRequestDto(name=name, expires_in_days=1)
            )
        except ForbiddenError as exc:
            _skip_if_forbidden(exc)

        assert isinstance(created, CreateApiTokenResponseDto)
        assert created.token

        token_uuid = str(created.uuid)
        try:
            listed = await remnawave.api_tokens_management.find_all()
            assert token_uuid in [str(t.uuid) for t in listed.api_keys]
        finally:
            deleted = await remnawave.api_tokens_management.delete(uuid=token_uuid)
            assert deleted is None

        listed_after = await remnawave.api_tokens_management.find_all()
        assert token_uuid not in [str(t.uuid) for t in listed_after.api_keys]

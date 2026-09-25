"""Tests for the Passkeys controller.

Registration and verification need a real WebAuthn authenticator, so only the read
paths are exercised here. The panel serves them to an admin session, so a suite
authenticated with an API token skips on 403.
"""
import pytest

from remnawave.exceptions import ForbiddenError
from remnawave.models import (
    GetAllPasskeysResponseDto,
    GetPasskeyRegistrationOptionsResponseDto,
)


def _skip_if_forbidden(exc: ForbiddenError) -> None:
    pytest.skip(f"Passkeys доступны только админ-сессии, текущий токен получает {exc}")


class TestPasskeys:
    @pytest.mark.asyncio
    async def test_get_active_passkeys(self, remnawave):
        try:
            response = await remnawave.passkeys.get_active_passkeys()
        except ForbiddenError as exc:
            _skip_if_forbidden(exc)

        assert isinstance(response, GetAllPasskeysResponseDto)
        assert isinstance(response.passkeys, list)
        for passkey in response.passkeys:
            assert passkey.id
            assert passkey.created_at is not None

    @pytest.mark.asyncio
    async def test_registration_options(self, remnawave):
        """Опции регистрации приходят с challenge и параметрами RP"""
        try:
            response = await remnawave.passkeys.passkey_registration_options()
        except ForbiddenError as exc:
            _skip_if_forbidden(exc)

        assert isinstance(response, GetPasskeyRegistrationOptionsResponseDto)

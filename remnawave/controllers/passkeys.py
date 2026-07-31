from typing import Annotated

from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    DeletePasskeyRequestDto,
    DeletePasskeyResponseDto,
    GetAllPasskeysResponseDto,
    GetPasskeyRegistrationOptionsResponseDto,
    UpdatePasskeyRequestDto,
    UpdatePasskeyResponseDto,
    VerifyPasskeyRegistrationRequestDto,
    VerifyPasskeyRegistrationResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class PasskeysController(BaseController):
    @get("/passkeys/registration/options", response_class=GetPasskeyRegistrationOptionsResponseDto)
    async def passkey_registration_options(
        self,
    ) -> GetPasskeyRegistrationOptionsResponseDto:
        """Get registration options for passkey"""
        ...

    @post("/passkeys/registration/verify", response_class=VerifyPasskeyRegistrationResponseDto)
    async def passkey_registration_verify(
        self,
        body: Annotated[VerifyPasskeyRegistrationRequestDto, PydanticBody()],
    ) -> VerifyPasskeyRegistrationResponseDto:
        """Verify registration for passkey"""
        ...

    @get("/passkeys", response_class=GetAllPasskeysResponseDto)
    async def get_active_passkeys(
        self,
    ) -> GetAllPasskeysResponseDto:
        """Get all passkeys"""
        ...

    @delete("/passkeys", response_class=None)
    async def delete_passkey(
        self,
        body: Annotated[DeletePasskeyRequestDto, PydanticBody()],
    ) -> DeletePasskeyResponseDto:
        """Delete a passkey by ID"""
        ...

    @patch("/passkeys", response_class=UpdatePasskeyResponseDto)
    async def update_passkey(
        self,
        body: Annotated[UpdatePasskeyRequestDto, PydanticBody()],
    ) -> UpdatePasskeyResponseDto:
        """Update a passkey name"""
        ...
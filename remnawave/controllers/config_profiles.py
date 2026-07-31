from typing import Annotated

from rapid_api_client import Path, Query
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateConfigProfileRequestDto,
    CreateConfigProfileResponseDto,
    DeleteConfigProfileResponseDto,
    GetAllConfigProfilesResponseDto,
    GetAllInboundsResponseDto,
    GetConfigProfileByUuidResponseDto,
    GetInboundsByProfileUuidResponseDto,
    ReorderConfigProfilesRequestDto,
    ReorderConfigProfilesResponseDto,
    UpdateConfigProfileRequestDto,
    UpdateConfigProfileResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class ConfigProfilesController(BaseController):
    @get("/config-profiles", response_class=GetAllConfigProfilesResponseDto)
    async def get_config_profiles(self) -> GetAllConfigProfilesResponseDto:
        """Get config profiles"""
        ...

    @post("/config-profiles", response_class=CreateConfigProfileResponseDto)
    async def create_config_profile(
        self,
        body: Annotated[CreateConfigProfileRequestDto, PydanticBody()],
    ) -> CreateConfigProfileResponseDto:
        """Create config profile"""
        ...

    @patch("/config-profiles", response_class=UpdateConfigProfileResponseDto)
    async def update_config_profile(
        self,
        body: Annotated[UpdateConfigProfileRequestDto, PydanticBody()],
    ) -> UpdateConfigProfileResponseDto:
        """Update Core Config in specific config profile"""
        ...

    @get("/config-profiles/inbounds", response_class=GetAllInboundsResponseDto)
    async def get_all_inbounds(self) -> GetAllInboundsResponseDto:
        """Get all inbounds from all config profiles"""
        ...

    @get("/config-profiles/{uuid}/inbounds", response_class=GetInboundsByProfileUuidResponseDto)
    async def get_inbounds_by_profile_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the config profile")],
    ) -> GetInboundsByProfileUuidResponseDto:
        """Get inbounds by profile uuid"""
        ...

    @get("/config-profiles/{uuid}", response_class=GetConfigProfileByUuidResponseDto)
    async def get_config_profile_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the config profile")],
    ) -> GetConfigProfileByUuidResponseDto:
        """Get config profile by uuid"""
        ...

    @delete("/config-profiles/{uuid}", response_class=None)
    async def delete_config_profile_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the config profile")],
    ) -> DeleteConfigProfileResponseDto:
        """Delete config profile"""
        ...

    @post("/config-profiles/actions/reorder", response_class=ReorderConfigProfilesResponseDto)
    async def reorder_config_profiles(
        self,
        body: Annotated[ReorderConfigProfilesRequestDto, PydanticBody()],
    ) -> ReorderConfigProfilesResponseDto:
        """Reorder config profiles"""
        ...

    # Get computed config profile by uuid​
    @get("/config-profiles/{uuid}/computed-config", response_class=GetConfigProfileByUuidResponseDto)
    async def get_computed_config_profile_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the config profile")],
    ) -> GetConfigProfileByUuidResponseDto:
        """Get computed config profile by uuid"""
        ...
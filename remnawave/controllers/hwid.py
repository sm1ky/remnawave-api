from typing import Annotated, Optional
from uuid import UUID

from remnawave.models import (
    CreateUserHwidDeviceResponseDto,
    DeleteUserHwidDeviceResponseDto,
    GetUserHwidDevicesResponseDto,
    GetHwidStatisticsResponseDto,
    CreateHWIDUser,
    HWIDDeleteRequest,
    DeleteUserAllHwidDeviceRequestDto,
    GetTopUsersByHwidDevicesResponseDto
)
from rapid_api_client import Path, PydanticBody, Query
from remnawave.rapid import AttributeBody, BaseController, post, get


class HWIDUserController(BaseController):
    @get("/hwid/devices", response_class=GetUserHwidDevicesResponseDto)
    async def get_hwid_users(
        self,
        size: Annotated[int | None, AttributeBody()] = None,
        start: Annotated[int | None, AttributeBody()] = None,
    ) -> GetUserHwidDevicesResponseDto:
        """Get all user HWID devices"""
        ...

    @get("/hwid/devices/stats", response_class=GetHwidStatisticsResponseDto)
    async def get_hwid_stats(
        self,
    ) -> GetHwidStatisticsResponseDto:
        """Get HWID statistics"""
        ...

    @post("/hwid/devices", response_class=CreateUserHwidDeviceResponseDto)
    async def add_hwid_to_users(
        self,
        body: Annotated[CreateHWIDUser, PydanticBody()],
    ) -> CreateUserHwidDeviceResponseDto:
        """Create a user HWID device"""
        ...

    @post("/hwid/devices/delete", response_class=DeleteUserHwidDeviceResponseDto)
    async def delete_hwid_to_user(
        self,
        body: Annotated[HWIDDeleteRequest, PydanticBody()],
    ) -> DeleteUserHwidDeviceResponseDto:
        """Delete a user HWID device"""
        ...

    @post("/hwid/devices/delete-all", response_class=DeleteUserHwidDeviceResponseDto)
    async def delete_all_hwid_user(
        self,
        body: Annotated[DeleteUserAllHwidDeviceRequestDto, PydanticBody()],
    ) -> DeleteUserHwidDeviceResponseDto:
        """Delete all user HWID devices"""
        ...

    @get("/hwid/devices/{userId}", response_class=GetUserHwidDevicesResponseDto)
    async def get_hwid_user(
        self,
        user_id: Annotated[int, Path(description="Numeric id of the user", alias="userId")],
    ) -> GetUserHwidDevicesResponseDto:
        """Get a user HWID device"""
        ...

    @get("/hwid/devices/top-users", response_class=GetTopUsersByHwidDevicesResponseDto)
    async def get_top_users_by_hwid_devices(
        self,
        size: Annotated[Optional[int], Query(default=None, description="Page size for pagination")] = None,
        start: Annotated[Optional[int], Query(default=None, description="Offset for pagination")] = None,
    ) -> GetTopUsersByHwidDevicesResponseDto:
        """Get top users by HWID devices"""
        ...
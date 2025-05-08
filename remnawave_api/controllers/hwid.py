from typing import Annotated
from uuid import UUID

from remnawave_api.models import (
    HWIDUserResponseDto,
    HWIDUserResponseDtoList,
    CreateHWIDUser,
    HWIDDeleteRequest
)
from rapid_api_client import Path, PydanticBody
from remnawave_api.rapid import AttributeBody, BaseController, post, get


class HWIDUserController(BaseController):
    @post("/hwid/devices", response_class=HWIDUserResponseDtoList)
    async def add_hwid_to_users(
        self,
        body: Annotated[CreateHWIDUser, PydanticBody()],
    ) -> HWIDUserResponseDtoList:
        """Create a user HWID device"""
        ...
        
    @post("/hwid/devices/delete", response_class=HWIDUserResponseDtoList)
    async def delete_hwid_to_user(
        self,
        body: Annotated[HWIDDeleteRequest, PydanticBody()],
    ) -> HWIDUserResponseDtoList:
        """Delete a user HWID device"""
        ...
    
    @get("/hwid/devices/{uuid}", response_class=HWIDUserResponseDtoList)
    async def get_hwid_user(
        self,
        uuid: Annotated[str, Path(description="UUID of the User")],
    ) -> HWIDUserResponseDtoList:
        """Get a user HWID device"""
        ...
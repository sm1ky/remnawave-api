from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

class CreateHWIDUser(BaseModel):
    hwid: str
    userUuid: UUID
    platform: str
    osVersion: str
    deviceModel: str
    userAgent: str

class HWIDUserResponseDto(BaseModel):
    hwid: str
    user_uuid: UUID = Field(alias="userUuid")
    platform: str
    os_version: str = Field(alias="osVersion")
    device_model: str = Field(alias="deviceModel")
    user_agent: str = Field(alias="userAgent")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    
class HWIDUserResponseDtoList(BaseModel):
    response: List[HWIDUserResponseDto]
    
class HWIDDeleteRequest(BaseModel):
    hwid: str
    userUuid: UUID
    

from datetime import datetime
from typing import List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, RootModel

class NodeActiveSquadDto(BaseModel):
    squad_name: str = Field(alias="squadName")
    active_inbounds: list[str] = Field(alias="activeInbounds")

class NodeInfoDto(BaseModel):
    uuid: UUID
    name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    config_profile_name: str = Field(alias="configProfileName")
    config_profile_uuid: UUID = Field(alias="configProfileUuid")
    active_squads: List[NodeActiveSquadDto] = Field(alias="activeSquads")

class GetUserAccessibleNodesResponse(BaseModel):
    user_uuid: UUID = Field(alias="userUuid")
    active_nodes: List[NodeInfoDto] = Field(default_factory=list, alias="activeNodes")

    @property
    def nodes(self) -> List[NodeInfoDto]:
        """Backward compatibility (renamed to `active_nodes`/`activeNodes` in v2.8.x)"""
        return self.active_nodes

class GetUserAccessibleNodesResponseDto(GetUserAccessibleNodesResponse):
    pass


class NodeUsageDto(BaseModel):
    """Individual node usage item"""
    node_uuid: UUID = Field(alias="nodeUuid")
    date: datetime
    upload: int = Field(0, alias="totalBytes")  
    download: int = Field(0, alias="totalBytes") 

    
class GetNodesUsageByRangeResponseDto(RootModel[List[NodeUsageDto]]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)
    
    def __len__(self):
        """Return length of list"""
        return len(self.root)


class UserUsageDto(BaseModel):
    """User usage data with node information"""
    user_uuid: UUID = Field(alias="userUuid")
    node_uuid: UUID = Field(alias="nodeUuid")
    username: str
    total: int
    date: datetime


class GetNodeUserUsageByRangeResponseDto(RootModel[List[UserUsageDto]]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)
    
    def __len__(self):
        """Return length of list"""
        return len(self.root)

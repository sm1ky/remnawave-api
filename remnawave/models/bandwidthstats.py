from datetime import datetime, date
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, RootModel


# ============ Legacy Models (Deprecated) ============

class NodeUsageResponseDto(BaseModel):
    """Deprecated: Old node usage model"""
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    total: int
    total_download: float = Field(alias="totalDownload")
    total_upload: float = Field(alias="totalUpload")
    human_readable_total: str = Field(alias="humanReadableTotal")
    human_readable_total_download: str = Field(alias="humanReadableTotalDownload")
    human_readable_total_upload: str = Field(alias="humanReadableTotalUpload")
    date: date


class NodesUsageResponseDto(RootModel[List[NodeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


class GetNodesUsageByRangeResponseDto(RootModel[List[NodeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


class NodeRealtimeUsageResponseDto(BaseModel):
    """Deprecated: Use NodeRealtimeUsageItem instead"""
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    download_bytes: float = Field(alias="downloadBytes")
    upload_bytes: float = Field(alias="uploadBytes")
    total_bytes: float = Field(alias="totalBytes")
    download_speed_bps: float = Field(alias="downloadSpeedBps")
    upload_speed_bps: float = Field(alias="uploadSpeedBps")
    total_speed_bps: float = Field(alias="totalSpeedBps")


class NodesRealtimeUsageResponseDto(RootModel[List[NodeRealtimeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesRealtimeUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


class GetNodesRealtimeUsageResponseDto(RootModel[List[NodeRealtimeUsageResponseDto]]):
    """Deprecated: Use GetStatsNodesRealtimeUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


class UserUsageByRangeItem(BaseModel):
    """Deprecated: Use LegacyUserUsageItem instead"""
    user_uuid: UUID = Field(alias="userUuid")
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    total: int
    date: str


class GetUserUsageByRangeResponseDto(RootModel[List[UserUsageByRangeItem]]):
    """Deprecated: Use GetLegacyStatsUserUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


class NodeUserUsageItem(BaseModel):
    """Deprecated: Use LegacyNodeUserUsageItem instead"""
    user_uuid: UUID = Field(alias="userUuid")
    username: str
    node_uuid: UUID = Field(alias="nodeUuid")
    total: int
    date: str


class GetNodeUserUsageByRangeResponseDto(RootModel[List[NodeUserUsageItem]]):
    """Deprecated: Use GetLegacyStatsNodesUsersUsageResponseDto instead"""
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        return bool(self.root)
    
    def __len__(self):
        return len(self.root)


# ============ New Stats Models ============

# Legacy Stats Models

class LegacyUserUsageItem(BaseModel):
    """Legacy user usage item"""
    user_uuid: UUID = Field(alias="userUuid")
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    total: int
    date: str


class GetLegacyStatsUserUsageResponseDto(RootModel[List[LegacyUserUsageItem]]):
    """Response for legacy user usage"""
    @property
    def response(self) -> List[LegacyUserUsageItem]:
        return self.root
    
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class LegacyNodeUserUsageItem(BaseModel):
    """Legacy node user usage item"""
    user_uuid: UUID = Field(alias="userUuid")
    username: str
    node_uuid: UUID = Field(alias="nodeUuid")
    total: int
    date: str


class GetLegacyStatsNodesUsersUsageResponseDto(RootModel[List[LegacyNodeUserUsageItem]]):
    """Response for legacy nodes users usage"""
    @property
    def response(self) -> List[LegacyNodeUserUsageItem]:
        return self.root
    
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


# Realtime Stats

class NodeRealtimeUsageItem(BaseModel):
    """Node realtime usage item"""
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    download_bytes: float = Field(alias="downloadBytes")
    upload_bytes: float = Field(alias="uploadBytes")
    total_bytes: float = Field(alias="totalBytes")
    download_speed_bps: float = Field(alias="downloadSpeedBps")
    upload_speed_bps: float = Field(alias="uploadSpeedBps")
    total_speed_bps: float = Field(alias="totalSpeedBps")


class GetStatsNodesRealtimeUsageResponseDto(RootModel[List[NodeRealtimeUsageItem]]):
    """Response for nodes realtime usage"""
    @property
    def response(self) -> List[NodeRealtimeUsageItem]:
        return self.root
    
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


# Stats Nodes Usage (with charts)

class TopNodeItem(BaseModel):
    """Top node item"""
    uuid: UUID
    color: str
    name: str
    country_code: str = Field(alias="countryCode")
    total: int


class NodeSeriesItem(BaseModel):
    """Node series item for charts"""
    uuid: UUID
    name: str
    color: str
    country_code: str = Field(alias="countryCode")
    total: int
    data: List[int]


class StatsNodesUsageData(BaseModel):
    """Stats nodes usage data"""
    categories: List[str]
    sparkline_data: List[int] = Field(alias="sparklineData")
    top_nodes: List[TopNodeItem] = Field(alias="topNodes")
    series: List[NodeSeriesItem]


class GetStatsNodesUsageResponseDto(RootModel[StatsNodesUsageData]):
    """Response for stats nodes usage"""
    @property
    def response(self) -> StatsNodesUsageData:
        return self.root


# Stats Node Users Usage (with charts)

class TopUserItem(BaseModel):
    """Top user item"""
    color: str
    username: str
    total: int


class StatsNodeUsersUsageData(BaseModel):
    """Stats node users usage data"""
    categories: List[str]
    sparkline_data: List[int] = Field(alias="sparklineData")
    top_users: List[TopUserItem] = Field(alias="topUsers")


class GetStatsNodeUsersUsageResponseDto(RootModel[StatsNodeUsersUsageData]):
    """Response for stats node users usage"""
    @property
    def response(self) -> StatsNodeUsersUsageData:
        return self.root


# Stats Nodes Users Usage by Nodes UUIDs (POST /bandwidth-stats/nodes/users)

class GetStatsNodesUsersUsageRequestDto(BaseModel):
    """Request for nodes users usage by nodes UUIDs"""
    nodes_uuids: List[UUID] = Field(serialization_alias="nodesUuids", min_length=1)


class TopNodesUserItem(BaseModel):
    """Top user item for nodes users usage"""
    color: str
    username: str
    total: float


class StatsNodesUsersUsageData(BaseModel):
    """Stats nodes users usage data"""
    categories: List[str]
    sparkline_data: List[float] = Field(alias="sparklineData")
    top_users: List[TopNodesUserItem] = Field(alias="topUsers")


class GetStatsNodesUsersUsageResponseDto(RootModel[StatsNodesUsersUsageData]):
    """Response for stats nodes users usage by nodes UUIDs"""
    @property
    def response(self) -> StatsNodesUsersUsageData:
        return self.root


# Stats User Usage (with charts)

class StatsUserUsageData(BaseModel):
    """Stats user usage data"""
    categories: List[str]
    sparkline_data: List[int] = Field(alias="sparklineData")
    top_nodes: List[TopNodeItem] = Field(alias="topNodes")
    series: List[NodeSeriesItem]


class GetStatsUserUsageResponseDto(RootModel[StatsUserUsageData]):
    """Response for stats user usage"""
    @property
    def response(self) -> StatsUserUsageData:
        return self.root


# ===== v3.0.0 usage endpoints =====
class FetchNodesUsageBodyDto(BaseModel):
    nodes_uuids: List[UUID] = Field(serialization_alias="nodesUuids", min_length=1)


class FetchNodesUsageResponseDto(BaseModel):
    nodes: List[Dict[str, Any]] = Field(default_factory=list)


class GetInternalSquadUsageResponseDto(BaseModel):
    squad_uuid: UUID = Field(alias="squadUuid")
    users: List[Dict[str, Any]] = Field(default_factory=list)
    next_cursor: Optional[int] = Field(None, alias="nextCursor")
    has_more: bool = Field(False, alias="hasMore")


class GetInternalSquadUserUsageResponseDto(BaseModel):
    days: List[Dict[str, Any]] = Field(default_factory=list)

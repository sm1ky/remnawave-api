import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from remnawave.enums import ResponseType
from remnawave.models.subscriptions_settings import ResponseRule, ResponseRules


class NodeStatistic(BaseModel):
    node_name: str = Field(alias="nodeName")
    date: datetime.date
    total_bytes: str = Field(alias="totalBytes")


class NodesStatisticResponseDto(BaseModel):
    last_seven_days: List[NodeStatistic] = Field(alias="lastSevenDays")


class BandwidthStatistic(BaseModel):
    current: str
    previous: str
    difference: str


class BandwidthStatisticResponseDto(BaseModel):
    last_two_days: BandwidthStatistic = Field(alias="bandwidthLastTwoDays")
    last_seven_days: BandwidthStatistic = Field(alias="bandwidthLastSevenDays")
    last_30_days: BandwidthStatistic = Field(alias="bandwidthLast30Days")
    calendar_month: BandwidthStatistic = Field(alias="bandwidthCalendarMonth")
    current_year: BandwidthStatistic = Field(alias="bandwidthCurrentYear")


class CPUStatistic(BaseModel):
    cores: float
    physical_cores: Optional[float] = Field(None, alias="physicalCores")


class MemoryStatistic(BaseModel):
    total: float
    free: float
    used: float
    active: Optional[float] = None
    available: Optional[float] = None


class StatusCounts(BaseModel):
    """Dynamic status counts - использует additionalProperties"""
    model_config = {"extra": "allow"}
    
    def __getitem__(self, key: str) -> int:
        """Allow dict-like access"""
        return getattr(self, key, 0)
    
    def get(self, key: str, default: int = 0) -> int:
        """Dict-like get method"""
        return getattr(self, key, default)


class UsersStatistic(BaseModel):
    status_counts: StatusCounts = Field(alias="statusCounts")
    total_users: float = Field(alias="totalUsers")


class OnlineStatistic(BaseModel):
    last_day: float = Field(alias="lastDay")
    last_week: float = Field(alias="lastWeek")
    never_online: float = Field(alias="neverOnline")
    online_now: float = Field(alias="onlineNow")


class NodesStatistic(BaseModel):
    total_online: float = Field(alias="totalOnline")
    total_bytes_lifetime: str = Field(alias="totalBytesLifetime")


class StatisticResponseDto(BaseModel):
    """System statistics data"""
    cpu: CPUStatistic
    memory: MemoryStatistic
    uptime: float
    timestamp: float
    users: UsersStatistic
    online_stats: OnlineStatistic = Field(alias="onlineStats")
    nodes: NodesStatistic


class PM2Stat(BaseModel):
    name: str
    memory: str
    cpu: str


class RemnawaveHealthData(BaseModel):
    pm2_stats: List[PM2Stat] = Field(alias="pm2Stats")


class GetStatsResponseDto(StatisticResponseDto):
    """Get system statistics response"""
    pass


class GetBandwidthStatsResponseDto(BaseModel):
    last_two_days: BandwidthStatistic = Field(alias="bandwidthLastTwoDays")
    last_seven_days: BandwidthStatistic = Field(alias="bandwidthLastSevenDays")
    last_30_days: BandwidthStatistic = Field(alias="bandwidthLast30Days")
    calendar_month: BandwidthStatistic = Field(alias="bandwidthCalendarMonth")
    current_year: BandwidthStatistic = Field(alias="bandwidthCurrentYear")


class GetNodesStatisticsResponseDto(BaseModel):
    last_seven_days: List[NodeStatistic] = Field(alias="lastSevenDays")


class RuntimeMetric(BaseModel):
    """Runtime metric from health endpoint"""
    model_config = {"extra": "allow"}

    rss: Optional[float] = None
    heap_total: Optional[float] = Field(None, alias="heapTotal")
    heap_used: Optional[float] = Field(None, alias="heapUsed")
    external: Optional[float] = None
    instance_type: Optional[str] = Field(None, alias="instanceType")


class GetRemnawaveHealthResponseDto(BaseModel):
    pm2_stats: Optional[List[PM2Stat]] = Field(None, alias="pm2Stats")
    runtime_metrics: Optional[List[RuntimeMetric]] = Field(None, alias="runtimeMetrics")


class TrafficStatDto(BaseModel):
    tag: str
    upload: str
    download: str


class NodeMetric(BaseModel):
    """Node metric data (API v1.10)"""
    node_uuid: str = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_emoji: str = Field(alias="countryEmoji")
    provider_name: str = Field(alias="providerName")
    users_online: float = Field(alias="usersOnline")
    inbounds_stats: List[TrafficStatDto] = Field(alias="inboundsStats")
    outbounds_stats: List[TrafficStatDto] = Field(alias="outboundsStats")

    @property
    def uuid(self) -> str:
        return self.node_uuid

    @property
    def name(self) -> str:
        return self.node_name

    @property
    def connected_users(self) -> float:
        return self.users_online

    @property
    def cpu_usage(self) -> None:
        return None

    @property
    def memory_usage(self) -> None:
        return None

    @property
    def network_upload(self) -> None:
        return None

    @property
    def network_download(self) -> None:
        return None

    @property
    def uptime(self) -> None:
        return None

    @property
    def last_seen(self) -> None:
        return None


class GetNodesMetricsResponseDto(BaseModel):
    nodes: List[NodeMetric]


class X25519KeyPair(BaseModel):
    public_key: str = Field(alias="publicKey")
    private_key: str = Field(alias="privateKey")


class GetX25519KeyPairResponseDto(BaseModel):
    key_pairs: List[X25519KeyPair] = Field(alias="keypairs")


# OpenAPI v1.10 schema name
GenerateX25519ResponseDto = GetX25519KeyPairResponseDto


class DebugSrrMatcherRequestDto(BaseModel):
    response_rules: ResponseRules = Field(serialization_alias="responseRules")


class DebugSrrMatcherData(BaseModel):
    matched: bool
    response_type: ResponseType = Field(alias="responseType")
    matched_rule: Optional[ResponseRule] = Field(alias="matchedRule")
    input_headers: Dict[str, str] = Field(alias="inputHeaders")
    output_headers: Dict[str, str] = Field(alias="outputHeaders")


class DebugSrrMatcherResponseDto(DebugSrrMatcherData):
    pass

class RecapThisMonth(BaseModel):
    users: float
    traffic: str


class RecapTotal(BaseModel):
    users: float
    nodes: float
    traffic: str
    nodes_ram: str = Field(alias="nodesRam")
    nodes_cpu_cores: float = Field(alias="nodesCpuCores")
    distinct_countries: float = Field(alias="distinctCountries")


class GetRecapResponseDto(BaseModel):
    this_month: RecapThisMonth = Field(alias="thisMonth")
    total: RecapTotal
    version: str
    init_date: datetime.datetime = Field(alias="initDate")


class BuildInfo(BaseModel):
    """Build information"""
    time: str
    number: str


class GitBackendInfo(BaseModel):
    """Git backend information"""
    commit_sha: str = Field(alias="commitSha")
    branch: str
    commit_url: str = Field(alias="commitUrl")


class GitFrontendInfo(BaseModel):
    """Git frontend information"""
    commit_sha: str = Field(alias="commitSha")
    commit_url: str = Field(alias="commitUrl")


class GitInfo(BaseModel):
    """Git information"""
    backend: GitBackendInfo
    frontend: GitFrontendInfo


class MetadataResponse(BaseModel):
    """Metadata response data"""
    version: str
    build: BuildInfo
    git: GitInfo


class GetMetadataResponseDto(MetadataResponse):
    """Get metadata response"""
    pass


# ===== v3.0.0 new system stats =====
class GetStatsDigestResponseDto(BaseModel):
    users: Dict[str, Any]
    traffic: Dict[str, Any]
    hwid_devices: Dict[str, Any] = Field(alias="hwidDevices")


class GetHttpStatsResponseDto(BaseModel):
    routes: List[Dict[str, Any]] = Field(default_factory=list)
    total: float = 0

from typing import Annotated
from rapid_api_client import PydanticBody, Query
from remnawave.models import (
    GetStatsDigestResponseDto,
    GetHttpStatsResponseDto,
    GetBandwidthStatsResponseDto,
    GetNodesStatisticsResponseDto,
    GetStatsResponseDto,
    GetNodesMetricsResponseDto,
    GetRemnawaveHealthResponseDto,
    GetX25519KeyPairResponseDto,
    DebugSrrMatcherRequestDto,
    DebugSrrMatcherResponseDto,
    GetMetadataResponseDto,
    GetRecapResponseDto,
    GetConfigurationResponseDto,
)
from remnawave.rapid import BaseController, get, post


class SystemController(BaseController):
    @get("/system/metadata", response_class=GetMetadataResponseDto)
    async def get_metadata(
        self,
    ) -> GetMetadataResponseDto:
        """Get Remnawave Information"""
        ...
        
    @get("/system/stats", response_class=GetStatsResponseDto)
    async def get_stats(
        self,
    ) -> GetStatsResponseDto:
        """Get System Stats"""
        ...

    @get("/system/stats/bandwidth", response_class=GetBandwidthStatsResponseDto)
    async def get_bandwidth_stats(
        self,
    ) -> GetBandwidthStatsResponseDto:
        """Get System Bandwidth Statistics"""
        ...

    @get("/system/stats/nodes", response_class=GetNodesStatisticsResponseDto)
    async def get_nodes_statistics(
        self,
    ) -> GetNodesStatisticsResponseDto:
        """Get Nodes Statistics"""
        ...

    @get("/system/health", response_class=GetRemnawaveHealthResponseDto)
    async def get_health(
        self,
    ) -> GetRemnawaveHealthResponseDto:
        """Get System Health"""
        ...

    @get("/system/nodes/metrics", response_class=GetNodesMetricsResponseDto)
    async def get_nodes_metrics(
        self,
    ) -> GetNodesMetricsResponseDto:
        """Get Nodes Metrics"""
        ...

    @get("/system/tools/x25519/generate", response_class=GetX25519KeyPairResponseDto)
    async def get_x25519_key_pair(
        self,
    ) -> GetX25519KeyPairResponseDto:
        """Get X25519 Key Pair"""
        ...
        
    @post("/system/testers/srr-matcher", response_class=DebugSrrMatcherResponseDto)
    async def debug_srr_matcher(
        self,
        body: Annotated[DebugSrrMatcherRequestDto, PydanticBody()],
    ) -> DebugSrrMatcherResponseDto:
        """Test SRR Matcher"""
        ...

    @get("/system/stats/recap", response_class=GetRecapResponseDto)
    async def get_recap(
        self,
    ) -> GetRecapResponseDto:
        """Get Recap"""
        ...

    @get("/system/stats/digest", response_class=GetStatsDigestResponseDto)
    async def get_stats_digest(
        self,
        start: Annotated[str, Query(description="Range start (datetime)")],
        end: Annotated[str, Query(description="Range end (datetime)")],
    ) -> GetStatsDigestResponseDto:
        """Aggregated statistics for a datetime range"""
        ...

    @get("/system/stats/http", response_class=GetHttpStatsResponseDto)
    async def get_http_stats(
        self,
    ) -> GetHttpStatsResponseDto:
        """HTTP request counters per route"""
        ...

    @get("/system/configuration", response_class=GetConfigurationResponseDto)
    async def get_configuration(
        self,
    ) -> GetConfigurationResponseDto:
        """Get Remnawave Configuration"""
        ...

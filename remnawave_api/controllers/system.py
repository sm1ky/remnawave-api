from remnawave_api.models import (
    BandwidthStatisticResponseDto,
    NodesStatisticResponseDto,
    StatisticResponseDto,
)
from remnawave_api.rapid import BaseController, get


class SystemController(BaseController):
    @get("/system/stats", response_class=StatisticResponseDto)
    async def get_stats(
        self,
    ) -> StatisticResponseDto:
        """Get System Stats"""
        ...

    @get("/system/stats/bandwidth", response_class=BandwidthStatisticResponseDto)
    async def get_bandwidth_stats(
        self,
    ) -> BandwidthStatisticResponseDto:
        """Get System Bandwidth Statistics"""
        ...

    @get("/system/stats/nodes", response_class=NodesStatisticResponseDto)
    async def get_nodes_statistics(
        self,
    ) -> NodesStatisticResponseDto:
        """Get Nodes Statistics"""
        ...

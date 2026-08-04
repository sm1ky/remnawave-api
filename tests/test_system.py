import pytest

from remnawave.models import (
    GetBandwidthStatsResponseDto,
    GetNodesStatisticsResponseDto,
    GetStatsResponseDto,
    GetNodesMetricsResponseDto,
    GetRemnawaveHealthResponseDto,
    GetConfigurationResponseDto,
)


class TestSystemStatistics:
    """Тесты для получения статистики системы"""
    
    @pytest.mark.asyncio
    async def test_get_stats(self, remnawave):
        """Тест получения общей статистики"""
        stats = await remnawave.system.get_stats()
        assert isinstance(stats, GetStatsResponseDto)
        assert hasattr(stats, 'timestamp')
        assert hasattr(stats, 'uptime')
    
    @pytest.mark.asyncio
    async def test_get_bandwidth_stats(self, remnawave):
        """Тест получения статистики по полосе пропускания"""
        bandwidth_stats = await remnawave.system.get_bandwidth_stats()
        assert isinstance(bandwidth_stats, GetBandwidthStatsResponseDto)
        assert hasattr(bandwidth_stats, 'current_year')
    
    @pytest.mark.asyncio
    async def test_get_nodes_statistics(self, remnawave):
        """Тест получения статистики по нодам"""
        nodes_statistics = await remnawave.system.get_nodes_statistics()
        assert isinstance(nodes_statistics, GetNodesStatisticsResponseDto)
        assert hasattr(nodes_statistics, 'last_seven_days')


class TestSystemMonitoring:
    """Тесты для мониторинга системы"""
    
    @pytest.mark.asyncio
    async def test_get_nodes_metrics(self, remnawave):
        """Тест получения метрик нод"""
        nodes_metrics = await remnawave.system.get_nodes_metrics()
        assert isinstance(nodes_metrics, GetNodesMetricsResponseDto)
        assert hasattr(nodes_metrics, 'nodes')
        assert isinstance(nodes_metrics.nodes, list)
        
        if nodes_metrics.nodes:  # Если список не пустой
            node = nodes_metrics.nodes[0]
            assert hasattr(node, 'uuid')
            assert hasattr(node, 'name')
            assert hasattr(node, 'cpu_usage')
            assert hasattr(node, 'memory_usage')
            assert hasattr(node, 'network_upload')
            assert hasattr(node, 'network_download')
            assert hasattr(node, 'uptime')
            assert hasattr(node, 'last_seen')
            assert hasattr(node, 'connected_users')
    
    @pytest.mark.asyncio
    async def test_get_health(self, remnawave):
        """Тест получения состояния здоровья системы"""
        health = await remnawave.system.get_health()
        assert isinstance(health, GetRemnawaveHealthResponseDto)
        assert hasattr(health, 'pm2_stats')


class TestSystemConfiguration:
    """Тесты для конфигурации системы (API v3.2.0)"""

    @pytest.mark.asyncio
    async def test_get_configuration(self, remnawave):
        """Тест получения конфигурации Remnawave"""
        config = await remnawave.system.get_configuration()
        assert isinstance(config, GetConfigurationResponseDto)

        # notifications
        assert isinstance(config.notifications.webhook, bool)
        # service
        assert isinstance(config.service.clean_usage_history, bool)
        assert isinstance(config.service.disable_user_usage_records, bool)
        assert isinstance(config.service.disable_srh_records, bool)
        assert isinstance(config.service.export_to_redis_stream, bool)
        # misc
        assert isinstance(config.misc.short_uuid_length, (int, float))
        assert isinstance(config.misc.sub_public_domain, str)
        assert isinstance(config.misc.user_usage_ignore_below_bytes, (int, float))

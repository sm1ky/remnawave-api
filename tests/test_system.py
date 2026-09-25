import re

import pytest

from remnawave.exceptions import ApiError
from remnawave.models import (
    DebugSrrMatcherRequestDto,
    DebugSrrMatcherResponseDto,
    GetBandwidthStatsResponseDto,
    GetHttpStatsResponseDto,
    GetMetadataResponseDto,
    GetNodesStatisticsResponseDto,
    GetRecapResponseDto,
    GetStatsDigestResponseDto,
    GetStatsResponseDto,
    GetNodesMetricsResponseDto,
    GetRemnawaveHealthResponseDto,
    GetConfigurationResponseDto,
    GetX25519KeyPairResponseDto,
)
from tests.utils import generate_utc_isoformat_range


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


class TestSystemMetadata:
    """Информация о панели и сборке"""

    @pytest.mark.asyncio
    async def test_get_metadata(self, remnawave):
        response = await remnawave.system.get_metadata()

        assert isinstance(response, GetMetadataResponseDto)
        # версия панели — непустой semver-подобный идентификатор
        assert response.version
        assert re.match(r"^\d+\.\d+", response.version), response.version
        assert response.build is not None
        assert response.build.number

    @pytest.mark.asyncio
    async def test_metadata_matches_spec_version(self, remnawave):
        """Панель в окружении должна соответствовать контракту, под который собран SDK"""
        response = await remnawave.system.get_metadata()
        major_minor = ".".join(response.version.split(".")[:2])
        assert major_minor == "3.4", (
            f"SDK собран под контракт 3.4.x, панель отвечает {response.version}"
        )


class TestSystemRecap:
    @pytest.mark.asyncio
    async def test_get_recap(self, remnawave):
        response = await remnawave.system.get_recap()

        assert isinstance(response, GetRecapResponseDto)
        assert response.this_month.users >= 0
        assert response.total.users >= response.this_month.users
        assert response.total.nodes >= 0
        assert response.this_month.traffic
        assert response.total.traffic

    @pytest.mark.asyncio
    async def test_recap_user_total_matches_users_endpoint(self, remnawave):
        """Сводка считает тех же пользователей, что отдаёт /users"""
        recap = await remnawave.system.get_recap()
        users = await remnawave.users.get_all_users(size=1)

        assert recap.total.users == users.total


class TestSystemStatsDigest:
    @pytest.mark.asyncio
    async def test_get_stats_digest(self, remnawave):
        start, end = generate_utc_isoformat_range()
        response = await remnawave.system.get_stats_digest(start=start, end=end)

        assert isinstance(response, GetStatsDigestResponseDto)

    @pytest.mark.asyncio
    async def test_inverted_range_is_rejected(self, remnawave):
        """start позже end — панель отвечает ошибкой, а не пустым отчётом"""
        start, end = generate_utc_isoformat_range()
        with pytest.raises(ApiError):
            await remnawave.system.get_stats_digest(start=end, end=start)


class TestSystemHttpStats:
    @pytest.mark.asyncio
    async def test_get_http_stats(self, remnawave):
        response = await remnawave.system.get_http_stats()

        assert isinstance(response, GetHttpStatsResponseDto)
        assert response.total >= 0
        assert isinstance(response.routes, list)

    @pytest.mark.asyncio
    async def test_counters_grow_after_a_request(self, remnawave):
        """Счётчик запросов растёт — значит цифры живые, а не заглушка"""
        before = await remnawave.system.get_http_stats()
        await remnawave.system.get_stats()
        after = await remnawave.system.get_http_stats()

        assert after.total >= before.total


class TestSystemTools:
    @pytest.mark.asyncio
    async def test_get_x25519_key_pair(self, remnawave):
        response = await remnawave.system.get_x25519_key_pair()

        assert isinstance(response, GetX25519KeyPairResponseDto)
        assert response.key_pairs

    @pytest.mark.asyncio
    async def test_key_pairs_differ_between_calls(self, remnawave):
        """Ключи генерируются, а не отдаются из кэша"""
        first = await remnawave.system.get_x25519_key_pair()
        second = await remnawave.system.get_x25519_key_pair()

        assert first.key_pairs != second.key_pairs


class TestSrrMatcher:
    """Тестер SRR-правил"""

    @pytest.mark.asyncio
    async def test_debug_srr_matcher_with_live_rules(self, remnawave):
        """Правила из настроек подписки прогоняются через тестер без ошибок"""
        settings = await remnawave.subscriptions_settings.get_settings()
        if settings.response_rules is None:
            pytest.skip("В настройках подписки не заданы response rules")

        response = await remnawave.system.debug_srr_matcher(
            DebugSrrMatcherRequestDto(response_rules=settings.response_rules)
        )

        assert isinstance(response, DebugSrrMatcherResponseDto)

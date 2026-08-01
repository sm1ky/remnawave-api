import pytest

from remnawave.exceptions import NotFoundError
from remnawave.models import (
    CloneNodePluginRequestDto,
    CloneNodePluginResponseDto,
    CreateNodePluginRequestDto,
    CreateNodePluginResponseDto,
    DeleteNodePluginResponseDto,
    GetNodePluginResponseDto,
    GetNodePluginsResponseDto,
    GetTorrentBlockerReportsResponseDto,
    GetTorrentBlockerReportsStatsResponseDto,
    PluginExecutorRequestDto,
    PluginExecutorResponseDto,
    ReorderNodePluginsRequestDto,
    ReorderNodePluginsResponseDto,
    TruncateTorrentBlockerReportsResponseDto,
    UpdateNodePluginRequestDto,
    UpdateNodePluginResponseDto,
    BlockIpsCommandDto,
    BlockIpItemDto,
    ReorderNodePluginItem,
    TargetAllNodesDto,
)
from tests.utils import generate_random_string


class TestNodePlugins:
    """Тесты для Node Plugins контроллера"""

    @pytest.mark.asyncio
    async def test_get_all_node_plugins(self, remnawave):
        """Тест получения списка всех Node Plugins"""
        response = await remnawave.node_plugins.get_all_node_plugins()
        
        assert isinstance(response, GetNodePluginsResponseDto)
        assert hasattr(response, "node_plugins")
        assert isinstance(response.node_plugins, list)

    @pytest.mark.asyncio
    async def test_create_and_delete_node_plugin(self, remnawave):
        """Тест создания и удаления Node Plugin"""
        plugin_name = f"test_plugin_{generate_random_string(length=8)}"
        
        # Create plugin
        create_response = await remnawave.node_plugins.create_node_plugin(
            CreateNodePluginRequestDto(
                name=plugin_name
            )
        )
        
        assert isinstance(create_response, CreateNodePluginResponseDto)
        assert create_response.uuid is not None
        plugin_uuid = str(create_response.uuid)
        
        # Get plugin by UUID to verify creation
        get_response = await remnawave.node_plugins.get_node_plugin_by_uuid(uuid=plugin_uuid)
        assert isinstance(get_response, GetNodePluginResponseDto)
        assert get_response.name == plugin_name
        
        # Delete plugin
        delete_response = await remnawave.node_plugins.delete_node_plugin(uuid=plugin_uuid)
        assert delete_response is None

    @pytest.mark.asyncio
    async def test_update_node_plugin(self, remnawave):
        """Тест обновления Node Plugin"""
        plugin_name = f"test_plugin_{generate_random_string(length=8)}"
        
        # Create plugin first
        create_response = await remnawave.node_plugins.create_node_plugin(
            CreateNodePluginRequestDto(
                name=plugin_name
            )
        )
        plugin_uuid = str(create_response.uuid)
        
        try:
            # Update plugin
            updated_name = f"updated_{plugin_name}"
            update_response = await remnawave.node_plugins.update_node_plugin(
                UpdateNodePluginRequestDto(
                    uuid=plugin_uuid,
                    name=updated_name,
                    plugin_config={"enabled": False}
                )
            )
            
            assert isinstance(update_response, UpdateNodePluginResponseDto)
            
            # Verify update
            get_response = await remnawave.node_plugins.get_node_plugin_by_uuid(uuid=plugin_uuid)
            assert get_response.name == updated_name
            
        finally:
            # Cleanup
            await remnawave.node_plugins.delete_node_plugin(uuid=plugin_uuid)

    @pytest.mark.asyncio
    async def test_reorder_node_plugins(self, remnawave):
        """Тест изменения порядка Node Plugins"""
        # Create two plugins
        plugin1_name = f"test_plugin_1_{generate_random_string(length=6)}"
        plugin2_name = f"test_plugin_2_{generate_random_string(length=6)}"
        
        create1 = await remnawave.node_plugins.create_node_plugin(
            CreateNodePluginRequestDto(
                name=plugin1_name
            )
        )
        uuid1 = str(create1.uuid)
        
        create2 = await remnawave.node_plugins.create_node_plugin(
            CreateNodePluginRequestDto(
                name=plugin2_name
            )
        )
        uuid2 = str(create2.uuid)
        
        try:
            # Reorder plugins
            reorder_response = await remnawave.node_plugins.reorder_node_plugins(
                ReorderNodePluginsRequestDto(
                    items=[
                        ReorderNodePluginItem(view_position=0, uuid=uuid2),
                        ReorderNodePluginItem(view_position=1, uuid=uuid1),
                    ]
                )
            )
            
            assert isinstance(reorder_response, ReorderNodePluginsResponseDto)
            
        finally:
            # Cleanup
            await remnawave.node_plugins.delete_node_plugin(uuid=uuid1)
            await remnawave.node_plugins.delete_node_plugin(uuid=uuid2)

    @pytest.mark.asyncio
    async def test_clone_node_plugin(self, remnawave):
        """Тест клонирования Node Plugin"""
        plugin_name = f"test_plugin_{generate_random_string(length=8)}"
        
        # Create plugin
        create_response = await remnawave.node_plugins.create_node_plugin(
            CreateNodePluginRequestDto(
                name=plugin_name
            )
        )
        original_uuid = str(create_response.uuid)
        
        try:
            # Clone plugin
            clone_response = await remnawave.node_plugins.clone_node_plugin(
                CloneNodePluginRequestDto(
                    clone_from_uuid=original_uuid,
                )
            )
            
            assert isinstance(clone_response, CloneNodePluginResponseDto)
            cloned_uuid = str(clone_response.uuid)
            
            # Verify clone
            get_cloned = await remnawave.node_plugins.get_node_plugin_by_uuid(uuid=cloned_uuid)
            assert get_cloned.uuid == clone_response.uuid
            
            # Cleanup cloned plugin
            await remnawave.node_plugins.delete_node_plugin(uuid=cloned_uuid)
            
        finally:
            # Cleanup original plugin
            await remnawave.node_plugins.delete_node_plugin(uuid=original_uuid)

    @pytest.mark.asyncio
    async def test_plugin_executor(self, remnawave):
        """Тест выполнения команды на плагинах"""
        # This test assumes there's at least one node plugin configured
        # Create a test plugin first
        plugin_name = f"test_plugin_{generate_random_string(length=8)}"
        
        create_response = await remnawave.node_plugins.create_node_plugin(
            CreateNodePluginRequestDto(
                name=plugin_name
            )
        )
        plugin_uuid = str(create_response.uuid)
        
        try:
            # Execute command
            try:
                executor_response = await remnawave.node_plugins.plugin_executor(
                    PluginExecutorRequestDto(
                        command=BlockIpsCommandDto(
                            command="blockIps",
                            ips=[
                                BlockIpItemDto(ip="192.168.1.1", timeout=60),
                                BlockIpItemDto(ip="10.0.0.1", timeout=60),
                            ],
                        ),
                        target_nodes=TargetAllNodesDto(target="allNodes"),
                    )
                )
                assert isinstance(executor_response, PluginExecutorResponseDto)
            except NotFoundError:
                # В тестовых окружениях без подключенных нод API может вернуть 404
                pytest.skip("Node plugins executor is unavailable in this environment (no connected nodes)")
            
        finally:
            # Cleanup
            await remnawave.node_plugins.delete_node_plugin(uuid=plugin_uuid)


class TestTorrentBlocker:
    """Тесты для Torrent Blocker функциональности"""

    @pytest.mark.asyncio
    async def test_get_torrent_blocker_reports(self, remnawave):
        """Тест получения отчетов Torrent Blocker"""
        response = await remnawave.node_plugins.get_torrent_blocker_reports(
            size=10,
            start=0
        )
        
        assert isinstance(response, GetTorrentBlockerReportsResponseDto)
        assert hasattr(response, "records")
        assert isinstance(response.records, list)
        assert hasattr(response, "total")

    @pytest.mark.asyncio
    async def test_get_torrent_blocker_reports_without_pagination(self, remnawave):
        """Тест получения отчетов Torrent Blocker без пагинации"""
        response = await remnawave.node_plugins.get_torrent_blocker_reports()
        
        assert isinstance(response, GetTorrentBlockerReportsResponseDto)
        assert hasattr(response, "records")
        assert isinstance(response.records, list)

    @pytest.mark.asyncio
    async def test_get_torrent_blocker_stats(self, remnawave):
        """Тест получения статистики Torrent Blocker"""
        response = await remnawave.node_plugins.get_torrent_blocker_reports_stats()
        
        assert isinstance(response, GetTorrentBlockerReportsStatsResponseDto)
        assert hasattr(response, "stats")

    @pytest.mark.asyncio
    async def test_truncate_torrent_blocker_reports(self, remnawave):
        """Тест очистки отчетов Torrent Blocker"""
        # This is a destructive operation, so be careful
        # Only run in test environment
        response = await remnawave.node_plugins.truncate_torrent_blocker_reports()
        
        assert response is None
        
        # Verify truncation by checking reports are empty
        reports = await remnawave.node_plugins.get_torrent_blocker_reports()
        assert len(reports.records) == 0

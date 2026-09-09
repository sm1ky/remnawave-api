import pytest

from remnawave.exceptions import ApiError, ConflictError, NotFoundError
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
    CreateSharedListRequestDto,
    CreateSharedListResponseDto,
    DeleteSharedListRequestDto,
    GetNodePluginsTagsResponseDto,
    GetSharedListResponseDto,
    GetSharedListsResponseDto,
    ReorderNodePluginItem,
    SetNodePluginsTagsRequestDto,
    SetNodePluginsTagsResponseDto,
    SyncNodePluginRequestDto,
    SyncSharedListRequestDto,
    TargetAllNodesDto,
    UpdateSharedListRequestDto,
    UpdateSharedListResponseDto,
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
            except ApiError as exc:
                # В тестовых окружениях без подключенных нод панель отвечает
                # 404 либо 500 A219 "Connected nodes not found"
                if isinstance(exc, NotFoundError) or "Connected nodes not found" in str(exc):
                    pytest.skip(
                        "Node plugins executor is unavailable in this environment (no connected nodes)"
                    )
                raise
            
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


class TestNodePluginTags:
    """Теги Node Plugins (Remnawave API v3.4.0+)"""

    @pytest.fixture
    async def plugin(self, remnawave):
        created = await remnawave.node_plugins.create_node_plugin(
            CreateNodePluginRequestDto(name=f"tags_{generate_random_string(length=8)}")
        )
        yield created
        try:
            await remnawave.node_plugins.delete_node_plugin(uuid=str(created.uuid))
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_new_plugin_has_empty_tags(self, remnawave, plugin):
        """Свежесозданный плагин приходит с пустым списком тегов"""
        assert plugin.tags == []

    @pytest.mark.asyncio
    async def test_get_node_plugins_tags(self, remnawave):
        """Тест получения списка тегов Node Plugins"""
        response = await remnawave.node_plugins.get_node_plugins_tags()

        assert isinstance(response, GetNodePluginsTagsResponseDto)
        assert isinstance(response.tags, list)

    @pytest.mark.asyncio
    async def test_set_node_plugin_tags(self, remnawave, plugin):
        """Тест установки тегов Node Plugin"""
        tags = ["SDK_TEST", "PLUGIN:TAG"]

        response = await remnawave.node_plugins.set_node_plugin_tags(
            SetNodePluginsTagsRequestDto(uuid=plugin.uuid, tags=tags)
        )

        assert isinstance(response, SetNodePluginsTagsResponseDto)
        assert response.uuid == plugin.uuid
        assert sorted(response.tags) == sorted(tags)

        fetched = await remnawave.node_plugins.get_node_plugin_by_uuid(uuid=str(plugin.uuid))
        assert sorted(fetched.tags) == sorted(tags)

        all_tags = await remnawave.node_plugins.get_node_plugins_tags()
        assert set(tags).issubset(set(all_tags.tags))

    @pytest.mark.asyncio
    async def test_clear_node_plugin_tags(self, remnawave, plugin):
        """Пустой список тегов очищает теги плагина"""
        await remnawave.node_plugins.set_node_plugin_tags(
            SetNodePluginsTagsRequestDto(uuid=plugin.uuid, tags=["SDK_TEST"])
        )

        response = await remnawave.node_plugins.set_node_plugin_tags(
            SetNodePluginsTagsRequestDto(uuid=plugin.uuid, tags=[])
        )
        assert response.tags == []

    @pytest.mark.asyncio
    async def test_sync_node_plugin(self, remnawave, plugin):
        """Тест синхронизации плагина на ноды (202 Accepted)"""
        response = await remnawave.node_plugins.sync_node_plugin(
            SyncNodePluginRequestDto(uuid=plugin.uuid)
        )

        assert response is None


class TestSharedLists:
    """Shared Lists для Node Plugins (Remnawave API v3.4.0+)"""

    @pytest.fixture
    async def shared_list(self, remnawave):
        name = f"sdk-{generate_random_string(length=8)}"
        created = await remnawave.node_plugins.create_shared_list(
            CreateSharedListRequestDto(
                name=name,
                config={"type": "ipList", "items": ["198.51.100.1", "198.51.100.2"]},
            )
        )
        yield created
        try:
            await remnawave.node_plugins.delete_shared_list_by_name(
                DeleteSharedListRequestDto(name=name)
            )
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_get_all_shared_lists(self, remnawave):
        """Тест получения превью всех shared lists"""
        response = await remnawave.node_plugins.get_all_shared_lists()

        assert isinstance(response, GetSharedListsResponseDto)
        assert isinstance(response.shared_lists, list)
        assert response.total == len(response.shared_lists)

    @pytest.mark.asyncio
    async def test_create_shared_list(self, remnawave, shared_list):
        """Тест создания shared list"""
        assert isinstance(shared_list, CreateSharedListResponseDto)
        assert shared_list.config["type"] == "ipList"
        assert shared_list.config["items"] == ["198.51.100.1", "198.51.100.2"]

    @pytest.mark.asyncio
    async def test_shared_list_preview_fields(self, remnawave, shared_list):
        """Превью содержит имя, тип и количество элементов"""
        response = await remnawave.node_plugins.get_all_shared_lists()
        preview = next(sl for sl in response.shared_lists if sl.name == shared_list.name)

        assert preview.type == "ipList"
        assert preview.items_count == 2

    @pytest.mark.asyncio
    async def test_get_shared_list_by_name(self, remnawave, shared_list):
        """Тест получения shared list по имени"""
        fetched = await remnawave.node_plugins.get_shared_list_by_name(name=shared_list.name)

        assert isinstance(fetched, GetSharedListResponseDto)
        assert fetched.name == shared_list.name
        assert fetched.config["items"] == ["198.51.100.1", "198.51.100.2"]

    @pytest.mark.asyncio
    async def test_update_shared_list(self, remnawave, shared_list):
        """Тест обновления shared list"""
        updated = await remnawave.node_plugins.update_shared_list(
            UpdateSharedListRequestDto(
                name=shared_list.name,
                config={"type": "ipList", "items": ["203.0.113.7"]},
            )
        )

        assert isinstance(updated, UpdateSharedListResponseDto)
        assert updated.config["items"] == ["203.0.113.7"]

        fetched = await remnawave.node_plugins.get_shared_list_by_name(name=shared_list.name)
        assert fetched.config["items"] == ["203.0.113.7"]

    @pytest.mark.asyncio
    async def test_delete_shared_list(self, remnawave):
        """Тест удаления shared list (204 No Content)"""
        name = f"sdk-{generate_random_string(length=8)}"
        await remnawave.node_plugins.create_shared_list(
            CreateSharedListRequestDto(
                name=name, config={"type": "ipList", "items": ["192.0.2.1"]}
            )
        )

        deleted = await remnawave.node_plugins.delete_shared_list_by_name(
            DeleteSharedListRequestDto(name=name)
        )
        assert deleted is None

        with pytest.raises(NotFoundError):
            await remnawave.node_plugins.get_shared_list_by_name(name=name)

    @pytest.mark.asyncio
    async def test_sync_shared_list(self, remnawave, shared_list):
        """Тест синхронизации shared list на ноды (202 Accepted)"""
        response = await remnawave.node_plugins.sync_shared_list(
            SyncSharedListRequestDto(name=shared_list.name)
        )

        assert response is None

    @pytest.mark.asyncio
    async def test_duplicate_name_conflicts(self, remnawave, shared_list):
        """Повторное имя shared list отклоняется (A246)"""
        with pytest.raises(ConflictError):
            await remnawave.node_plugins.create_shared_list(
                CreateSharedListRequestDto(
                    name=shared_list.name,
                    config={"type": "ipList", "items": ["192.0.2.1"]},
                )
            )

    @pytest.mark.asyncio
    async def test_get_unknown_name_raises_not_found(self, remnawave):
        """Неизвестное имя shared list даёт NotFoundError (A245)"""
        with pytest.raises(NotFoundError):
            await remnawave.node_plugins.get_shared_list_by_name(
                name=f"missing-{generate_random_string(length=10)}"
            )

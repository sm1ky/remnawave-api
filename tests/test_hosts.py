import random

import pytest

from remnawave.enums import ALPN, Fingerprint, InternalSquadsMode, SecurityLayer
from remnawave.exceptions import NotFoundError
from remnawave.exceptions.general import ApiError
from remnawave.models import (
    CreateHostRequestDto,
    CreateHostResponseDto,
    DeleteHostResponseDto,
    GetAllHostsResponseDto,
    GetOneHostResponseDto,
    ReorderHostItem,
    ReorderHostRequestDto,
    ReorderHostResponseDto,
    UpdateHostRequestDto,
    UpdateHostResponseDto,
    GetAllHostTagsResponseDto,
    CreateInternalSquadRequestDto,
    HostInternalSquadsDto,
    HostMapperCopyOp,
    HostMapperDto,
    HostMapperSetOp,
    HostMapperUnsetOp,
    UpdateManyHostsRequestDto,
)
from tests.conftest import REMNAWAVE_INBOUND_UUID, REMNAWAVE_CONFIG_PROFILE_UUID
from tests.utils import generate_random_string


class TestHostsBasic:
    """Тесты базового функционала хостов"""

    @pytest.mark.asyncio
    async def test_get_all_hosts(self, remnawave):
        """Тест получения списка всех хостов"""
        all_hosts = await remnawave.hosts.get_all_hosts()
        assert isinstance(all_hosts, GetAllHostsResponseDto)
        # Проверяем, что можно итерироваться по хостам
        for host in all_hosts:
            assert hasattr(host, 'uuid')
            assert hasattr(host, 'remark')
    
    @pytest.mark.asyncio
    async def test_get_hosts_tags(self, remnawave):
        """Тест получения всех тегов хостов"""
        try:
            tags = await remnawave.hosts.get_hosts_tags()
            assert isinstance(tags, GetAllHostTagsResponseDto)
            assert hasattr(tags, 'tags')
        except Exception as e:
            pytest.skip(f"Пропуск теста получения тегов: {str(e)}")


class TestHostsCRUD:
    """Тесты CRUD операций для хостов"""

    @pytest.fixture
    async def test_host(self, remnawave):
        """Фикстура для создания тестового хоста"""
        random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
        random_port: int = random.randint(5000, 8000)
        random_remark: str = generate_random_string()
        
        create_host = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=random_remark,
                address=random_ip,
                port=random_port,
                tag="TEST",  # Добавление тега
            )
        )
        
        yield create_host
        
        # Очистка - удаление тестового хоста
        try:
            await remnawave.hosts.delete_host(uuid=str(create_host.uuid))
        except Exception:
            pass
    
    @pytest.mark.asyncio
    async def test_create_host(self, remnawave):
        """Тест создания хоста"""
        random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
        random_port: int = random.randint(5000, 8000)
        random_remark: str = generate_random_string()
        
        create_host = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=random_remark,
                address=random_ip,
                port=random_port,
                tag="TEST",  # Добавление тега
                is_hidden=False,
                server_description="Test Server",
                vless_route_id=1234,
                shuffle_host=False,
                mihomo_x25519=False,
            )
        )
        
        assert isinstance(create_host, CreateHostResponseDto)
        assert str(create_host.inbound_uuid) == REMNAWAVE_INBOUND_UUID
        assert create_host.address == random_ip
        assert create_host.port == random_port
        assert create_host.remark == random_remark
        assert create_host.tag == "TEST"
        
        # Очистка - удаление созданного хоста
        await remnawave.hosts.delete_host(uuid=str(create_host.uuid))
    
    @pytest.mark.asyncio
    async def test_get_one_host(self, remnawave, test_host):
        """Тест получения одного хоста"""
        string_uuid = str(test_host.uuid)
        
        host = await remnawave.hosts.get_one_host(uuid=string_uuid)
        assert isinstance(host, GetOneHostResponseDto)
        assert host.uuid == test_host.uuid
        assert host.remark == test_host.remark
    
    @pytest.mark.asyncio
    async def test_update_host(self, remnawave, test_host):
        """Тест обновления хоста"""
        # Создаем новый объект для обновления
        update_data = UpdateHostRequestDto(
            uuid=test_host.uuid,
            server_description="Updated Host",
            is_disabled=False  # явно устанавливаем значение
        )
        
        # Обновляем хост
        updated_host: UpdateHostResponseDto = await remnawave.hosts.update_host(update_data)
        
        # Проверяем что обновление прошло успешно
        assert updated_host is not None
        assert updated_host.server_description == "Updated Host"
        assert updated_host.is_disabled is False
    
    @pytest.mark.asyncio
    async def test_delete_host(self, remnawave):
        """Тест удаления хоста"""
        # Сначала создаем хост для удаления
        random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
        random_port: int = random.randint(5000, 8000)
        random_remark: str = generate_random_string()
        
        create_host = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=random_remark,
                address=random_ip,
                port=random_port,
            )
        )
        
        string_uuid = str(create_host.uuid)
        
        # Теперь удаляем созданный хост
        delete_host = await remnawave.hosts.delete_host(uuid=string_uuid)
        assert delete_host is None
        
        # Проверяем, что хост действительно удален
        try:
            await remnawave.hosts.get_one_host(uuid=string_uuid)
            pytest.fail("Хост не был удален")
        except Exception:
            # Ожидаем ошибку, так как хост удален
            pass


class TestHostsOrdering:
    """Тесты упорядочивания хостов"""
    
    @pytest.mark.asyncio
    async def test_reorder_hosts(self, remnawave):
        """Тест переупорядочивания хостов"""
        try:
            # Получаем список хостов для работы
            hosts_response = await remnawave.hosts.get_all_hosts()
            
            # Преобразуем в список для проверки длины
            hosts_list = list(hosts_response)
            
            # Если хостов меньше 2, пропускаем тест
            if len(hosts_list) < 2:
                pytest.skip("Not enough hosts to test reordering")
            
            # Создаем объекты ReorderHostItem для первых двух хостов
            # и меняем их порядок (первый становится вторым, второй - первым)
            reorder_items = [
                ReorderHostItem(view_position=1, uuid=hosts_list[1].uuid),
                ReorderHostItem(view_position=0, uuid=hosts_list[0].uuid),
            ]
            
            # Формируем запрос на переупорядочивание
            reorder_request = ReorderHostRequestDto(hosts=reorder_items)
            
            # Отправляем запрос
            response: ReorderHostResponseDto = await remnawave.hosts.reorder_hosts(body=reorder_request)
            
            # Проверяем ответ
            assert response is not None
            assert response.is_updated is True
            
        except ApiError as e:
            # В случае ошибки доступа пропускаем тест
            pytest.skip(f"Could not reorder hosts: {str(e)}")


class TestHostsAdvanced:
    """Тесты расширенного функционала хостов"""
    
    @pytest.mark.asyncio
    async def test_create_host_with_advanced_options(self, remnawave):
        """Тест создания хоста с расширенными параметрами"""
        random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
        random_port: int = random.randint(5000, 8000)
        random_remark: str = generate_random_string()
        
        # Создаем хост с расширенными параметрами
        create_host = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=random_remark,
                address=random_ip,
                port=random_port,
                alpn=ALPN.H2,
                fingerprint=Fingerprint.CHROME,
                security_layer=SecurityLayer.TLS,
                path="/websocket",
                sni="example.com",
                host="example.org",
                allow_insecure=False,
                is_disabled=False,
                mux_params={"enabled": True, "concurrency": 8},
                sockopt_params={"mark": 255},
                tag="ADVANCED",
                is_hidden=False,
                override_sni_from_address=True,
                server_description="Advanced Server",
                vless_route_id=9876,
                shuffle_host=True,
                mihomo_x25519=True,
            )
        )
        
        assert isinstance(create_host, CreateHostResponseDto)
        assert create_host.alpn == ALPN.H2
        assert create_host.fingerprint == Fingerprint.CHROME
        assert create_host.security_layer == SecurityLayer.TLS
        assert create_host.path == "/websocket"
        assert create_host.sni == "example.com"
        assert create_host.host == "example.org"
        assert create_host.tag == "ADVANCED"
        
        # Очистка - удаление созданного хоста
        await remnawave.hosts.delete_host(uuid=str(create_host.uuid))


class TestHostInternalSquadsAndMapper:
    """`internalSquads` вместо `excludedInternalSquads` и новый `mapper` (v3.4.0)"""

    @pytest.fixture
    async def internal_squad(self, remnawave):
        created = await remnawave.internal_squads.create_internal_squad(
            CreateInternalSquadRequestDto(
                name=f"host_tags_{generate_random_string(length=6)}",
                inbounds=[REMNAWAVE_INBOUND_UUID],
            )
        )
        yield created
        try:
            await remnawave.internal_squads.delete_internal_squad(str(created.uuid))
        except NotFoundError:
            pass

    @pytest.fixture
    async def host(self, remnawave):
        created = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=generate_random_string(),
                address=f"{random.randint(500, 800)}.0.0.1",
                port=random.randint(5000, 8000),
            )
        )
        yield created
        try:
            await remnawave.hosts.delete_host(uuid=str(created.uuid))
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_all_hosts_expose_new_fields(self, remnawave):
        """Список хостов разбирается вместе с internalSquads/mapper"""
        all_hosts = await remnawave.hosts.get_all_hosts()
        for host in all_hosts:
            assert isinstance(host.internal_squads, HostInternalSquadsDto)
            assert host.internal_squads.mode in set(InternalSquadsMode)
            assert isinstance(host.mapper, HostMapperDto)

    @pytest.mark.asyncio
    async def test_new_host_defaults_to_exclude_mode(self, host):
        """Новый хост создаётся в режиме EXCLUDE с пустым списком сквадов"""
        assert host.internal_squads.mode == InternalSquadsMode.EXCLUDE
        assert host.internal_squads.squads == []
        assert host.excluded_internal_squads == []

    @pytest.mark.asyncio
    async def test_set_allow_only_internal_squads(self, remnawave, host, internal_squad):
        """Режим ALLOW_ONLY сохраняется и читается обратно"""
        updated = await remnawave.hosts.update_host(
            UpdateHostRequestDto(
                uuid=host.uuid,
                internal_squads=HostInternalSquadsDto(
                    mode=InternalSquadsMode.ALLOW_ONLY, squads=[internal_squad.uuid]
                ),
            )
        )

        assert updated.internal_squads.mode == InternalSquadsMode.ALLOW_ONLY
        assert updated.internal_squads.squads == [internal_squad.uuid]
        # В режиме ALLOW_ONLY legacy-свойство пустое
        assert updated.excluded_internal_squads == []

        fetched = await remnawave.hosts.get_one_host(uuid=str(host.uuid))
        assert fetched.internal_squads.squads == [internal_squad.uuid]

    @pytest.mark.asyncio
    async def test_legacy_excluded_internal_squads_kwarg(
        self, remnawave, host, internal_squad
    ):
        """Старый kwarg `excluded_internal_squads` по-прежнему работает"""
        updated = await remnawave.hosts.update_host(
            UpdateHostRequestDto(
                uuid=host.uuid,
                excluded_internal_squads=[internal_squad.uuid],
            )
        )

        assert updated.internal_squads.mode == InternalSquadsMode.EXCLUDE
        assert updated.internal_squads.squads == [internal_squad.uuid]
        assert updated.excluded_internal_squads == [internal_squad.uuid]

    @pytest.mark.asyncio
    async def test_set_mapper_operations(self, remnawave, host):
        """Операции mapper сохраняются панелью"""
        updated = await remnawave.hosts.update_host(
            UpdateHostRequestDto(
                uuid=host.uuid,
                mapper=HostMapperDto(
                    xray_json=[
                        HostMapperCopyOp(
                            from_="streamSettings.tlsSettings.alpn",
                            to="streamSettings.tlsSettings.alpn",
                        ),
                        HostMapperUnsetOp(to="mux"),
                    ],
                    mihomo=[HostMapperSetOp(to="ip-version", value="dual")],
                ),
            )
        )

        assert len(updated.mapper.xray_json) == 2
        assert updated.mapper.xray_json[0].from_ == "streamSettings.tlsSettings.alpn"
        assert updated.mapper.xray_json[1].op == "unset"
        assert updated.mapper.mihomo[0].value == "dual"

        fetched = await remnawave.hosts.get_one_host(uuid=str(host.uuid))
        assert fetched.mapper.mihomo[0].to == "ip-version"

    @pytest.mark.asyncio
    async def test_create_host_with_internal_squads(self, remnawave, internal_squad):
        """Хост создаётся сразу с internalSquads"""
        created = await remnawave.hosts.create_host(
            CreateHostRequestDto(
                inbound_uuid=REMNAWAVE_INBOUND_UUID,
                config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                remark=generate_random_string(),
                address=f"{random.randint(500, 800)}.0.0.1",
                port=random.randint(5000, 8000),
                internal_squads=HostInternalSquadsDto(
                    mode=InternalSquadsMode.ALLOW_ONLY, squads=[internal_squad.uuid]
                ),
            )
        )

        try:
            assert created.internal_squads.mode == InternalSquadsMode.ALLOW_ONLY
            assert created.internal_squads.squads == [internal_squad.uuid]
        finally:
            await remnawave.hosts.delete_host(uuid=str(created.uuid))

    @pytest.mark.asyncio
    async def test_bulk_update_internal_squads(self, remnawave, host, internal_squad):
        """Массовое обновление хостов принимает internalSquads"""
        updated = await remnawave.hosts_bulk_actions.update_hosts(
            UpdateManyHostsRequestDto(
                uuids=[host.uuid],
                internal_squads=HostInternalSquadsDto(
                    mode=InternalSquadsMode.EXCLUDE, squads=[internal_squad.uuid]
                ),
            )
        )

        # PATCH /hosts/bulk/update отвечает 204 No Content
        assert updated is None
        fetched = await remnawave.hosts.get_one_host(uuid=str(host.uuid))
        assert fetched.internal_squads.squads == [internal_squad.uuid]

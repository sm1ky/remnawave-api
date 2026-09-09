import random

import pytest

from remnawave.exceptions import NotFoundError
from remnawave.enums import NodeIpStatus
from remnawave.models import (
    BulkNodesUpdateFieldsDto,
    BulkNodesUpdateRequestDto,
    CreateNodeIntegrationRequestDto,
    NodeConfigProfileRequestDto,
    CreateNodeRequestDto,
    NodeIpDto,
    DeleteNodeResponseDto,
    GetAllNodesResponseDto,
    NodeResponseDto,
    NodesResponseDto,
    ReorderNodeRequestDto,
    ReorderNodeResponseDto,
    ResetNodeTrafficResponseDto,
    UpdateNodeRequestDto,
)
from remnawave.models.nodes import ReorderNodeItem
from tests.conftest import REMNAWAVE_CONFIG_PROFILE_UUID, REMNAWAVE_INBOUND_UUID
from tests.utils import generate_random_string


@pytest.mark.asyncio
async def test_nodes(remnawave):
    all_nodes = await remnawave.nodes.get_all_nodes()
    assert isinstance(all_nodes, GetAllNodesResponseDto)

    random_ip: str = f"{random.randint(500, 800)}" + ".0.0.1"
    random_port: int = random.randint(5000, 8000)
    random_name: str = generate_random_string()
    create_node = await remnawave.nodes.create_node(
        CreateNodeRequestDto(
            name=random_name, 
            address=random_ip, 
            port=random_port,
            config_profile=NodeConfigProfileRequestDto.model_validate({
                "activeConfigProfileUuid": str(REMNAWAVE_CONFIG_PROFILE_UUID),
                "activeInbounds": [str(REMNAWAVE_INBOUND_UUID)]
            })
        )
    )
    assert isinstance(create_node, NodeResponseDto)

    string_uuid = str(create_node.uuid)

    node = await remnawave.nodes.get_one_node(uuid=string_uuid)
    assert isinstance(node, NodeResponseDto)

    reorder_node = await remnawave.nodes.reorder_nodes(
        ReorderNodeRequestDto(
            nodes=[ReorderNodeItem(
                view_position=random.randint(1, 1000),
                uuid=create_node.uuid
            )]
        )
    )
    print(reorder_node)
    assert isinstance(reorder_node, ReorderNodeResponseDto)
    # assert any(node.uuid == create_node.uuid for node in reorder_node.root)

    update_name: str = generate_random_string()
    update_node = await remnawave.nodes.update_node(
        UpdateNodeRequestDto(uuid=string_uuid, name=update_name)
    )
    assert isinstance(update_node, NodeResponseDto)
    assert update_node.uuid == create_node.uuid
    assert update_node.name == update_name

    reset_traffic = await remnawave.nodes.reset_node_traffic(uuid=string_uuid)
    assert reset_traffic is None

    delete_node = await remnawave.nodes.delete_node(uuid=string_uuid)
    assert delete_node is None


class TestNodeIpsAndIntegrations:
    """`ips` и `integrationUuids` у ноды (Remnawave API v3.4.0+)"""

    @pytest.fixture
    async def node_integration(self, remnawave):
        created = await remnawave.node_integrations.create_node_integration(
            CreateNodeIntegrationRequestDto(
                name=f"ni_{generate_random_string(length=8)}",
                config={"kind": "test"},
            )
        )
        yield created
        try:
            await remnawave.node_integrations.delete_node_integration(uuid=str(created.uuid))
        except NotFoundError:
            pass

    @pytest.fixture
    async def node(self, remnawave):
        created = await remnawave.nodes.create_node(
            CreateNodeRequestDto(
                name=generate_random_string(),
                address=f"{random.randint(500, 800)}.0.0.1",
                port=random.randint(5000, 8000),
                config_profile=NodeConfigProfileRequestDto.model_validate(
                    {
                        "activeConfigProfileUuid": str(REMNAWAVE_CONFIG_PROFILE_UUID),
                        "activeInbounds": [str(REMNAWAVE_INBOUND_UUID)],
                    }
                ),
            )
        )
        yield created
        try:
            await remnawave.nodes.delete_node(uuid=str(created.uuid))
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_all_nodes_expose_new_fields(self, remnawave):
        """Список нод разбирается вместе с новыми полями"""
        all_nodes = await remnawave.nodes.get_all_nodes()
        for node in all_nodes:
            assert isinstance(node.integration_uuids, list)
            assert isinstance(node.ips, list)
            for ip in node.ips:
                assert isinstance(ip, NodeIpDto)
                assert ip.status in set(NodeIpStatus)

    @pytest.mark.asyncio
    async def test_new_node_has_empty_ips_and_integrations(self, node):
        """Новая нода приходит без IP и интеграций"""
        assert node.ips == []
        assert node.integration_uuids == []

    @pytest.mark.asyncio
    async def test_update_node_ips(self, remnawave, node):
        """IP-адреса ноды сохраняются и читаются обратно"""
        updated = await remnawave.nodes.update_node(
            UpdateNodeRequestDto(
                uuid=node.uuid,
                ips=[
                    NodeIpDto(ip="203.0.113.10", status=NodeIpStatus.INBOUND),
                    NodeIpDto(ip="203.0.113.11", status=NodeIpStatus.OUTBOUND),
                ],
            )
        )

        assert [ip.ip for ip in updated.ips] == ["203.0.113.10", "203.0.113.11"]
        assert [ip.status for ip in updated.ips] == [
            NodeIpStatus.INBOUND,
            NodeIpStatus.OUTBOUND,
        ]

        fetched = await remnawave.nodes.get_one_node(uuid=str(node.uuid))
        assert [ip.ip for ip in fetched.ips] == ["203.0.113.10", "203.0.113.11"]

    @pytest.mark.asyncio
    async def test_update_node_integration_uuids(self, remnawave, node, node_integration):
        """Интеграции привязываются к ноде"""
        updated = await remnawave.nodes.update_node(
            UpdateNodeRequestDto(uuid=node.uuid, integration_uuids=[node_integration.uuid])
        )

        assert updated.integration_uuids == [node_integration.uuid]

        fetched = await remnawave.nodes.get_one_node(uuid=str(node.uuid))
        assert fetched.integration_uuids == [node_integration.uuid]

    @pytest.mark.asyncio
    async def test_create_node_with_ips_and_integration(
        self, remnawave, node_integration
    ):
        """Нода создаётся сразу с IP и интеграцией"""
        created = await remnawave.nodes.create_node(
            CreateNodeRequestDto(
                name=generate_random_string(),
                address=f"{random.randint(500, 800)}.0.0.1",
                port=random.randint(5000, 8000),
                config_profile=NodeConfigProfileRequestDto.model_validate(
                    {
                        "activeConfigProfileUuid": str(REMNAWAVE_CONFIG_PROFILE_UUID),
                        "activeInbounds": [str(REMNAWAVE_INBOUND_UUID)],
                    }
                ),
                integration_uuids=[node_integration.uuid],
                ips=[NodeIpDto(ip="2001:db8::1", status=NodeIpStatus.MANAGEMENT)],
            )
        )

        try:
            assert created.integration_uuids == [node_integration.uuid]
            assert [ip.ip for ip in created.ips] == ["2001:db8::1"]
            assert created.ips[0].status == NodeIpStatus.MANAGEMENT
        finally:
            await remnawave.nodes.delete_node(uuid=str(created.uuid))

    @pytest.mark.asyncio
    async def test_bulk_update_integration_uuids(self, remnawave, node, node_integration):
        """Массовое обновление умеет проставлять integrationUuids"""
        response = await remnawave.nodes.bulk_nodes_update(
            BulkNodesUpdateRequestDto(
                uuids=[node.uuid],
                fields=BulkNodesUpdateFieldsDto(integration_uuids=[node_integration.uuid]),
            )
        )
        assert response is None or getattr(response, "event_sent", True)

        fetched = await remnawave.nodes.get_one_node(uuid=str(node.uuid))
        assert fetched.integration_uuids == [node_integration.uuid]

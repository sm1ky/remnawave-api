import random

import pytest

from remnawave.models import (
    NodeConfigProfileRequestDto,
    CreateNodeRequestDto,
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

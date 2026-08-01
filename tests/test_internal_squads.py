from uuid import UUID
import pytest

from remnawave.models import (
    AddUsersToInternalSquadRequestDto,
    AddUsersToInternalSquadResponseDto,
    CreateInternalSquadRequestDto,
    CreateInternalSquadResponseDto,
    DeleteInternalSquadResponseDto,
    DeleteUsersFromInternalSquadRequestDto,
    DeleteUsersFromInternalSquadResponseDto,
    GetAllInternalSquadsResponseDto,
    GetInternalSquadByUuidResponseDto,
    ReorderInternalSquadItem,
    ReorderInternalSquadsRequestDto,
    ReorderInternalSquadsResponseDto,
    UpdateInternalSquadRequestDto,
    UpdateInternalSquadResponseDto,
)
from tests.conftest import REMNAWAVE_INBOUND_UUID
from tests.utils import generate_random_string


@pytest.mark.asyncio
async def test_internal_squads(remnawave) -> None:
    squad_name = f"test_squad_{generate_random_string(length=6)}"
    
    # Test create internal squad
    create_squad = await remnawave.internal_squads.create_internal_squad(
        CreateInternalSquadRequestDto(name=squad_name, inbounds=[
            REMNAWAVE_INBOUND_UUID
        ])
    )
    
    assert isinstance(create_squad, CreateInternalSquadResponseDto)
    assert create_squad.name == squad_name

    squad_uuid = str(create_squad.uuid)

    # Test get all internal squads
    all_squads = await remnawave.internal_squads.get_internal_squads()
    assert isinstance(all_squads, GetAllInternalSquadsResponseDto)
    assert len(all_squads.internal_squads) > 0
    
    # Test get internal squad by uuid
    squad_by_uuid = await remnawave.internal_squads.get_internal_squad_by_uuid(squad_uuid)
    assert isinstance(squad_by_uuid, GetInternalSquadByUuidResponseDto)
    assert squad_by_uuid.name == squad_name

    # Test update internal squad
    update_squad = await remnawave.internal_squads.update_internal_squad(
        UpdateInternalSquadRequestDto(
            uuid=create_squad.uuid,
            inbounds=[REMNAWAVE_INBOUND_UUID], 
        )
    )
    
    assert isinstance(update_squad, UpdateInternalSquadResponseDto)
    assert update_squad.inbounds[0].uuid == UUID(REMNAWAVE_INBOUND_UUID)

    # Test add users to internal squad (with dummy UUIDs for testing)
    dummy_user_uuids = []  # Empty list for test
    add_users = await remnawave.internal_squads.add_users_to_internal_squad(
        squad_uuid,
    )
    
    assert add_users is None
    
    # Test remove users from internal squad
    remove_users = await remnawave.internal_squads.remove_users_from_internal_squad(
        squad_uuid,
    )
    
    assert remove_users is None

    # Test reorder internal squads
    all_squads = await remnawave.internal_squads.get_internal_squads()
    if len(all_squads.internal_squads) >= 2:
        items = [
            ReorderInternalSquadItem(
                uuid=squad.uuid,
                view_position=idx
            )
            for idx, squad in enumerate(all_squads.internal_squads)
        ]
        reorder_result = await remnawave.internal_squads.reorder_internal_squads(
            ReorderInternalSquadsRequestDto(items=items)
        )
        assert isinstance(reorder_result, ReorderInternalSquadsResponseDto)
    
    # Test delete internal squad
    delete_squad = await remnawave.internal_squads.delete_internal_squad(squad_uuid)
    assert delete_squad is None

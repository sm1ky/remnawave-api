from datetime import datetime, timedelta
from uuid import UUID

import pytest
import pytz

from remnawave.exceptions import ApiError, NotFoundError
from remnawave.models import (
    CreateUserBodyDto,
    GetInternalSquadAccessibleNodesResponseDto,
    GetInternalSquadUsageResponseDto,
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
from remnawave.models.internal_squads import (
    AddManyUsersToInternalSquadBodyDto,
    DeleteManyUsersFromInternalSquadBodyDto,
)
from tests.conftest import REMNAWAVE_INBOUND_UUID
from tests.utils import generate_date_range, generate_random_string


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


@pytest.fixture
async def squad(remnawave):
    created = await remnawave.internal_squads.create_internal_squad(
        CreateInternalSquadRequestDto(
            name=f"squad_{generate_random_string(length=6)}",
            inbounds=[REMNAWAVE_INBOUND_UUID],
        )
    )
    yield created
    try:
        await remnawave.internal_squads.delete_internal_squad(str(created.uuid))
    except NotFoundError:
        pass


class TestInternalSquadAccessibleNodes:
    @pytest.mark.asyncio
    async def test_get_accessible_nodes(self, remnawave, squad):
        response = await remnawave.internal_squads.get_accessible_nodes(str(squad.uuid))

        assert isinstance(response, GetInternalSquadAccessibleNodesResponseDto)
        assert response.squad_uuid == squad.uuid
        assert isinstance(response.accessible_nodes, list)

    @pytest.mark.asyncio
    async def test_accessible_nodes_are_real_nodes(self, remnawave, squad):
        """Каждая выданная нода существует в панели"""
        response = await remnawave.internal_squads.get_accessible_nodes(str(squad.uuid))
        known = {n.uuid for n in await remnawave.nodes.get_all_nodes()}

        for node in response.accessible_nodes:
            assert node.uuid in known


class TestInternalSquadMembership:
    """Точечное добавление и удаление участников по списку id"""

    @pytest.fixture
    async def users(self, remnawave):
        expire_at = datetime.now(tz=pytz.utc) + timedelta(days=7)
        created = [
            await remnawave.users.create_user(
                CreateUserBodyDto(
                    username=f"sq_{generate_random_string(length=10)}", expire_at=expire_at
                )
            )
            for _ in range(2)
        ]
        yield created
        for user in created:
            try:
                await remnawave.users.delete_user(user_id=user.id)
            except NotFoundError:
                pass

    @pytest.mark.asyncio
    async def test_add_then_remove_many_users(self, remnawave, squad, users):
        user_ids = [u.id for u in users]

        added = await remnawave.internal_squads.add_many_users_to_internal_squad(
            str(squad.uuid), AddManyUsersToInternalSquadBodyDto(user_ids=user_ids)
        )
        assert added is None

        for user in users:
            fetched = await remnawave.users.get_user_by_id(user_id=user.id)
            assert squad.uuid in [s.uuid for s in fetched.active_internal_squads]

        removed = await remnawave.internal_squads.remove_many_users_from_internal_squad(
            str(squad.uuid), DeleteManyUsersFromInternalSquadBodyDto(user_ids=user_ids)
        )
        assert removed is None

        for user in users:
            fetched = await remnawave.users.get_user_by_id(user_id=user.id)
            assert squad.uuid not in [s.uuid for s in fetched.active_internal_squads]

    @pytest.mark.asyncio
    async def test_members_count_reflects_membership(self, remnawave, squad, users):
        """Счётчик участников сквада растёт и возвращается обратно"""
        before = (await remnawave.internal_squads.get_internal_squad_by_uuid(str(squad.uuid))).info.members_count

        await remnawave.internal_squads.add_many_users_to_internal_squad(
            str(squad.uuid), AddManyUsersToInternalSquadBodyDto(user_ids=[u.id for u in users])
        )
        during = (await remnawave.internal_squads.get_internal_squad_by_uuid(str(squad.uuid))).info.members_count
        assert during == before + len(users)

        await remnawave.internal_squads.remove_many_users_from_internal_squad(
            str(squad.uuid), DeleteManyUsersFromInternalSquadBodyDto(user_ids=[u.id for u in users])
        )
        after = (await remnawave.internal_squads.get_internal_squad_by_uuid(str(squad.uuid))).info.members_count
        assert after == before


class TestInternalSquadUsage:
    @pytest.mark.asyncio
    async def test_get_internal_squad_usage(self, remnawave, squad):
        start, end = generate_date_range()
        response = await remnawave.internal_squads.get_internal_squad_usage(
            str(squad.uuid), start=start, end=end
        )

        assert isinstance(response, GetInternalSquadUsageResponseDto)
        assert response.squad_uuid == squad.uuid

    @pytest.mark.asyncio
    async def test_usage_requires_a_range(self, remnawave, squad):
        """start/end обязательны по контракту — панель отвергает запрос без них"""
        with pytest.raises(ApiError):
            await remnawave.internal_squads.get_internal_squad_usage(
                str(squad.uuid), start="", end=""
            )

    @pytest.mark.asyncio
    async def test_same_usage_via_bandwidth_stats(self, remnawave, squad):
        """Тот же отчёт доступен через bandwidth-stats"""
        start, end = generate_date_range()
        via_squads = await remnawave.internal_squads.get_internal_squad_usage(
            str(squad.uuid), start=start, end=end
        )
        via_stats = await remnawave.bandwidthstats.get_internal_squad_usage(
            str(squad.uuid), start=start, end=end
        )

        assert via_stats.squad_uuid == via_squads.squad_uuid

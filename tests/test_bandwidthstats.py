import pytest

from pydantic import ValidationError

from remnawave.exceptions import ApiError
from remnawave.models import (
    # Legacy models (deprecated)
    GetNodesUsageByRangeResponseDto,

    # New stats models
    FetchNodesUsageBodyDto,
    FetchNodesUsageResponseDto,
    GetInternalSquadUsageResponseDto,
    GetInternalSquadUserUsageResponseDto,
    GetStatsNodesUsageResponseDto,
    GetStatsNodesUsersUsageRequestDto,
    GetStatsNodesUsersUsageResponseDto,
    GetStatsNodeUsersUsageResponseDto,
    GetStatsUserUsageResponseDto,
)
from tests.utils import generate_date_range, generate_isoformat_range



@pytest.mark.asyncio
async def test_stats_nodes_usage(remnawave):
    """Test new stats nodes usage endpoint with charts"""
    start, end = generate_date_range()
    
    nodes_usage = await remnawave.bandwidthstats.get_stats_nodes_usage(
        start=start,
        end=end,
        top_nodes_limit=5
    )
    assert isinstance(nodes_usage, GetStatsNodesUsageResponseDto)
    assert hasattr(nodes_usage, 'response')
    assert hasattr(nodes_usage.response, 'categories')
    assert hasattr(nodes_usage.response, 'sparkline_data')
    assert hasattr(nodes_usage.response, 'top_nodes')
    assert hasattr(nodes_usage.response, 'series')
    
    # Check data types
    assert isinstance(nodes_usage.response.categories, list)
    assert isinstance(nodes_usage.response.sparkline_data, list)
    assert isinstance(nodes_usage.response.top_nodes, list)
    assert isinstance(nodes_usage.response.series, list)


@pytest.mark.asyncio
async def test_stats_node_users_usage(remnawave):
    """Test new stats node users usage endpoint"""
    # Get first node
    nodes = await remnawave.nodes.get_all_nodes()
    if not nodes:
        pytest.skip("No nodes available for testing")
    
    node_uuid = str(nodes[0].uuid)
    start, end = generate_date_range()
    
    node_users_usage = await remnawave.bandwidthstats.get_stats_node_users_usage(
        uuid=node_uuid,
        start=start,
        end=end,
        top_users_limit=5
    )
    assert isinstance(node_users_usage, GetStatsNodeUsersUsageResponseDto)
    assert hasattr(node_users_usage, 'response')
    assert hasattr(node_users_usage.response, 'categories')
    assert hasattr(node_users_usage.response, 'sparkline_data')
    assert hasattr(node_users_usage.response, 'top_users')
    
    # Check data types
    assert isinstance(node_users_usage.response.categories, list)
    assert isinstance(node_users_usage.response.sparkline_data, list)
    assert isinstance(node_users_usage.response.top_users, list)


@pytest.mark.asyncio
async def test_stats_user_usage(remnawave):
    """Test new stats user usage endpoint"""
    # Get first user
    users = await remnawave.users.get_all_users()
    if not users.users:
        pytest.skip("No users available for testing")
    
    user_id = users.users[0].id
    start, end = generate_date_range()

    user_usage = await remnawave.bandwidthstats.get_stats_user_usage(
        user_id=user_id,
        start=start,
        end=end,
        top_nodes_limit=5
    )
    assert isinstance(user_usage, GetStatsUserUsageResponseDto)
    assert hasattr(user_usage, 'response')
    assert hasattr(user_usage.response, 'categories')
    assert hasattr(user_usage.response, 'sparkline_data')
    assert hasattr(user_usage.response, 'top_nodes')
    assert hasattr(user_usage.response, 'series')
    
    # Check data types
    assert isinstance(user_usage.response.categories, list)
    assert isinstance(user_usage.response.sparkline_data, list)
    assert isinstance(user_usage.response.top_nodes, list)
    assert isinstance(user_usage.response.series, list)




@pytest.mark.asyncio
async def test_bandwidth_data_structure(remnawave):
    """Test bandwidth stats data structure validity"""
    start, end = generate_date_range()

    # Get stats data
    stats = await remnawave.bandwidthstats.get_stats_nodes_usage(
        start=start,
        end=end,
        top_nodes_limit=3
    )
    
    # Verify stats structure
    assert len(stats.response.categories) == len(stats.response.sparkline_data)
    assert len(stats.response.top_nodes) <= 3
    
    if stats.response.series:
        for series_item in stats.response.series:
            assert len(series_item.data) == len(stats.response.categories)

@pytest.fixture
async def node_uuids(remnawave):
    nodes = await remnawave.nodes.get_all_nodes()
    if not len(nodes):
        pytest.skip("В окружении нет ни одной ноды")
    return [n.uuid for n in nodes]


class TestNodesUsersUsage:
    @pytest.mark.asyncio
    async def test_get_stats_nodes_users_usage(self, remnawave, node_uuids):
        start, end = generate_date_range()

        response = await remnawave.bandwidthstats.get_stats_nodes_users_usage(
            body=GetStatsNodesUsersUsageRequestDto(nodes_uuids=node_uuids),
            start=start,
            end=end,
        )

        assert isinstance(response, GetStatsNodesUsersUsageResponseDto)

    def test_empty_node_list_is_rejected_client_side(self):
        """Пустой список нод отсекается моделью, запрос до панели не доходит"""
        with pytest.raises(ValidationError):
            GetStatsNodesUsersUsageRequestDto(nodes_uuids=[])


class TestFetchNodesUsage:
    @pytest.mark.asyncio
    async def test_fetch_nodes_usage(self, remnawave, node_uuids):
        start, end = generate_date_range()

        response = await remnawave.bandwidthstats.fetch_nodes_usage(
            body=FetchNodesUsageBodyDto(nodes_uuids=node_uuids),
            start=start,
            end=end,
        )

        assert isinstance(response, FetchNodesUsageResponseDto)

    @pytest.mark.asyncio
    async def test_min_total_bytes_filter(self, remnawave, node_uuids):
        """Недостижимый порог трафика отсекает всех пользователей"""
        start, end = generate_date_range()

        response = await remnawave.bandwidthstats.fetch_nodes_usage(
            body=FetchNodesUsageBodyDto(nodes_uuids=node_uuids),
            start=start,
            end=end,
            min_total_bytes=10**18,
        )

        assert not (response.nodes or [])


class TestInternalSquadUsageStats:
    @pytest.fixture
    async def squad(self, remnawave):
        squads = await remnawave.internal_squads.get_internal_squads()
        if not squads.internal_squads:
            pytest.skip("В окружении нет внутренних сквадов")
        return squads.internal_squads[0]

    @pytest.mark.asyncio
    async def test_squad_usage(self, remnawave, squad):
        start, end = generate_date_range()

        response = await remnawave.bandwidthstats.get_internal_squad_usage(
            str(squad.uuid), start=start, end=end
        )

        assert isinstance(response, GetInternalSquadUsageResponseDto)
        assert response.squad_uuid == squad.uuid

    @pytest.mark.asyncio
    async def test_squad_user_usage(self, remnawave, squad):
        """Посуточная разбивка по конкретному пользователю сквада"""
        start, end = generate_date_range()
        users = await remnawave.users.get_all_users(size=1)
        if not users.users:
            pytest.skip("В окружении нет ни одного пользователя")

        response = await remnawave.bandwidthstats.get_internal_squad_user_usage(
            squad_uuid=str(squad.uuid),
            user_id=users.users[0].id,
            start=start,
            end=end,
        )

        assert isinstance(response, GetInternalSquadUserUsageResponseDto)
        assert isinstance(response.days or [], list)

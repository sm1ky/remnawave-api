import pytest

from remnawave.models import (
    # Legacy models (deprecated)
    GetNodesUsageByRangeResponseDto,

    # New stats models
    GetStatsNodesUsageResponseDto,
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
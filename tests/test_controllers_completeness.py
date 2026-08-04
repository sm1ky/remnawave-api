"""Tests that all required endpoints exist in controllers (Remnawave API v3.0.0)."""
import pytest

from remnawave.controllers.users import UsersController
from remnawave.controllers.system import SystemController
from remnawave.controllers.connections import ConnectionsController
from remnawave.controllers.api_tokens_management import APITokensManagementController
from remnawave.controllers.hosts_bulk_actions import HostsBulkActionsController
from remnawave.controllers.bandwidthstats import BandWidthStatsController
from remnawave.controllers.internal_squads import InternalSquadsController


class TestUsersControllerEndpoints:
    def test_has_resolve_user(self):
        assert hasattr(UsersController, "resolve_user")

    def test_has_revoke_user_subscription(self):
        assert hasattr(UsersController, "revoke_user_subscription")

    def test_has_disable_user(self):
        assert hasattr(UsersController, "disable_user")

    def test_has_enable_user(self):
        assert hasattr(UsersController, "enable_user")

    def test_has_reset_user_traffic(self):
        assert hasattr(UsersController, "reset_user_traffic")

    def test_has_create_user(self):
        assert hasattr(UsersController, "create_user")

    def test_has_update_user(self):
        assert hasattr(UsersController, "update_user")

    def test_has_delete_user(self):
        assert hasattr(UsersController, "delete_user")

    def test_has_get_all_users(self):
        assert hasattr(UsersController, "get_all_users")

    def test_has_get_user_by_id(self):
        assert hasattr(UsersController, "get_user_by_id")

    def test_has_get_user_by_short_uuid(self):
        assert hasattr(UsersController, "get_user_by_short_uuid")

    def test_has_get_user_by_username(self):
        assert hasattr(UsersController, "get_user_by_username")

    def test_has_get_all_tags(self):
        assert hasattr(UsersController, "get_all_tags")

    def test_has_get_user_accessible_nodes(self):
        assert hasattr(UsersController, "get_user_accessible_nodes")

    def test_has_get_user_subscription_request_history(self):
        assert hasattr(UsersController, "get_user_subscription_request_history")

    def test_has_get_users_stream(self):
        assert hasattr(UsersController, "get_users_stream")

    def test_has_extend_user(self):
        # New in v3.0.0
        assert hasattr(UsersController, "extend_user")

    def test_no_removed_user_lookups(self):
        # Removed in v3.0.0 (use /users/stream filters or get_user_by_id)
        assert not hasattr(UsersController, "get_user_by_uuid")
        assert not hasattr(UsersController, "get_users_by_telegram_id")
        assert not hasattr(UsersController, "get_users_by_email")
        assert not hasattr(UsersController, "get_users_by_tag")


class TestSystemControllerEndpoints:
    def test_has_get_recap(self):
        assert hasattr(SystemController, "get_recap")

    def test_has_get_metadata(self):
        assert hasattr(SystemController, "get_metadata")

    def test_has_get_stats(self):
        assert hasattr(SystemController, "get_stats")

    def test_has_get_bandwidth_stats(self):
        assert hasattr(SystemController, "get_bandwidth_stats")

    def test_has_get_nodes_statistics(self):
        assert hasattr(SystemController, "get_nodes_statistics")

    def test_has_get_health(self):
        assert hasattr(SystemController, "get_health")

    def test_has_get_nodes_metrics(self):
        assert hasattr(SystemController, "get_nodes_metrics")

    def test_has_get_x25519_key_pair(self):
        assert hasattr(SystemController, "get_x25519_key_pair")

    def test_has_debug_srr_matcher(self):
        assert hasattr(SystemController, "debug_srr_matcher")

    def test_has_new_stats_digest_http(self):
        # New in v3.0.0
        assert hasattr(SystemController, "get_stats_digest")
        assert hasattr(SystemController, "get_http_stats")

    def test_has_get_configuration(self):
        # New in v3.2.0
        assert hasattr(SystemController, "get_configuration")


class TestApiTokensControllerEndpoints:
    def test_has_get_scopes(self):
        assert hasattr(APITokensManagementController, "get_scopes")


class TestHostsBulkActionsControllerEndpoints:
    def test_has_update_hosts(self):
        assert hasattr(HostsBulkActionsController, "update_hosts")

    def test_no_set_inbound_to_hosts(self):
        assert not hasattr(HostsBulkActionsController, "set_inbound_to_hosts")

    def test_no_set_port_to_hosts(self):
        assert not hasattr(HostsBulkActionsController, "set_port_to_hosts")


class TestBandwidthStatsControllerEndpoints:
    def test_has_get_stats_nodes_users_usage(self):
        assert hasattr(BandWidthStatsController, "get_stats_nodes_users_usage")

    def test_has_new_usage_endpoints(self):
        # New in v3.0.0
        assert hasattr(BandWidthStatsController, "fetch_nodes_usage")
        assert hasattr(BandWidthStatsController, "get_internal_squad_usage")

    def test_no_legacy_endpoints(self):
        # Removed in v3.0.0
        assert not hasattr(BandWidthStatsController, "get_user_usage_legacy_stats")
        assert not hasattr(BandWidthStatsController, "get_nodes_realtime_usage")


class TestConnectionsControllerEndpoints:
    """Renamed from ip-control in v3.0.0."""

    def test_has_fetch_connections_by_user(self):
        assert hasattr(ConnectionsController, "fetch_connections_by_user")

    def test_has_get_connections_by_user(self):
        assert hasattr(ConnectionsController, "get_connections_by_user")

    def test_has_fetch_connections_by_node(self):
        assert hasattr(ConnectionsController, "fetch_connections_by_node")

    def test_has_get_connections_by_node(self):
        assert hasattr(ConnectionsController, "get_connections_by_node")

    def test_has_drop_connections(self):
        assert hasattr(ConnectionsController, "drop_connections")


class TestInternalSquadsControllerEndpoints:
    def test_has_add_many_users(self):
        # New in v3.0.0
        assert hasattr(InternalSquadsController, "add_many_users_to_internal_squad")

    def test_has_remove_many_users(self):
        # New in v3.0.0
        assert hasattr(InternalSquadsController, "remove_many_users_from_internal_squad")

"""Tests for enum completeness against the OpenAPI spec."""
import pytest

from remnawave.enums import (
    ALPN,
    ClientType,
    ErrorCode,
    Fingerprint,
    HostMapperOperation,
    InternalSquadsMode,
    NodeIpStatus,
    OAuth2Provider,
    SecurityLayer,
    TemplateType,
    TrafficLimitStrategy,
    UserStatus,
    ResponseRuleConditionOperator,
    ResponseRuleOperator,
    ResponseRuleVersion,
    ResponseType,
    SubscriptionType,
    TTorrentBlockerEvents,
)


class TestOAuth2Provider:
    def test_has_telegram(self):
        assert OAuth2Provider.TELEGRAM == "telegram"

    def test_has_generic(self):
        assert OAuth2Provider.GENERIC == "generic"

    def test_has_github(self):
        assert OAuth2Provider.GITHUB == "github"

    def test_has_pocketid(self):
        assert OAuth2Provider.POCKETID == "pocketid"

    def test_has_yandex(self):
        assert OAuth2Provider.YANDEX == "yandex"

    def test_has_keycloak(self):
        assert OAuth2Provider.KEYCLOAK == "keycloak"

    def test_all_values(self):
        expected = {"telegram", "github", "pocketid", "yandex", "keycloak", "generic"}
        actual = {v.value for v in OAuth2Provider}
        assert actual == expected


class TestTemplateType:
    def test_has_xray_base64(self):
        assert TemplateType.XRAY_BASE64 == "XRAY_BASE64"

    def test_has_xray_json(self):
        assert TemplateType.XRAY_JSON == "XRAY_JSON"

    def test_all_api_values(self):
        api_values = {"XRAY_JSON", "XRAY_BASE64", "MIHOMO", "STASH", "CLASH", "SINGBOX"}
        actual = {v.value for v in TemplateType}
        assert api_values.issubset(actual)


class TestTrafficLimitStrategy:
    def test_has_month_rolling(self):
        assert TrafficLimitStrategy.MONTH_ROLLING == "MONTH_ROLLING"

    def test_all_api_values(self):
        api_values = {"NO_RESET", "DAY", "WEEK", "MONTH", "MONTH_ROLLING"}
        actual = {v.value for v in TrafficLimitStrategy}
        assert api_values == actual


class TestUserStatus:
    def test_all_values(self):
        expected = {"ACTIVE", "DISABLED", "LIMITED", "EXPIRED"}
        actual = {v.value for v in UserStatus}
        assert actual == expected


class TestClientType:
    def test_api_values_present(self):
        api_values = {"stash", "singbox", "mihomo", "json", "v2ray-json", "clash"}
        actual = {v.value for v in ClientType}
        assert api_values.issubset(actual)


class TestSecurityLayer:
    def test_all_values(self):
        expected = {"DEFAULT", "TLS", "NONE"}
        actual = {v.value for v in SecurityLayer}
        assert actual == expected


class TestFingerprint:
    def test_all_api_values(self):
        api_values = {"chrome", "firefox", "safari", "ios", "android", "edge", "qq", "random", "randomized"}
        actual = {v.value for v in Fingerprint}
        assert api_values == actual


class TestALPN:
    def test_has_h3(self):
        assert "h3" in {v.value for v in ALPN}

    def test_has_h2(self):
        assert "h2" in {v.value for v in ALPN}


class TestResponseRuleOperator:
    def test_all_values(self):
        expected = {"AND", "OR"}
        actual = {v.value for v in ResponseRuleOperator}
        assert actual == expected


class TestResponseRuleConditionOperator:
    def test_all_values(self):
        expected = {
            "EQUALS", "NOT_EQUALS", "CONTAINS", "NOT_CONTAINS",
            "STARTS_WITH", "NOT_STARTS_WITH", "ENDS_WITH", "NOT_ENDS_WITH",
            "REGEX", "NOT_REGEX",
        }
        actual = {v.value for v in ResponseRuleConditionOperator}
        assert actual == expected


class TestResponseType:
    def test_all_values(self):
        expected = {
            "XRAY_JSON", "XRAY_BASE64", "MIHOMO", "STASH", "CLASH", "SINGBOX",
            "BROWSER", "BLOCK", "STATUS_CODE_404", "STATUS_CODE_451", "SOCKET_DROP",
        }
        actual = {v.value for v in ResponseType}
        assert actual == expected


class TestInternalSquadsMode:
    """Host `internalSquads.mode` (Remnawave API v3.4.0+)."""

    def test_all_values(self):
        assert {mode.value for mode in InternalSquadsMode} == {"EXCLUDE", "ALLOW_ONLY"}


class TestHostMapperOperation:
    """Host mapper operations (Remnawave API v3.4.0+)."""

    def test_all_values(self):
        assert {op.value for op in HostMapperOperation} == {"copy", "set", "unset"}


class TestNodeIpStatus:
    """Node IP roles (Remnawave API v3.4.0+)."""

    def test_all_api_values(self):
        assert {status.value for status in NodeIpStatus} == {
            "INBOUND",
            "OUTBOUND",
            "MANAGEMENT",
            "TRANSIT",
            "MONITORING",
            "RESERVE",
            "BLOCKED",
            "FLAGGED",
            "DEPRECATED",
            "UNKNOWN",
        }


class TestErrorCodesV340:
    """Error codes introduced by Remnawave API v3.4.0."""

    @pytest.mark.parametrize(
        "member, code",
        [
            ("SYNC_SNIPPET_ERROR", "A237"),
            ("NODE_INTEGRATION_NOT_FOUND", "A238"),
            ("GET_ALL_NODE_INTEGRATIONS_ERROR", "A239"),
            ("GET_NODE_INTEGRATION_BY_UUID_ERROR", "A240"),
            ("CREATE_NODE_INTEGRATION_ERROR", "A241"),
            ("UPDATE_NODE_INTEGRATION_ERROR", "A242"),
            ("DELETE_NODE_INTEGRATION_ERROR", "A243"),
            ("NODE_INTEGRATION_NAME_ALREADY_EXISTS", "A244"),
            ("SHARED_LIST_NOT_FOUND", "A245"),
            ("SHARED_LIST_NAME_ALREADY_EXISTS", "A246"),
            ("GET_ALL_SHARED_LISTS_ERROR", "A247"),
            ("GET_SHARED_LIST_BY_NAME_ERROR", "A248"),
            ("CREATE_SHARED_LIST_ERROR", "A249"),
            ("UPDATE_SHARED_LIST_ERROR", "A250"),
            ("DELETE_SHARED_LIST_ERROR", "A251"),
            ("CREATE_SSH_TICKET_ERROR", "A254"),
            ("GET_TAGS_ERROR", "A256"),
            ("SET_TAGS_ERROR", "A257"),
        ],
    )
    def test_code_value(self, member, code):
        assert getattr(ErrorCode, member).value == code

    def test_codes_are_mapped_to_exceptions(self):
        from remnawave.exceptions import ConflictError, NotFoundError, ServerError
        from remnawave.exceptions.handler import ERRORS

        assert ERRORS[ErrorCode.NODE_INTEGRATION_NOT_FOUND] is NotFoundError
        assert ERRORS[ErrorCode.SHARED_LIST_NOT_FOUND] is NotFoundError
        assert ERRORS[ErrorCode.NODE_INTEGRATION_NAME_ALREADY_EXISTS] is ConflictError
        assert ERRORS[ErrorCode.SHARED_LIST_NAME_ALREADY_EXISTS] is ConflictError
        assert ERRORS[ErrorCode.SET_TAGS_ERROR] is ServerError

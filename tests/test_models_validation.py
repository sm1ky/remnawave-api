"""Tests for model field validation and serialization."""
import pytest
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import ValidationError

from remnawave.models import (
    # Users
    ResolveUserRequestBodyDto,
    ResolveUserResponseDto,
    RevokeUserRequestDto,
    # System
    GetRecapResponseDto,
    RecapThisMonth,
    RecapTotal,
    # IP Control
    FetchUsersIpsResponseDto,
    FetchUsersIpsResultResponseDto,
    FetchUsersIpsUserIp,
    FetchUsersIpsUser,
    FetchUsersIpsResult,
    DropConnectionsRequestDto,
    DropByUserUuids,
    DropByIpAddresses,
    TargetAllNodes,
    TargetSpecificNodes,
    # Infra Billing
    CreateInfraBillingHistoryRecordRequestDto,
    CreateInfraBillingNodeRequestDto,
    # Subscription Settings
    ResponseRules,
    ResponseRulesSettings,
    # Webhook
    NodeSystemDto,
    NodeSystemInfoDto,
    NodeSystemStatsDto,
    NodeVersionsDto,
)
from remnawave.enums import ResponseRuleVersion


class TestResolveUserRequestBodyDto:
    def test_create_with_uuid(self):
        uid = uuid4()
        dto = ResolveUserRequestBodyDto(uuid=uid)
        assert dto.uuid == uid
        assert dto.id is None
        assert dto.username is None

    def test_create_with_username(self):
        dto = ResolveUserRequestBodyDto(username="testuser")
        assert dto.username == "testuser"
        assert dto.uuid is None

    def test_create_with_short_uuid(self):
        dto = ResolveUserRequestBodyDto(short_uuid="abc123")
        assert dto.short_uuid == "abc123"

    def test_serialization_alias(self):
        dto = ResolveUserRequestBodyDto(short_uuid="abc123")
        data = dto.model_dump(by_alias=True)
        assert "shortUuid" in data

    def test_create_with_id(self):
        dto = ResolveUserRequestBodyDto(id=42)
        assert dto.id == 42


class TestResolveUserResponseDto:
    def test_from_api_response(self):
        uid = uuid4()
        dto = ResolveUserResponseDto(
            uuid=uid,
            username="testuser",
            id=1,
            shortUuid="abc123",
        )
        assert dto.uuid == uid
        assert dto.username == "testuser"
        assert dto.id == 1
        assert dto.short_uuid == "abc123"


class TestGetRecapResponseDto:
    def test_from_api_response(self):
        dto = GetRecapResponseDto(
            thisMonth={"users": 10, "traffic": "1.5 GB"},
            total={
                "users": 100,
                "nodes": 5,
                "traffic": "500 GB",
                "nodesRam": "32 GB",
                "nodesCpuCores": 16,
                "distinctCountries": 3,
            },
            version="1.11.0",
            initDate="2025-01-01T00:00:00Z",
        )
        assert dto.this_month.users == 10
        assert dto.this_month.traffic == "1.5 GB"
        assert dto.total.nodes == 5
        assert dto.total.nodes_ram == "32 GB"
        assert dto.total.nodes_cpu_cores == 16
        assert dto.total.distinct_countries == 3
        assert dto.version == "1.11.0"
        assert isinstance(dto.init_date, datetime)


class TestFetchUsersIpsModels:
    def test_response_dto(self):
        dto = FetchUsersIpsResponseDto(jobId="job-123")
        assert dto.job_id == "job-123"

    def test_result_not_completed(self):
        dto = FetchUsersIpsResultResponseDto(
            isCompleted=False,
            isFailed=False,
            result=None,
        )
        assert dto.is_completed is False
        assert dto.is_failed is False
        assert dto.result is None

    def test_result_completed(self):
        uid = uuid4()
        dto = FetchUsersIpsResultResponseDto(
            isCompleted=True,
            isFailed=False,
            result={
                "success": True,
                "nodeUuid": str(uid),
                "users": [
                    {
                        "userId": "user-1",
                        "ips": [
                            {"ip": "1.2.3.4", "lastSeen": "2025-01-01T00:00:00Z"},
                        ],
                    }
                ],
            },
        )
        assert dto.is_completed is True
        assert dto.result.success is True
        assert dto.result.node_uuid == uid
        assert len(dto.result.users) == 1
        assert dto.result.users[0].user_id == "user-1"
        assert dto.result.users[0].ips[0].ip == "1.2.3.4"


class TestCreateInfraBillingHistoryRecordRequestDto:
    def test_fields_match_spec(self):
        uid = uuid4()
        now = datetime.now(tz=timezone.utc)
        dto = CreateInfraBillingHistoryRecordRequestDto(
            provider_uuid=uid,
            amount=29.99,
            billed_at=now,
        )
        assert dto.provider_uuid == uid
        assert dto.amount == 29.99
        assert dto.billed_at == now

    def test_serialization(self):
        uid = uuid4()
        now = datetime.now(tz=timezone.utc)
        dto = CreateInfraBillingHistoryRecordRequestDto(
            provider_uuid=uid,
            amount=10.0,
            billed_at=now,
        )
        data = dto.model_dump(by_alias=True)
        assert "providerUuid" in data
        assert "billedAt" in data
        assert "amount" in data

    def test_no_old_fields(self):
        """Ensure removed fields don't exist."""
        assert not hasattr(CreateInfraBillingHistoryRecordRequestDto, "node_uuid")
        assert not hasattr(CreateInfraBillingHistoryRecordRequestDto, "payment_date")
        assert not hasattr(CreateInfraBillingHistoryRecordRequestDto, "description")


class TestCreateInfraBillingNodeRequestDto:
    def test_next_billing_at_required(self):
        """next_billing_at became required in Remnawave API v2.8.0."""
        with pytest.raises(ValidationError):
            CreateInfraBillingNodeRequestDto(
                node_uuid=uuid4(),
                provider_uuid=uuid4(),
            )

    def test_next_billing_at_provided(self):
        now = datetime.now(tz=timezone.utc)
        dto = CreateInfraBillingNodeRequestDto(
            node_uuid=uuid4(),
            provider_uuid=uuid4(),
            name="My server",
            next_billing_at=now,
        )
        assert dto.next_billing_at == now

    def test_name_and_node_uuid_required(self):
        """name and node_uuid are required in the Remnawave API v2.8.1 contract."""
        now = datetime.now(tz=timezone.utc)
        # node_uuid missing -> error
        with pytest.raises(ValidationError):
            CreateInfraBillingNodeRequestDto(
                provider_uuid=uuid4(),
                name="My server",
                next_billing_at=now,
            )
        # name missing -> error
        with pytest.raises(ValidationError):
            CreateInfraBillingNodeRequestDto(
                provider_uuid=uuid4(),
                node_uuid=uuid4(),
                next_billing_at=now,
            )
        # all required fields provided -> ok
        dto = CreateInfraBillingNodeRequestDto(
            provider_uuid=uuid4(),
            node_uuid=uuid4(),
            name="My server",
            next_billing_at=now,
        )
        assert dto.name == "My server"


class TestResponseRulesSettings:
    def test_settings_field_exists(self):
        rules = ResponseRules(
            version=ResponseRuleVersion.V1,
            rules=[],
            settings=ResponseRulesSettings(
                disable_subscription_access_by_path=True,
            ),
        )
        assert rules.settings is not None
        assert rules.settings.disable_subscription_access_by_path is True

    def test_settings_optional(self):
        rules = ResponseRules(
            version=ResponseRuleVersion.V1,
            rules=[],
        )
        assert rules.settings is None

    def test_settings_deserialization(self):
        rules = ResponseRules.model_validate({
            "version": "1",
            "rules": [],
            "settings": {"disableSubscriptionAccessByPath": False},
        })
        assert rules.settings.disable_subscription_access_by_path is False


class TestWebhookNodeDto:
    def test_system_field(self):
        system = NodeSystemDto.model_validate({
            "info": {
                "arch": "x64",
                "cpus": 4,
                "cpuModel": "Intel Core i7",
                "memoryTotal": 16384,
                "hostname": "node-1",
                "platform": "linux",
                "release": "5.15.0",
                "type": "Linux",
                "version": "#1 SMP",
                "networkInterfaces": ["eth0", "lo"],
            },
            "stats": {
                "memoryFree": 8192,
                "memoryUsed": 8192,
                "uptime": 3600,
                "loadAvg": [0.5, 0.3, 0.1],
                "interface": None,
            },
        })
        assert system.info.arch == "x64"
        assert system.info.cpus == 4
        assert system.info.cpu_model == "Intel Core i7"
        assert system.stats.memory_free == 8192
        assert system.stats.uptime == 3600

    def test_versions_field(self):
        versions = NodeVersionsDto.model_validate({
            "xray": "1.8.6",
            "node": "0.5.0",
        })
        assert versions.xray == "1.8.6"
        assert versions.node == "0.5.0"

    def test_node_dto_has_new_fields(self):
        from remnawave.models.webhook import NodeDto

        fields = NodeDto.model_fields
        assert "active_plugin_uuid" in fields
        assert "system" in fields
        assert "versions" in fields

    def test_node_dto_xray_uptime_is_float(self):
        from remnawave.models.webhook import NodeDto

        field = NodeDto.model_fields["xray_uptime"]
        assert field.annotation == float or field.annotation is float

"""Tests for model field validation and serialization."""
import pytest
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import ValidationError

from remnawave.models import (
    # Users
    ResolveUserBodyDto,
    ResolveUserResponseDto,
    RevokeUserSubscriptionBodyDto,
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
    # Hosts (v3.4.x)
    CreateHostInboundData,
    CreateHostRequestDto,
    HostInternalSquadsDto,
    HostMapperCopyOp,
    HostMapperDto,
    HostMapperSetOp,
    HostMapperUnsetOp,
    HostResponseDto,
    UpdateHostRequestDto,
    UpdateManyHostsRequestDto,
    # Nodes (v3.4.x)
    BulkNodesUpdateFieldsDto,
    CreateNodeRequestDto,
    NodeConfigProfileRequestDto,
    NodeIpDto,
    UpdateNodeRequestDto,
    # Node integrations (v3.4.x)
    CreateNodeIntegrationRequestDto,
    GetNodeIntegrationsResponseDto,
    UpdateNodeIntegrationRequestDto,
    # Node plugins / shared lists (v3.4.x)
    CreateSharedListRequestDto,
    DeleteSharedListRequestDto,
    GetSharedListsResponseDto,
    NodePluginDto,
    SyncNodePluginRequestDto,
    SyncSharedListRequestDto,
    # Snippets (v3.4.x)
    CreateSnippetRequestDto,
    SyncSnippetRequestDto,
    UpdateSnippetRequestDto,
    # Tags (v3.4.x)
    GetConfigProfilesTagsResponseDto,
    GetExternalSquadsTagsResponseDto,
    GetInternalSquadsTagsResponseDto,
    GetNodePluginsTagsResponseDto,
    GetSubpageConfigsTagsResponseDto,
    GetSubscriptionTemplatesTagsResponseDto,
    GetTagsResponseDto,
    SetTagsRequestDto,
    SubscriptionPageConfigDto,
    # Connections / geocheck (v3.4.x)
    GeocheckByNodeRequestDto,
    GeocheckByNodeResponseDto,
    GeocheckByNodeResultResponseDto,
    # Pre-3.4.3 contract drift fixes
    FetchIpsResultResponseDto,
    InfraBillingNodeDto,
    OAuth2Settings,
    PlatformStatItem,
    RuntimeMetric,
    SubscriptionRequestHistoryRecord,
    TorrentBlockerTopUserDto,
    TorrentBlockerUserDto,
)
from remnawave.models.subscriptions_settings import ResponseModifications
from remnawave.enums import InternalSquadsMode, NodeIpStatus, ResponseRuleVersion


class TestResolveUserBodyDto:
    def test_create_with_username(self):
        dto = ResolveUserBodyDto(username="testuser")
        assert dto.username == "testuser"

    def test_create_with_short_uuid(self):
        dto = ResolveUserBodyDto(short_uuid="abc123")
        assert dto.short_uuid == "abc123"

    def test_serialization_alias(self):
        dto = ResolveUserBodyDto(short_uuid="abc123")
        data = dto.model_dump(by_alias=True)
        assert "shortUuid" in data

    def test_create_with_id(self):
        dto = ResolveUserBodyDto(id=42)
        assert dto.id == 42


class TestResolveUserResponseDto:
    def test_from_api_response(self):
        dto = ResolveUserResponseDto(
            username="testuser",
            id=1,
            shortUuid="abc123",
        )
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
                        "userId": 1,
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
        assert dto.result.users[0].user_id == 1
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


# ─────────────────────────────────────────────────────────────────────────────
# Remnawave API v3.4.x
# ─────────────────────────────────────────────────────────────────────────────

HOST_PAYLOAD = {
    "uuid": "c88acc18-291e-4d79-bb5f-72b229281e92",
    "viewPosition": 0,
    "remark": "DE - fast",
    "address": "91.99.13.29",
    "port": 443,
    "path": None,
    "sni": "example.com",
    "host": None,
    "alpn": None,
    "fingerprint": None,
    "isDisabled": False,
    "securityLayer": "DEFAULT",
    "xhttpExtraParams": None,
    "muxParams": None,
    "sockoptParams": None,
    "finalMask": None,
    "serverDescription": None,
    "pinnedPeerCertSha256": None,
    "verifyPeerCertByName": None,
    "shuffleHost": False,
    "mihomoX25519": False,
    "mihomoIpVersion": None,
    "tags": [],
    "isHidden": False,
    "overrideSniFromAddress": False,
    "keepSniBlank": False,
    "vlessRouteId": None,
    "inbound": {
        "configProfileUuid": "ac249d83-c32b-45fc-94de-2f77ce41aead",
        "configProfileInboundUuid": "e62f07d8-292a-4a35-9ee9-427ad3fa4bc1",
    },
    "nodes": [],
    "xrayJsonTemplateUuid": None,
    "excludeFromSubscriptionTypes": [],
    "mapper": {},
    "internalSquads": {"mode": "EXCLUDE", "squads": []},
}


class TestHostInternalSquadsAndMapper:
    """`excludedInternalSquads` became `internalSquads`; `mapper` is new (v3.4.0)."""

    def test_response_parses_internal_squads(self):
        host = HostResponseDto.model_validate(HOST_PAYLOAD)
        assert host.internal_squads.mode == InternalSquadsMode.EXCLUDE
        assert host.internal_squads.squads == []

    def test_response_parses_allow_only_mode(self):
        squad = "11111111-1111-4111-8111-111111111111"
        payload = {**HOST_PAYLOAD, "internalSquads": {"mode": "ALLOW_ONLY", "squads": [squad]}}
        host = HostResponseDto.model_validate(payload)
        assert host.internal_squads.mode == InternalSquadsMode.ALLOW_ONLY
        assert [str(u) for u in host.internal_squads.squads] == [squad]

    def test_excluded_internal_squads_backward_compat_property(self):
        squad = "11111111-1111-4111-8111-111111111111"
        excluding = HostResponseDto.model_validate(
            {**HOST_PAYLOAD, "internalSquads": {"mode": "EXCLUDE", "squads": [squad]}}
        )
        assert [str(u) for u in excluding.excluded_internal_squads] == [squad]

        allowing = HostResponseDto.model_validate(
            {**HOST_PAYLOAD, "internalSquads": {"mode": "ALLOW_ONLY", "squads": [squad]}}
        )
        assert allowing.excluded_internal_squads == []

    def test_response_parses_mapper(self):
        payload = {
            **HOST_PAYLOAD,
            "mapper": {
                "xrayJson": [
                    {"op": "copy", "from": "streamSettings.tlsSettings.alpn", "to": "alpn"},
                    {"op": "set", "to": "mux.enabled", "value": True},
                    {"op": "unset", "to": "mux"},
                ]
            },
        }
        host = HostResponseDto.model_validate(payload)
        assert isinstance(host.mapper.xray_json[0], HostMapperCopyOp)
        assert host.mapper.xray_json[0].from_ == "streamSettings.tlsSettings.alpn"
        assert isinstance(host.mapper.xray_json[1], HostMapperSetOp)
        assert host.mapper.xray_json[1].value is True
        assert isinstance(host.mapper.xray_json[2], HostMapperUnsetOp)
        assert host.mapper.singbox is None

    def test_empty_mapper_and_defaults(self):
        host = HostResponseDto.model_validate(HOST_PAYLOAD)
        assert host.mapper.xray_json is None
        assert host.mapper.base64 is None

    def test_mapper_set_op_requires_value(self):
        with pytest.raises(ValidationError):
            HostMapperSetOp(to="mux.enabled")

    def test_mapper_set_op_keeps_falsy_values(self):
        assert HostMapperSetOp(to="mux.enabled", value=False).model_dump(by_alias=True) == {
            "op": "set",
            "to": "mux.enabled",
            "value": False,
        }

    def test_mapper_copy_op_serializes_from_alias(self):
        op = HostMapperCopyOp(from_="a.b", to="c.d")
        assert op.model_dump(by_alias=True) == {"op": "copy", "from": "a.b", "to": "c.d"}

    def test_create_request_serializes_internal_squads(self):
        squad = uuid4()
        dto = CreateHostRequestDto(
            inbound=CreateHostInboundData(
                config_profile_uuid=uuid4(), config_profile_inbound_uuid=uuid4()
            ),
            remark="test",
            address="127.0.0.1",
            port=443,
            internal_squads=HostInternalSquadsDto(
                mode=InternalSquadsMode.ALLOW_ONLY, squads=[squad]
            ),
        )
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert data["internalSquads"] == {"mode": "ALLOW_ONLY", "squads": [str(squad)]}
        assert "excludedInternalSquads" not in data

    def test_update_request_migrates_legacy_kwarg(self):
        squad = uuid4()
        dto = UpdateHostRequestDto(uuid=uuid4(), excluded_internal_squads=[squad])
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert data["internalSquads"] == {"mode": "EXCLUDE", "squads": [str(squad)]}
        assert "excludedInternalSquads" not in data

    def test_bulk_update_request_migrates_legacy_kwarg(self):
        squad = uuid4()
        dto = UpdateManyHostsRequestDto(uuids=[uuid4()], excluded_internal_squads=[squad])
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert data["internalSquads"] == {"mode": "EXCLUDE", "squads": [str(squad)]}

    def test_legacy_kwarg_with_empty_list_sends_nothing(self):
        dto = UpdateHostRequestDto(uuid=uuid4(), excluded_internal_squads=[])
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert "internalSquads" not in data

    def test_mapper_serialization_in_request(self):
        dto = UpdateHostRequestDto(
            uuid=uuid4(),
            mapper=HostMapperDto(
                mihomo=[HostMapperSetOp(to="ip-version", value="dual")],
            ),
        )
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert data["mapper"] == {"mihomo": [{"op": "set", "to": "ip-version", "value": "dual"}]}


class TestNodeIpsAndIntegrations:
    """`integrationUuids` and `ips` are new node fields in v3.4.0."""

    def test_node_ip_dto(self):
        dto = NodeIpDto(ip="203.0.113.5", status=NodeIpStatus.OUTBOUND)
        assert dto.model_dump(by_alias=True, mode="json") == {
            "ip": "203.0.113.5",
            "status": "OUTBOUND",
        }

    def test_node_ip_rejects_unknown_status(self):
        with pytest.raises(ValidationError):
            NodeIpDto(ip="203.0.113.5", status="NOT_A_STATUS")

    def test_create_request_serializes_new_fields(self):
        integration = uuid4()
        dto = CreateNodeRequestDto(
            name="node-1",
            address="127.0.0.1",
            config_profile=NodeConfigProfileRequestDto(
                activeConfigProfileUuid=uuid4(), activeInbounds=[uuid4()]
            ),
            integration_uuids=[integration],
            ips=[NodeIpDto(ip="203.0.113.5", status=NodeIpStatus.INBOUND)],
        )
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert data["integrationUuids"] == [str(integration)]
        assert data["ips"] == [{"ip": "203.0.113.5", "status": "INBOUND"}]

    def test_update_request_serializes_new_fields(self):
        dto = UpdateNodeRequestDto(
            uuid=uuid4(),
            ips=[NodeIpDto(ip="2001:db8::1", status=NodeIpStatus.MANAGEMENT)],
        )
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert data["ips"] == [{"ip": "2001:db8::1", "status": "MANAGEMENT"}]

    def test_bulk_update_fields_accept_integration_uuids(self):
        integration = uuid4()
        dto = BulkNodesUpdateFieldsDto(integration_uuids=[integration])
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert data["integrationUuids"] == [str(integration)]


class TestNodeIntegrationModels:
    def test_list_response_from_api_payload(self):
        dto = GetNodeIntegrationsResponseDto.model_validate(
            {
                "total": 1,
                "nodeIntegrations": [
                    {
                        "uuid": "edb09a2c-72a9-44ff-9bb5-acee980cb5f0",
                        "name": "probe",
                        "description": None,
                        "config": {"a": 1},
                    }
                ],
            }
        )
        assert dto.total == 1
        assert dto.node_integrations[0].name == "probe"
        assert dto.node_integrations[0].description is None
        assert dto.node_integrations[0].config == {"a": 1}

    def test_create_request_requires_config(self):
        with pytest.raises(ValidationError):
            CreateNodeIntegrationRequestDto(name="probe")

    def test_create_request_name_length(self):
        with pytest.raises(ValidationError):
            CreateNodeIntegrationRequestDto(name="x", config={})

    def test_update_request_only_sends_provided_fields(self):
        integration_uuid = uuid4()
        dto = UpdateNodeIntegrationRequestDto(uuid=integration_uuid, restart_nodes=True)
        data = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert data == {"uuid": str(integration_uuid), "restartNodes": True}


class TestSharedListModels:
    def test_preview_response(self):
        dto = GetSharedListsResponseDto.model_validate(
            {"total": 1, "sharedLists": [{"name": "a/b", "type": "ipList", "itemsCount": 3}]}
        )
        assert dto.shared_lists[0].items_count == 3
        assert dto.shared_lists[0].type == "ipList"

    def test_name_allows_folder_segments(self):
        dto = CreateSharedListRequestDto(name="blocklists/ip/ru", config={"type": "ipList"})
        assert dto.name == "blocklists/ip/ru"

    def test_name_rejects_spaces(self):
        with pytest.raises(ValidationError):
            CreateSharedListRequestDto(name="with space", config={"type": "ipList"})

    def test_name_rejects_trailing_slash(self):
        with pytest.raises(ValidationError):
            CreateSharedListRequestDto(name="folder/", config={"type": "ipList"})

    def test_sync_and_delete_bodies(self):
        assert SyncSharedListRequestDto(name="a-b").model_dump() == {"name": "a-b"}
        assert DeleteSharedListRequestDto(name="a-b").model_dump() == {"name": "a-b"}

    def test_sync_node_plugin_body(self):
        plugin_uuid = uuid4()
        dto = SyncNodePluginRequestDto(uuid=plugin_uuid)
        assert dto.model_dump(by_alias=True, mode="json") == {"uuid": str(plugin_uuid)}


class TestSnippetNamePattern:
    """Snippet names gained "/" folder support in v3.4.0."""

    def test_folder_name_allowed(self):
        assert CreateSnippetRequestDto(name="group/my snippet", snippet=[]).name == (
            "group/my snippet"
        )

    def test_plain_name_still_allowed(self):
        assert UpdateSnippetRequestDto(name="A B C", snippet=[]).name == "A B C"

    def test_trailing_slash_rejected(self):
        with pytest.raises(ValidationError):
            CreateSnippetRequestDto(name="group/", snippet=[])

    def test_sync_snippet_body(self):
        assert SyncSnippetRequestDto(name="group/name").model_dump() == {"name": "group/name"}


class TestTagsModels:
    def test_get_tags_response(self):
        assert GetTagsResponseDto.model_validate({"tags": ["A", "B"]}).tags == ["A", "B"]

    def test_get_tags_defaults_to_empty(self):
        assert GetTagsResponseDto().tags == []

    def test_set_tags_request_serialization(self):
        entity_uuid = uuid4()
        dto = SetTagsRequestDto(uuid=entity_uuid, tags=["SDK_TEST"])
        assert dto.model_dump(by_alias=True, mode="json") == {
            "uuid": str(entity_uuid),
            "tags": ["SDK_TEST"],
        }

    def test_set_tags_rejects_lowercase(self):
        with pytest.raises(ValidationError):
            SetTagsRequestDto(uuid=uuid4(), tags=["lowercase"])

    def test_set_tags_rejects_more_than_ten(self):
        with pytest.raises(ValidationError):
            SetTagsRequestDto(uuid=uuid4(), tags=[f"TAG_{i}" for i in range(11)])

    def test_per_resource_dtos_share_the_shape(self):
        for dto_cls in (
            GetConfigProfilesTagsResponseDto,
            GetInternalSquadsTagsResponseDto,
            GetExternalSquadsTagsResponseDto,
            GetNodePluginsTagsResponseDto,
            GetSubpageConfigsTagsResponseDto,
            GetSubscriptionTemplatesTagsResponseDto,
        ):
            assert dto_cls.model_validate({"tags": ["X"]}).tags == ["X"]

    def test_taggable_entities_default_to_empty_tags(self):
        assert NodePluginDto.model_validate(
            {"uuid": str(uuid4()), "viewPosition": 0, "name": "p", "pluginConfig": None}
        ).tags == []
        assert SubscriptionPageConfigDto.model_validate(
            {"uuid": str(uuid4()), "viewPosition": 0, "name": "c", "config": None}
        ).tags == []


class TestGeocheckModels:
    def test_job_response(self):
        assert GeocheckByNodeResponseDto.model_validate({"jobId": "42"}).job_id == "42"

    def test_request_body_is_optional(self):
        assert GeocheckByNodeRequestDto().model_dump(exclude_none=True) == {}
        assert GeocheckByNodeRequestDto(ip="1.1.1.1").model_dump(exclude_none=True) == {
            "ip": "1.1.1.1"
        }

    def test_pending_result(self):
        dto = GeocheckByNodeResultResponseDto.model_validate(
            {"isCompleted": False, "isFailed": False, "result": None}
        )
        assert dto.is_completed is False
        assert dto.result is None

    def test_failed_node_result(self):
        dto = GeocheckByNodeResultResponseDto.model_validate(
            {
                "isCompleted": True,
                "isFailed": False,
                "result": {
                    "success": False,
                    "nodeUuid": "584dbf53-48ef-43e5-b78f-ead6f5c6809f",
                    "image": None,
                    "rawReport": None,
                    "message": "ERR_INVALID_URL",
                },
            }
        )
        assert dto.result.success is False
        assert dto.result.message == "ERR_INVALID_URL"
        assert dto.result.image is None

    def test_successful_result_with_image(self):
        dto = GeocheckByNodeResultResponseDto.model_validate(
            {
                "isCompleted": True,
                "isFailed": False,
                "result": {
                    "success": True,
                    "nodeUuid": "584dbf53-48ef-43e5-b78f-ead6f5c6809f",
                    "image": {
                        "format": "svg",
                        "media_type": "image/svg+xml",
                        "encoding": "base64",
                        "data": "PHN2Zy8+",
                    },
                    "rawReport": {"country": "DE"},
                    "message": None,
                },
            }
        )
        assert dto.result.image.data == "PHN2Zy8+"
        assert dto.result.raw_report == {"country": "DE"}


class TestResponseModificationsNewFields:
    """SRR response modifications gained `respondWithRemarks` in v3.4.0."""

    def test_respond_with_remarks(self):
        dto = ResponseModifications.model_validate({"respondWithRemarks": ["Blocked"]})
        assert dto.respond_with_remarks == ["Blocked"]
        assert dto.model_dump(exclude_none=True, by_alias=True) == {
            "respondWithRemarks": ["Blocked"]
        }

    def test_previously_unmodelled_fields(self):
        dto = ResponseModifications.model_validate(
            {
                "additionalExtendedClientsRegex": ["MyApp/.*"],
                "disableHwidCheck": True,
                "excludeHostsByTags": ["HIDDEN"],
                "encryption": {"method": "age1", "key": "age1abc"},
            }
        )
        assert dto.additional_extended_clients_regex == ["MyApp/.*"]
        assert dto.disable_hwid_check is True
        assert dto.exclude_hosts_by_tags == ["HIDDEN"]
        assert dto.encryption.method == "age1"

    def test_encryption_rejects_unknown_method(self):
        with pytest.raises(ValidationError):
            ResponseModifications.model_validate(
                {"encryption": {"method": "rot13", "key": "x"}}
            )


class TestContractDriftFixes:
    """Регрессии на поля, разъезжавшиеся с контрактом до 3.4.3."""

    def test_connections_by_user_result_uses_numeric_user_id(self):
        dto = FetchIpsResultResponseDto.model_validate(
            {
                "isCompleted": True,
                "isFailed": False,
                "progress": {"total": 0, "completed": 0, "percent": 0},
                "result": {"success": True, "userId": 1417, "nodes": []},
            }
        )
        assert dto.result.user_id == 1417
        assert dto.result.user_uuid is None

    def test_connections_by_node_result_uses_numeric_user_id(self):
        dto = FetchUsersIpsResultResponseDto.model_validate(
            {
                "isCompleted": True,
                "isFailed": False,
                "result": {
                    "success": True,
                    "nodeUuid": "584dbf53-48ef-43e5-b78f-ead6f5c6809f",
                    "users": [
                        {
                            "userId": 42,
                            "ips": [{"ip": "1.2.3.4", "lastSeen": "2026-09-09T10:00:00.000Z"}],
                        }
                    ],
                },
            }
        )
        assert dto.result.users[0].user_id == 42

    def test_torrent_blocker_user_without_uuid(self):
        dto = TorrentBlockerUserDto.model_validate({"username": "someone"})
        assert dto.username == "someone"
        assert dto.uuid is None

    def test_torrent_blocker_top_user_uses_user_id(self):
        dto = TorrentBlockerTopUserDto.model_validate(
            {"userId": 7, "color": "#fff", "username": "someone", "total": 3}
        )
        assert dto.user_id == 7
        assert dto.uuid is None

    def test_oauth2_settings_without_optional_providers(self):
        provider = {
            "enabled": False,
            "clientId": None,
            "clientSecret": None,
            "allowedEmails": [],
        }
        dto = OAuth2Settings.model_validate(
            {
                "github": {**provider, "allowedOrgs": []} if False else provider,
                "pocketid": {
                    **provider,
                    "frontendDomain": None,
                    "plainDomain": None,
                },
                "yandex": provider,
            }
        )
        assert dto.keycloak is None
        assert dto.generic is None
        assert dto.telegram is None
        assert dto.pocketid.frontend_domain is None

    def test_hwid_platform_stat_carries_by_app(self):
        dto = PlatformStatItem.model_validate(
            {"platform": "ios", "count": 2, "byApp": [{"app": "happ", "count": 2}]}
        )
        assert dto.by_app[0].app == "happ"

    def test_infra_billing_node_without_node(self):
        dto = InfraBillingNodeDto.model_validate(
            {
                "uuid": str(uuid4()),
                "name": "hetzner-1",
                "nodeUuid": None,
                "providerUuid": str(uuid4()),
                "provider": {
                    "uuid": str(uuid4()),
                    "name": "Hetzner",
                    "faviconLink": None,
                    "loginUrl": None,
                },
                "node": None,
                "nextBillingAt": "2026-10-01T00:00:00.000Z",
                "createdAt": "2026-09-01T00:00:00.000Z",
                "updatedAt": "2026-09-01T00:00:00.000Z",
            }
        )
        assert dto.name == "hetzner-1"
        assert dto.node is None
        assert dto.node_uuid is None

    def test_subscription_request_history_srr_fields(self):
        record = SubscriptionRequestHistoryRecord.model_validate(
            {
                "id": 1,
                "userId": 2,
                "srrResponseType": "DEFAULT",
                "srrRuleName": None,
                "requestIp": None,
                "userAgent": None,
                "requestAt": "2026-09-09T10:00:00.000Z",
            }
        )
        assert record.srr_response_type == "DEFAULT"
        assert record.srr_rule_name is None

    def test_runtime_metric_typed_fields(self):
        metric = RuntimeMetric.model_validate(
            {
                "rss": 1.0,
                "heapUsed": 2.0,
                "heapTotal": 3.0,
                "external": 4.0,
                "arrayBuffers": 5.0,
                "eventLoopDelayMs": 0.1,
                "eventLoopP99Ms": 0.5,
                "activeHandles": 30,
                "uptime": 523.0,
                "pid": 101,
                "timestamp": 1788968290203,
                "instanceId": "0",
                "instanceType": "api",
            }
        )
        assert metric.array_buffers == 5.0
        assert metric.active_handles == 30
        assert metric.instance_id == "0"
        assert metric.event_loop_p99_ms == 0.5

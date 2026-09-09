from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, RootModel, StringConstraints

from remnawave.enums import ALPN, MihomoIpVersion, SecurityLayer, SubscriptionType
from remnawave.models import HostResponseDto
from remnawave.models.hosts import (
    CreateHostInboundData,
    HostInternalSquadsDto,
    HostMapperDto,
    HostTag,
    _migrate_excluded_internal_squads,
)


class _HostListResponse(RootModel[List[HostResponseDto]]):
    """Base for bulk host responses that return a plain list of hosts."""
    root: List[HostResponseDto]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __bool__(self):
        return bool(self.root)

    def __len__(self):
        return len(self.root)


class BulkDeleteHostsResponseDto(_HostListResponse):
    pass


class BulkDisableHostsResponseDto(_HostListResponse):
    pass


class BulkEnableHostsResponseDto(_HostListResponse):
    pass


class UpdateManyHostsRequestDto(BaseModel):
    """Request to update many hosts at once (PATCH /hosts/bulk/update)."""
    uuids: List[UUID] = Field(min_length=1)
    inbound: Optional[CreateHostInboundData] = None
    remark: Annotated[Optional[str], StringConstraints(max_length=40)] = None
    address: Optional[str] = None
    port: Optional[int] = None
    path: Optional[str] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    alpn: Optional[ALPN] = None
    fingerprint: Optional[str] = None
    is_disabled: Optional[bool] = Field(None, serialization_alias="isDisabled")
    security_layer: Optional[SecurityLayer] = Field(None, serialization_alias="securityLayer")
    server_description: Optional[str] = Field(None, serialization_alias="serverDescription", max_length=30)
    tags: Optional[List[HostTag]] = Field(None, serialization_alias="tags", max_length=10)
    is_hidden: Optional[bool] = Field(None, serialization_alias="isHidden")
    override_sni_from_address: Optional[bool] = Field(None, serialization_alias="overrideSniFromAddress")
    keep_blank_sni: Optional[bool] = Field(None, serialization_alias="keepSniBlank")
    vless_route_id: Optional[int] = Field(None, serialization_alias="vlessRouteId", ge=0, le=65535)
    pinned_peer_cert_sha256: Optional[str] = Field(None, serialization_alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: Optional[str] = Field(None, serialization_alias="verifyPeerCertByName")
    shuffle_host: Optional[bool] = Field(None, serialization_alias="shuffleHost")
    mihomo_x25519: Optional[bool] = Field(None, serialization_alias="mihomoX25519")
    mihomo_ip_version: Optional[MihomoIpVersion] = Field(None, serialization_alias="mihomoIpVersion")
    xhttp_extra_params: Optional[Dict[str, Any]] = Field(None, serialization_alias="xhttpExtraParams")
    mux_params: Optional[Dict[str, Any]] = Field(None, serialization_alias="muxParams")
    sockopt_params: Optional[Dict[str, Any]] = Field(None, serialization_alias="sockoptParams")
    final_mask: Optional[Any] = Field(None, serialization_alias="finalMask")
    nodes: Optional[List[UUID]] = None
    xray_json_template_uuid: Optional[UUID] = Field(None, serialization_alias="xrayJsonTemplateUuid")
    internal_squads: Optional[HostInternalSquadsDto] = Field(
        None,
        serialization_alias="internalSquads",
        description="Internal-squad visibility applied to every listed host.",
    )
    mapper: Optional[HostMapperDto] = Field(
        None,
        serialization_alias="mapper",
        description="Operations applied to the entries generated for every listed host.",
    )
    exclude_from_subscription_types: Optional[List[SubscriptionType]] = Field(
        None,
        serialization_alias="excludeFromSubscriptionTypes",
        description="Subscription types from which the hosts will be excluded.",
    )

    def __init__(self, **data):
        # Backward compatibility: `excluded_internal_squads` became `internal_squads` in v3.4.0
        _migrate_excluded_internal_squads(data)
        super().__init__(**data)


class UpdateManyHostsResponseDto(_HostListResponse):
    pass

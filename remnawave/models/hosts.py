from typing import Annotated, Any, Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, RootModel

from remnawave.enums import (
    ALPN,
    InternalSquadsMode,
    MihomoIpVersion,
    SecurityLayer,
    SubscriptionType,
)

# Tag for a single host tag entry: uppercase alphanumeric, underscores and colons, max 36 chars
HostTag = Annotated[str, StringConstraints(max_length=36, pattern=r"^[A-Z0-9_:]+$")]

# Dot-separated path inside a raw inbound / generated outbound (Remnawave API v3.4.0+)
MapperPath = Annotated[str, StringConstraints(min_length=1, max_length=512)]


class HostMapperCopyOp(BaseModel):
    """Copy a value from the raw inbound (or from the host itself via ``$host.``)."""

    model_config = ConfigDict(populate_by_name=True)

    op: Literal["copy"] = "copy"
    from_: MapperPath = Field(alias="from", description="Source path")
    to: MapperPath = Field(description="Target path in the generated entry")


class HostMapperSetOp(BaseModel):
    """Write a literal value into the generated entry."""

    model_config = ConfigDict(populate_by_name=True)

    op: Literal["set"] = "set"
    to: MapperPath = Field(description="Target path in the generated entry")
    value: Any = Field(description="Literal value to write; required by the API")


class HostMapperUnsetOp(BaseModel):
    """Remove a key from the generated entry."""

    model_config = ConfigDict(populate_by_name=True)

    op: Literal["unset"] = "unset"
    to: MapperPath = Field(description="Target path in the generated entry")


HostMapperOp = Annotated[
    Union[HostMapperCopyOp, HostMapperSetOp, HostMapperUnsetOp],
    Field(discriminator="op"),
]


class HostMapperDto(BaseModel):
    """Per-subscription-format operations applied to the entry generated for a host."""

    model_config = ConfigDict(populate_by_name=True)

    xray_json: Optional[List[HostMapperOp]] = Field(None, alias="xrayJson")
    singbox: Optional[List[HostMapperOp]] = None
    mihomo: Optional[List[HostMapperOp]] = None
    base64: Optional[List[HostMapperOp]] = None


class HostInternalSquadsDto(BaseModel):
    """Internal-squad visibility of a host (replaces ``excludedInternalSquads`` in v3.4.0)."""

    model_config = ConfigDict(populate_by_name=True)

    mode: InternalSquadsMode = InternalSquadsMode.EXCLUDE
    squads: List[UUID] = Field(default_factory=list)


def _migrate_excluded_internal_squads(data: Dict[str, Any]) -> None:
    """Translate the pre-v3.4.0 `excluded_internal_squads` kwarg into `internal_squads`."""
    if "excluded_internal_squads" not in data:
        return
    squads = data.pop("excluded_internal_squads")
    if squads and "internal_squads" not in data:
        data["internal_squads"] = HostInternalSquadsDto(
            mode=InternalSquadsMode.EXCLUDE, squads=squads
        )


class ReorderHostItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class ReorderHostRequestDto(BaseModel):
    hosts: List[ReorderHostItem]


class HostInboundData(BaseModel):
    config_profile_uuid: Optional[UUID] = Field(None, alias="configProfileUuid")
    config_profile_inbound_uuid: Optional[UUID] = Field(None, alias="configProfileInboundUuid")


class CreateHostInboundData(BaseModel):
    config_profile_uuid: UUID = Field(serialization_alias="configProfileUuid")
    config_profile_inbound_uuid: UUID = Field(serialization_alias="configProfileInboundUuid")


class UpdateHostRequestDto(BaseModel):
    uuid: UUID
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
        description="Internal-squad visibility of this host.",
    )
    mapper: Optional[HostMapperDto] = Field(
        None,
        serialization_alias="mapper",
        description="Operations applied to the entries generated for this host.",
    )
    exclude_from_subscription_types: Optional[List[SubscriptionType]] = Field(
        None,
        serialization_alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host will be excluded.",
    )

    def __init__(self, **data):
        # Backward compatibility: `excluded_internal_squads` became `internal_squads` in v3.4.0
        _migrate_excluded_internal_squads(data)
        # Backward compatibility: `tag` (single value) was replaced by `tags` (list) in v2.8.0
        if "tag" in data and "tags" not in data:
            tag = data.pop("tag")
            data["tags"] = [tag] if tag is not None else None
        # Backward compatibility: `allow_insecure` was removed in v2.8.0 (use security_layer instead)
        data.pop("allow_insecure", None)
        # Backward compatibility: `xHttpExtraParams` alias was renamed to `xhttpExtraParams`
        if "x_http_extra_params" in data and "xhttp_extra_params" not in data:
            data["xhttp_extra_params"] = data.pop("x_http_extra_params")
        super().__init__(**data)

    @property
    def x_http_extra_params(self) -> Optional[Dict[str, Any]]:
        """Backward compatibility property (renamed to xhttp_extra_params in v2.8.0)"""
        return self.xhttp_extra_params

    @property
    def tag(self) -> Optional[str]:
        """Backward compatibility property (replaced by `tags` in v2.8.0)"""
        return self.tags[0] if self.tags else None

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid if self.inbound else None


class HostResponseDto(BaseModel):
    uuid: UUID
    view_position: int = Field(alias="viewPosition")
    remark: str
    address: str
    port: int
    path: str | None = Field(alias="path")
    sni: str | None = Field(alias="sni")
    host: str | None = Field(alias="host")
    alpn: str | None = Field(alias="alpn")
    fingerprint: str | None = Field(alias="fingerprint")
    xhttp_extra_params: Dict[str, Any] | None = Field(None, alias="xhttpExtraParams")
    mux_params: Dict[str, Any] | None = Field(alias="muxParams")
    sockopt_params: Dict[str, Any] | None = Field(alias="sockoptParams")
    final_mask: Any | None = Field(None, alias="finalMask")
    inbound: HostInboundData
    server_description: str | None = Field(alias="serverDescription")
    tags: List[str] = Field(default_factory=list, alias="tags")
    vless_route_id: int | None = Field(alias="vlessRouteId")
    pinned_peer_cert_sha256: str | None = Field(None, alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: str | None = Field(None, alias="verifyPeerCertByName")
    shuffle_host: bool = Field(alias="shuffleHost")
    mihomo_x25519: bool = Field(alias="mihomoX25519")
    mihomo_ip_version: str | None = Field(None, alias="mihomoIpVersion")
    nodes: List[UUID]
    is_disabled: bool = Field(False, alias="isDisabled")
    security_layer: SecurityLayer = Field(SecurityLayer.DEFAULT, alias="securityLayer")
    is_hidden: bool = Field(False, alias="isHidden")
    override_sni_from_address: bool = Field(False, alias="overrideSniFromAddress")
    keep_blank_sni: bool = Field(False, alias="keepSniBlank")
    xray_json_template_uuid: UUID | None = Field(alias="xrayJsonTemplateUuid")
    internal_squads: HostInternalSquadsDto = Field(
        default_factory=HostInternalSquadsDto,
        alias="internalSquads",
        description="Internal-squad visibility of this host.",
    )
    mapper: HostMapperDto = Field(
        default_factory=HostMapperDto,
        alias="mapper",
        description="Operations applied to the entries generated for this host.",
    )
    exclude_from_subscription_types: List[SubscriptionType] = Field(
        default_factory=list,
        alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host is excluded.",
    )

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid

    @property
    def excluded_internal_squads(self) -> List[UUID]:
        """Backward compatibility property (replaced by `internal_squads` in v3.4.0)"""
        if self.internal_squads.mode == InternalSquadsMode.EXCLUDE:
            return self.internal_squads.squads
        return []

    @property
    def x_http_extra_params(self) -> Dict[str, Any] | None:
        """Backward compatibility property (renamed to xhttp_extra_params in v2.8.0)"""
        return self.xhttp_extra_params

    @property
    def tag(self) -> str | None:
        """Backward compatibility property (replaced by `tags` in v2.8.0)"""
        return self.tags[0] if self.tags else None

    @property
    def allow_insecure(self) -> bool:
        """Backward compatibility property (removed in v2.8.0, derived from security_layer)"""
        return self.security_layer == SecurityLayer.NONE


class CreateHostRequestDto(BaseModel):
    inbound: CreateHostInboundData
    remark: Annotated[str, StringConstraints(min_length=1, max_length=40)]
    address: str
    port: int
    path: Optional[str] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    alpn: Optional[ALPN] = None
    fingerprint: Optional[str] = None
    xhttp_extra_params: Optional[Dict[str, Any]] = Field(None, serialization_alias="xhttpExtraParams")
    mux_params: Optional[Dict[str, Any]] = Field(None, serialization_alias="muxParams")
    sockopt_params: Optional[Dict[str, Any]] = Field(None, serialization_alias="sockoptParams")
    final_mask: Optional[Any] = Field(None, serialization_alias="finalMask")
    server_description: Optional[str] = Field(None, serialization_alias="serverDescription", max_length=30)
    tags: Optional[List[HostTag]] = Field(None, serialization_alias="tags", max_length=10)
    vless_route_id: Optional[int] = Field(None, serialization_alias="vlessRouteId", ge=0, le=65535)
    pinned_peer_cert_sha256: Optional[str] = Field(None, serialization_alias="pinnedPeerCertSha256")
    verify_peer_cert_by_name: Optional[str] = Field(None, serialization_alias="verifyPeerCertByName")
    shuffle_host: bool = Field(False, serialization_alias="shuffleHost")
    mihomo_x25519: bool = Field(False, serialization_alias="mihomoX25519")
    mihomo_ip_version: Optional[MihomoIpVersion] = Field(None, serialization_alias="mihomoIpVersion")
    nodes: List[UUID] = Field(default_factory=list)
    is_disabled: bool = Field(False, serialization_alias="isDisabled")
    security_layer: SecurityLayer = Field(SecurityLayer.DEFAULT, serialization_alias="securityLayer")
    is_hidden: bool = Field(False, serialization_alias="isHidden")
    override_sni_from_address: bool = Field(False, serialization_alias="overrideSniFromAddress")
    keep_blank_sni: bool = Field(False, serialization_alias="keepSniBlank")
    xray_json_template_uuid: Optional[UUID] = Field(None, serialization_alias="xrayJsonTemplateUuid")
    internal_squads: Optional[HostInternalSquadsDto] = Field(
        None,
        serialization_alias="internalSquads",
        description="Internal-squad visibility of this host.",
    )
    mapper: Optional[HostMapperDto] = Field(
        None,
        serialization_alias="mapper",
        description="Operations applied to the entries generated for this host.",
    )
    exclude_from_subscription_types: List[SubscriptionType] = Field(
        default_factory=list,
        serialization_alias="excludeFromSubscriptionTypes",
        description="Subscription types from which this host will be excluded.",
    )

    @property
    def inbound_uuid(self) -> Optional[UUID]:
        return self.inbound.config_profile_inbound_uuid

    @property
    def x_http_extra_params(self) -> Optional[Dict[str, Any]]:
        """Backward compatibility property (renamed to xhttp_extra_params in v2.8.0)"""
        return self.xhttp_extra_params

    @property
    def tag(self) -> Optional[str]:
        """Backward compatibility property (replaced by `tags` in v2.8.0)"""
        return self.tags[0] if self.tags else None

    def __init__(
        self,
        inbound_uuid: Optional[UUID] = None,
        config_profile_uuid: Optional[UUID] = None,
        **data,
    ):
        # Backward-compatible support for misspelled helper argument used in old tests/examples
        if config_profile_uuid is None and "config_profile_inbound_uuid" in data:
            config_profile_uuid = data.pop("config_profile_inbound_uuid")

        # Backward compatibility: `excluded_internal_squads` became `internal_squads` in v3.4.0
        _migrate_excluded_internal_squads(data)

        if inbound_uuid is not None and "inbound" not in data:
            data["inbound"] = CreateHostInboundData(
                config_profile_uuid=config_profile_uuid
                or UUID("107541f1-ae1a-4e2d-9dec-7297557b5125"),
                config_profile_inbound_uuid=inbound_uuid,
            )

        # Backward compatibility: `tag` (single value) was replaced by `tags` (list) in v2.8.0
        if "tag" in data and "tags" not in data:
            tag = data.pop("tag")
            data["tags"] = [tag] if tag is not None else None
        # Backward compatibility: `allow_insecure` was removed in v2.8.0 (use security_layer instead)
        data.pop("allow_insecure", None)
        # Backward compatibility: `xHttpExtraParams` alias was renamed to `xhttpExtraParams`
        if "x_http_extra_params" in data and "xhttp_extra_params" not in data:
            data["xhttp_extra_params"] = data.pop("x_http_extra_params")

        super().__init__(**data)


class GetAllHostTagsResponseDto(BaseModel):
    tags: List[str]


# Response wrappers - обернуты в response
class CreateHostResponseDto(HostResponseDto):
    """Create host response"""
    pass


class UpdateHostResponseDto(CreateHostResponseDto):
    """Update host response"""
    pass


class GetAllHostsResponseDto(RootModel[List[HostResponseDto]]):
    root: List[HostResponseDto]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
    def __bool__(self):
        """Return True if list is not empty"""
        return bool(self.root)
    
    def __len__(self):
        """Return length of list"""
        return len(self.root)


class GetOneHostResponseDto(HostResponseDto):
    """Get one host response"""
    pass


class ReorderHostResponseDto(BaseModel):
    """Reorder hosts response"""
    is_updated: bool = Field(alias="isUpdated", default=True)


class DeleteHostResponseDto(BaseModel):
    """Delete host response"""
    is_deleted: bool = Field(alias="isDeleted")
    
class HostsResponseDto(HostResponseDto):
    """Host response data with backward compatibility properties"""
    
    @property
    def allow_insecure(self) -> bool:
        """Backward compatibility property"""
        return self.security_layer == SecurityLayer.NONE
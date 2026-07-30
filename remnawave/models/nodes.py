from datetime import datetime
from typing import Annotated, List, Optional, Union, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, RootModel

from remnawave.models.internal_squads import InboundsDto
from remnawave.models.webhook import NodeSystemDto, NodeVersionsDto


class ExcludedInbounds(BaseModel):
    uuid: UUID
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None


class RestartEventResponse(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class DeleteResponse(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")


class ReorderNodeItem(BaseModel):
    view_position: int = Field(serialization_alias="viewPosition")
    uuid: UUID


class GetAllNodesTagsResponseDto(BaseModel):
    """Response with all nodes tags"""
    tags: List[str]


class NodeProviderDto(BaseModel):
    """Node provider information"""
    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(None, alias="faviconLink")
    login_url: Optional[str] = Field(None, alias="loginUrl")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class NodeConfigProfileDto(BaseModel):
    active_config_profile_uuid: Optional[UUID] = Field(alias="activeConfigProfileUuid")
    active_inbounds: List[InboundsDto] = Field(alias="activeInbounds")


class NodeConfigProfileRequestDto(BaseModel):
    active_config_profile_uuid: UUID = Field(alias="activeConfigProfileUuid")
    active_inbounds: List[UUID] = Field(alias="activeInbounds")


class CreateNodeRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    address: Annotated[str, StringConstraints(min_length=2)]
    port: Optional[int] = Field(None, ge=1, le=65535)
    is_traffic_tracking_active: Optional[bool] = Field(
        False, 
        serialization_alias="isTrafficTrackingActive",
    )
    traffic_limit_bytes: Optional[float] = Field(
        None, serialization_alias="trafficLimitBytes", ge=0
    )
    notify_percent: Optional[int] = Field(
        None, serialization_alias="notifyPercent", ge=0, le=100
    )
    traffic_reset_day: Optional[int] = Field(
        None, serialization_alias="trafficResetDay", ge=1, le=31
    )
    country_code: Annotated[Optional[str], StringConstraints(max_length=2)] = Field(
        "XX",
        serialization_alias="countryCode"
    )
    consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="consumptionMultiplier", ge=0, le=100
    )
    node_consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="nodeConsumptionMultiplier", ge=0, le=100
    )
    note: Optional[str] = Field(None, serialization_alias="note", max_length=255)
    proxy_url: Optional[str] = Field(
        None,
        serialization_alias="proxyUrl",
        pattern=r"^socks5://(?:[^:@/\s]+(?::[^@/\s]*)?@)?[^:@/\s]+:\d{1,5}$",
    )
    config_profile: NodeConfigProfileRequestDto = Field(
        serialization_alias="configProfile"
    )
    provider_uuid: Optional[UUID] = Field(None, serialization_alias="providerUuid")
    tags: Optional[List[Annotated[str, StringConstraints(max_length=36, pattern=r'^[A-Z0-9_:]+$')]]] = Field(
        None, 
        serialization_alias="tags",
        max_length=10
    )
    active_plugin_uuid: Optional[UUID] = Field(
        None, serialization_alias="activePluginUuid"
    )


class UpdateNodeRequestDto(BaseModel):
    uuid: UUID
    name: Annotated[Optional[str], StringConstraints(min_length=3, max_length=30)] = None
    address: Annotated[Optional[str], StringConstraints(min_length=2)] = None
    port: Optional[float] = Field(None, ge=1, le=65535)  # ИСПРАВЛЕН тип на float
    is_traffic_tracking_active: Optional[bool] = Field(
        None, serialization_alias="isTrafficTrackingActive"
    )
    traffic_limit_bytes: Optional[float] = Field(
        None, serialization_alias="trafficLimitBytes", ge=0
    )
    notify_percent: Optional[float] = Field(
        None, serialization_alias="notifyPercent", ge=0, le=100
    )
    traffic_reset_day: Optional[float] = Field(
        None, serialization_alias="trafficResetDay", ge=1, le=31
    )
    country_code: Annotated[Optional[str], StringConstraints(max_length=2)] = Field(
        None, serialization_alias="countryCode"
    )
    consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="consumptionMultiplier", ge=0, le=100
    )
    node_consumption_multiplier: Optional[float] = Field(
        None, serialization_alias="nodeConsumptionMultiplier", ge=0, le=100
    )
    note: Optional[str] = Field(None, serialization_alias="note", max_length=255)
    proxy_url: Optional[str] = Field(
        None,
        serialization_alias="proxyUrl",
        pattern=r"^socks5://(?:[^:@/\s]+(?::[^@/\s]*)?@)?[^:@/\s]+:\d{1,5}$",
    )
    config_profile: Optional[NodeConfigProfileRequestDto] = Field(
        None, serialization_alias="configProfile"
    )
    provider_uuid: Optional[UUID] = Field(None, serialization_alias="providerUuid")
    tags: Optional[List[Annotated[str, StringConstraints(max_length=36, pattern=r'^[A-Z0-9_:]+$')]]] = Field(
        None,
        serialization_alias="tags",
        max_length=10
    )
    active_plugin_uuid: Optional[UUID] = Field(
        None, serialization_alias="activePluginUuid"
    )


class ReorderNodeRequestDto(BaseModel):
    nodes: List[ReorderNodeItem]


class NodeResponseDto(BaseModel):
    uuid: UUID
    name: str
    address: str
    port: Optional[int] = None
    is_connected: bool = Field(alias="isConnected")
    is_disabled: bool = Field(alias="isDisabled")
    is_connecting: bool = Field(alias="isConnecting")
    last_status_change: Optional[datetime] = Field(None, alias="lastStatusChange")
    last_status_message: Optional[str] = Field(None, alias="lastStatusMessage")
    xray_uptime: float = Field(0, alias="xrayUptime")
    is_traffic_tracking_active: bool = Field(alias="isTrafficTrackingActive")
    traffic_reset_day: Optional[int] = Field(None, alias="trafficResetDay")
    traffic_limit_bytes: Optional[float] = Field(None, alias="trafficLimitBytes")
    traffic_used_bytes: Optional[float] = Field(None, alias="trafficUsedBytes")
    notify_percent: Optional[int] = Field(None, alias="notifyPercent")
    users_online: Optional[int] = Field(None, alias="usersOnline")
    view_position: int = Field(alias="viewPosition")
    country_code: str = Field(alias="countryCode")
    consumption_multiplier: float = Field(alias="consumptionMultiplier")
    node_consumption_multiplier: Optional[float] = Field(None, alias="nodeConsumptionMultiplier")
    note: Optional[str] = Field(None, alias="note")
    proxy_url: Optional[str] = Field(None, alias="proxyUrl")
    system: Optional[NodeSystemDto] = Field(None, alias="system")
    versions: Optional[NodeVersionsDto] = Field(None, alias="versions")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config_profile: NodeConfigProfileDto = Field(alias="configProfile")
    provider_uuid: Optional[UUID] = Field(None, alias="providerUuid")
    provider: Optional[NodeProviderDto] = None
    tags: List[str] = Field(default_factory=list, alias="tags")
    active_plugin_uuid: Optional[UUID] = Field(None, alias="activePluginUuid")

    @property
    def xray_version(self) -> Optional[str]:
        """Backward compatibility (moved to `versions.xray` in v2.8.x)"""
        return self.versions.xray if self.versions else None

    @property
    def node_version(self) -> Optional[str]:
        """Backward compatibility (moved to `versions.node` in v2.8.x)"""
        return self.versions.node if self.versions else None

    @property
    def cpu_count(self) -> Optional[int]:
        """Backward compatibility (moved to `system.info.cpus` in v2.8.x)"""
        return self.system.info.cpus if self.system and self.system.info else None

    @property
    def cpu_model(self) -> Optional[str]:
        """Backward compatibility (moved to `system.info.cpu_model` in v2.8.x)"""
        return self.system.info.cpu_model if self.system and self.system.info else None

    @property
    def total_ram(self) -> Optional[float]:
        """Backward compatibility (moved to `system.info.memory_total` in v2.8.x)"""
        return self.system.info.memory_total if self.system and self.system.info else None


class CreateNodeResponseDto(NodeResponseDto):
    pass


class UpdateNodeResponseDto(NodeResponseDto):
    pass


class GetOneNodeResponseDto(NodeResponseDto):
    pass


class GetAllNodesResponseDto(RootModel[List[NodeResponseDto]]):
    root: List[NodeResponseDto]

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



class EnableNodeResponseDto(NodeResponseDto):
    pass


class DisableNodeResponseDto(NodeResponseDto):
    pass


class RestartNodeResponseDto(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class RestartAllNodesResponseDto(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class ResetNodeTrafficResponseDto(BaseModel):
    event_sent: bool = Field(alias="eventSent")


class ReorderNodeResponseDto(RootModel[List[NodeResponseDto]]):
    root: List[NodeResponseDto]

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


class DeleteNodeResponseDto(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")

    def __bool__(self):
        return self.is_deleted


class RestartAllNodesRequestBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    force_restart: bool = Field(default=False, alias="forceRestart")


class RestartNodeRequestBodyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    force_restart: bool = Field(default=False, alias="forceRestart")

class ResetNodeTrafficRequestDto(BaseModel):
    uuid: Union[str, UUID] = Field(alias="uuid")

class ResetNodeTrafficResponseDto(RestartEventResponse):
    pass

class ConfigProfileData(BaseModel):
    """Config profile data for modification"""
    active_config_profile_uuid: str = Field(alias="activeConfigProfileUuid")
    active_inbounds: List[str] = Field(alias="activeInbounds", min_length=1)


class ProfileModificationRequestDto(BaseModel):
    """Request to modify profiles for multiple nodes"""
    uuids: List[str] = Field(min_length=1)
    config_profile: ConfigProfileData = Field(alias="configProfile")


class ProfileModificationResponseData(BaseModel):
    """Profile modification response data"""
    event_sent: bool = Field(alias="eventSent")


class ProfileModificationResponseDto(ProfileModificationResponseData):
    """Profile modification response"""
    pass

# Для обратной совместимости
RestartAllNodesRequestDto = RestartAllNodesRequestBodyDto
NodesResponseDto = NodeResponseDto


NodeBulkActionType = Literal["ENABLE", "DISABLE", "RESTART", "RESET_TRAFFIC"]


class NodesBulkActionsRequestDto(BaseModel):
    """Request for performing bulk actions on nodes"""
    uuids: List[UUID] = Field(min_length=1)
    action: NodeBulkActionType = Field(description="Action to perform on nodes")


class NodesBulkActionsResponseDto(BaseModel):
    """Response after performing bulk actions on nodes"""
    event_sent: bool = Field(alias="eventSent")


class BulkNodesUpdateFieldsDto(BaseModel):
    """Fields to update in a bulk nodes update request"""
    country_code: Optional[str] = Field(None, serialization_alias="countryCode")
    consumption_multiplier: Optional[float] = Field(None, serialization_alias="consumptionMultiplier")
    node_consumption_multiplier: Optional[float] = Field(None, serialization_alias="nodeConsumptionMultiplier")
    provider_uuid: Optional[UUID] = Field(None, serialization_alias="providerUuid")
    tags: Optional[List[str]] = Field(None, serialization_alias="tags")
    active_plugin_uuid: Optional[UUID] = Field(None, serialization_alias="activePluginUuid")
    note: Optional[str] = Field(None, serialization_alias="note")


class BulkNodesUpdateRequestDto(BaseModel):
    """Bulk nodes update request: node UUIDs + fields to update"""
    uuids: List[UUID] = Field(min_length=1)
    fields: BulkNodesUpdateFieldsDto


class BulkNodesUpdateResponseDto(NodesBulkActionsResponseDto):
    """OpenAPI alias for bulk nodes update response"""
    pass
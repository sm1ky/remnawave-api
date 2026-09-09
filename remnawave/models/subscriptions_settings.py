from datetime import datetime
from typing import Annotated, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

from remnawave.enums import (
    ResponseRuleConditionOperator,
    ResponseRuleOperator,
    ResponseRuleVersion,
    ResponseType,
    SubscriptionType,
)
from remnawave.models.hosts import HostTag


class ResponseRuleCondition(BaseModel):
    """Condition to check against request headers"""
    header_name: Annotated[str, StringConstraints(pattern=r"^[!#$%&'*+\-.0-9A-Z^_`a-z|~]+$")] = Field(
        alias="headerName"
    )
    operator: ResponseRuleConditionOperator
    value: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    case_sensitive: bool = Field(alias="caseSensitive")


class ResponseModificationHeader(BaseModel):
    """Response header modification"""
    key: Annotated[str, StringConstraints(pattern=r"^[!#$%&'*+\-.0-9A-Z^_`a-z|~]+$")]
    value: Annotated[str, StringConstraints(min_length=1)]


class ResponseModificationEncryption(BaseModel):
    """Encryption applied to the response body when the rule matches"""
    method: Literal["age1", "age1pq1"]
    key: str


class ResponseModifications(BaseModel):
    """Response modifications to apply when rule matches"""
    headers: Optional[List[ResponseModificationHeader]] = None
    apply_headers_to_end: Optional[bool] = Field(
        None,
        alias="applyHeadersToEnd",
        description=(
            "If True, SRR headers are appended at the very end of the response "
            "and may override headers from other sections."
        ),
    )
    subscription_template: Optional[Annotated[str, StringConstraints(min_length=1)]] = Field(
        None, alias="subscriptionTemplate"
    )
    ignore_host_xray_json_template: Optional[bool] = Field(
        None,
        alias="ignoreHostXrayJsonTemplate",
        description=(
            "If True, the Host's own Xray Json Template is ignored and the "
            "template defined by the SRR rule is used instead."
        ),
    )
    ignore_serve_json_at_base_subscription: Optional[bool] = Field(
        None,
        alias="ignoreServeJsonAtBaseSubscription",
        description=(
            "If True, the Serve JSON at Base Subscription setting is ignored "
            "(treated as False)."
        ),
    )
    additional_extended_clients_regex: Optional[
        List[Annotated[str, StringConstraints(min_length=1)]]
    ] = Field(
        None,
        alias="additionalExtendedClientsRegex",
        description="Extra user-agent patterns treated as extended clients.",
    )
    disable_hwid_check: Optional[bool] = Field(
        None,
        alias="disableHwidCheck",
        description="If True, the HWID device check is skipped for the matched request.",
    )
    encryption: Optional[ResponseModificationEncryption] = Field(
        None, description="Encrypt the response body with the given method and key."
    )
    exclude_hosts_by_tags: Optional[List[HostTag]] = Field(
        None,
        alias="excludeHostsByTags",
        min_length=1,
        description="Hosts carrying any of these tags are excluded from the response.",
    )
    respond_with_remarks: Optional[List[str]] = Field(
        None,
        alias="respondWithRemarks",
        description=(
            "Replaces the response body with the given remarks. With more than one "
            "element no actual hosts are sent."
        ),
    )


class ResponseRule(BaseModel):
    """Individual response rule configuration"""
    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    description: Optional[Annotated[str, StringConstraints(min_length=1, max_length=250)]] = None
    enabled: bool
    operator: ResponseRuleOperator
    conditions: List[ResponseRuleCondition]
    response_type: ResponseType = Field(alias="responseType")
    response_modifications: Optional[ResponseModifications] = Field(
        None, alias="responseModifications"
    )


class ResponseRulesSettings(BaseModel):
    """Settings for response rules"""
    model_config = {"populate_by_name": True}

    disable_subscription_access_by_path: Optional[bool] = Field(
        None, alias="disableSubscriptionAccessByPath"
    )


class ResponseRules(BaseModel):
    """Response rules configuration"""
    version: ResponseRuleVersion
    rules: List[ResponseRule]
    settings: Optional[ResponseRulesSettings] = None


class CustomRemarksDto(BaseModel):
    """Custom remarks for different user states"""
    expired_users: List[str] = Field(alias="expiredUsers", min_length=1)
    limited_users: List[str] = Field(alias="limitedUsers", min_length=1)
    disabled_users: List[str] = Field(alias="disabledUsers", min_length=1)
    empty_hosts: List[str] = Field(alias="emptyHosts", min_length=1)
    hwid_max_devices_exceeded: List[str] = Field(alias="HWIDMaxDevicesExceeded", min_length=1)
    hwid_not_supported: List[str] = Field(alias="HWIDNotSupported", min_length=1)


class HwidSettingsDto(BaseModel):
    """HWID (Hardware ID) settings"""
    enabled: bool
    fallback_device_limit: int = Field(alias="fallbackDeviceLimit")
    max_devices_announce: Optional[Annotated[str, StringConstraints(max_length=200)]] = Field(
        None, alias="maxDevicesAnnounce"
    )

class SubscriptionSettingsResponseDto(BaseModel):
    """Subscription settings response data"""
    uuid: UUID
    serve_json_at_base_subscription: bool = Field(alias="serveJsonAtBaseSubscription")
    show_custom_remarks: bool = Field(alias="isShowCustomRemarks")
    
    custom_remarks: CustomRemarksDto = Field(alias="customRemarks")
    
    custom_response_headers: Optional[Dict[str, str]] = Field(None, alias="customResponseHeaders")
    randomize_hosts: bool = Field(alias="randomizeHosts")
    response_rules: Optional[ResponseRules] = Field(None, alias="responseRules")
    
    hwid_settings: Optional[HwidSettingsDto] = Field(None, alias="hwidSettings")
    
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class GetSubscriptionSettingsResponseDto(SubscriptionSettingsResponseDto):
    pass


class UpdateSubscriptionSettingsResponseDto(SubscriptionSettingsResponseDto):
    pass


class UpdateSubscriptionSettingsRequestDto(BaseModel):
    """Update subscription settings request"""
    uuid: UUID
    serve_json_at_base_subscription: Optional[bool] = Field(
        None, serialization_alias="serveJsonAtBaseSubscription"
    )
    is_show_custom_remarks: Optional[bool] = Field(None, serialization_alias="isShowCustomRemarks")
    
    custom_remarks: Optional[CustomRemarksDto] = Field(None, serialization_alias="customRemarks")
    
    custom_response_headers: Optional[Dict[str, str]] = Field(
        None, serialization_alias="customResponseHeaders"
    )
    randomize_hosts: Optional[bool] = Field(None, serialization_alias="randomizeHosts")
    response_rules: Optional[ResponseRules] = Field(None, serialization_alias="responseRules")
    
    hwid_settings: Optional[HwidSettingsDto] = Field(None, serialization_alias="hwidSettings")


# Backward compatibility aliases
CustomRemarks = CustomRemarksDto
HwidSettings = HwidSettingsDto
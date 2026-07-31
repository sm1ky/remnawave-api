from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────────────────────
# Fetch IPs – step 1: start the job
# ─────────────────────────────────────────────────────────────────────────────

class FetchIpsJobData(BaseModel):
    """Returned job ID after requesting IP fetch"""
    job_id: str = Field(alias="jobId")


class FetchIpsResponseDto(FetchIpsJobData):
    """Response for POST /api/ip-control/fetch-ips/{uuid}"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Fetch IPs – step 2: poll the job result
# ─────────────────────────────────────────────────────────────────────────────

class FetchIpsProgressData(BaseModel):
    """Progress information for an IP-fetch job"""
    total: int
    completed: int
    percent: float


class FetchIpsNodeResult(BaseModel):
    """Per-node IP list for a user"""
    node_uuid: UUID = Field(alias="nodeUuid")
    node_name: str = Field(alias="nodeName")
    country_code: str = Field(alias="countryCode")
    ips: List[str]


class FetchIpsResult(BaseModel):
    """Full result payload when the job is completed"""
    success: bool
    user_uuid: UUID = Field(alias="userUuid")
    user_id: str = Field(alias="userId")
    nodes: List[FetchIpsNodeResult]


class FetchIpsResultData(BaseModel):
    """Job state + optional result"""
    is_completed: bool = Field(alias="isCompleted")
    is_failed: bool = Field(alias="isFailed")
    progress: FetchIpsProgressData
    result: Optional[FetchIpsResult] = None


class FetchIpsResultResponseDto(FetchIpsResultData):
    """Response for GET /api/ip-control/fetch-ips/result/{jobId}"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Drop Connections request – discriminated unions for dropBy / targetNodes
# ─────────────────────────────────────────────────────────────────────────────

class DropByUserUuids(BaseModel):
    """Drop connections for specific user ids (Remnawave API v3.0.0)."""
    by: Literal["userIds"] = "userIds"
    user_ids: List[int] = Field(
        ...,
        serialization_alias="userIds",
        min_length=1,
        description="List of user ids whose connections should be dropped",
    )


class DropByIpAddresses(BaseModel):
    """Drop connections from specific IP addresses"""
    by: Literal["ipAddresses"] = "ipAddresses"
    ip_addresses: List[str] = Field(
        ...,
        serialization_alias="ipAddresses",
        min_length=1,
        description="List of IP addresses to disconnect",
    )


# Discriminated union – use `by` field as the discriminator
DropBy = Annotated[
    Union[DropByUserUuids, DropByIpAddresses],
    Field(discriminator="by"),
]


class TargetAllNodes(BaseModel):
    """Send the drop-connections event to all connected nodes"""
    target: Literal["allNodes"] = "allNodes"


class TargetSpecificNodes(BaseModel):
    """Send the drop-connections event to specific nodes only"""
    target: Literal["specificNodes"] = "specificNodes"
    node_uuids: List[UUID] = Field(
        ...,
        serialization_alias="nodeUuids",
        min_length=1,
        description="List of node UUIDs to target",
    )


# Discriminated union – use `target` field as the discriminator
TargetNodes = Annotated[
    Union[TargetAllNodes, TargetSpecificNodes],
    Field(discriminator="target"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Fetch Users IPs – step 1: start the job
# ─────────────────────────────────────────────────────────────────────────────

class FetchUsersIpsJobData(BaseModel):
    """Returned job ID after requesting users IP fetch"""
    job_id: str = Field(alias="jobId")


class FetchUsersIpsResponseDto(FetchUsersIpsJobData):
    """Response for POST /api/ip-control/fetch-users-ips/{nodeUuid}"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Fetch Users IPs – step 2: poll the job result
# ─────────────────────────────────────────────────────────────────────────────

class FetchUsersIpsUserIp(BaseModel):
    """IP entry with last seen timestamp"""
    ip: str
    last_seen: datetime = Field(alias="lastSeen")


class FetchUsersIpsUser(BaseModel):
    """Per-user IP list"""
    user_id: str = Field(alias="userId")
    ips: List[FetchUsersIpsUserIp]


class FetchUsersIpsResult(BaseModel):
    """Full result payload when the job is completed"""
    success: bool
    node_uuid: UUID = Field(alias="nodeUuid")
    users: List[FetchUsersIpsUser]


class FetchUsersIpsResultData(BaseModel):
    """Job state + optional result"""
    is_completed: bool = Field(alias="isCompleted")
    is_failed: bool = Field(alias="isFailed")
    result: Optional[FetchUsersIpsResult] = None


class FetchUsersIpsResultResponseDto(FetchUsersIpsResultData):
    """Response for GET /api/ip-control/fetch-users-ips/result/{jobId}"""
    pass


class DropConnectionsRequestDto(BaseModel):
    """Request body for POST /api/ip-control/drop-connections"""
    drop_by: DropBy = Field(
        ...,
        serialization_alias="dropBy",
        description="Selector for whose connections to drop",
    )
    target_nodes: TargetNodes = Field(
        ...,
        serialization_alias="targetNodes",
        description="Selector for which nodes to send the drop event to",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Drop Connections response
# ─────────────────────────────────────────────────────────────────────────────

class DropConnectionsResponseData(BaseModel):
    """Payload confirming the drop-connections event was sent"""
    event_sent: bool = Field(alias="eventSent")


class DropConnectionsResponseDto(DropConnectionsResponseData):
    """Response for POST /api/ip-control/drop-connections"""
    pass

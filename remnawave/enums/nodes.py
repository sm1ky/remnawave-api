from enum import StrEnum


class NodeIpStatus(StrEnum):
    """Role of an IP address declared on a node."""

    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    MANAGEMENT = "MANAGEMENT"
    TRANSIT = "TRANSIT"
    MONITORING = "MONITORING"
    RESERVE = "RESERVE"
    BLOCKED = "BLOCKED"
    FLAGGED = "FLAGGED"
    DEPRECATED = "DEPRECATED"
    UNKNOWN = "UNKNOWN"

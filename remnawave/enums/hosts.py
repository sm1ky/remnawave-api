from enum import StrEnum


class InternalSquadsMode(StrEnum):
    """How a host treats the internal squads listed in ``internalSquads.squads``."""

    EXCLUDE = "EXCLUDE"
    ALLOW_ONLY = "ALLOW_ONLY"


class HostMapperOperation(StrEnum):
    """Operation applied to the generated config entry of a host."""

    COPY = "copy"
    SET = "set"
    UNSET = "unset"

"""ErrorCode / exception-mapping conformance against the bundled OpenAPI document.

Offline test: the panel lists its error codes in three DTOs, so both the enum and
the exception mapping can be checked against them directly.
"""
import json
from pathlib import Path

import pytest

from remnawave.enums import ErrorCode
from remnawave.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    ServerError,
)
from remnawave.exceptions.handler import ERRORS

SPEC_PATH = Path(__file__).resolve().parent.parent / "openapi" / "remna-3-4-3.json"

# openapi/ is not tracked by git, so these checks only run in a working copy that
# has the spec next to the sources.
pytestmark = pytest.mark.skipif(
    not SPEC_PATH.exists(), reason=f"OpenAPI spec not available: {SPEC_PATH}"
)

# The panel reuses each of these for two unrelated errors, so only the HTTP status
# can pick the exception class — they are intentionally left unmapped.
REUSED_CODES = {"A089", "A219"}

GROUP_EXCEPTION = {
    "RemnawaveNotFoundErrorDto": NotFoundError,
    "RemnawaveInternalServerErrorDto": ServerError,
}

# `message` is a parallel enum that JSON-Schema dedup shortened by one entry in the
# bad-request DTO: the first 12 codes align 1:1, the rest are shifted by one.
BAD_REQUEST_SPLIT = 12


def _pairs(schemas, dto, split=None):
    codes = schemas[dto]["properties"]["errorCode"]["enum"]
    messages = schemas[dto]["properties"]["message"]["enum"]
    if split is None:
        assert len(codes) == len(messages), dto
        return list(zip(codes, messages))
    return [(codes[i], messages[i]) for i in range(split)] + [
        (codes[i], messages[i - 1]) for i in range(split, len(codes))
    ]


@pytest.fixture(scope="module")
def spec_codes() -> dict[str, list[tuple[str, str]]]:
    schemas = json.loads(SPEC_PATH.read_text(encoding="utf-8"))["components"]["schemas"]
    groups = {
        "RemnawaveBadRequestErrorDto": _pairs(
            schemas, "RemnawaveBadRequestErrorDto", split=BAD_REQUEST_SPLIT
        ),
        "RemnawaveNotFoundErrorDto": _pairs(schemas, "RemnawaveNotFoundErrorDto"),
        "RemnawaveInternalServerErrorDto": _pairs(
            schemas, "RemnawaveInternalServerErrorDto"
        ),
    }
    out: dict[str, list[tuple[str, str]]] = {}
    for dto, pairs in groups.items():
        for code, message in pairs:
            out.setdefault(code, []).append((dto, message))
    return out


def test_every_panel_code_is_an_enum_member(spec_codes):
    known = {member.value for member in ErrorCode}
    missing = sorted(code for code in spec_codes if code not in known)
    assert not missing, f"Codes the panel can send but the SDK does not define: {missing}"


def test_enum_member_names_are_unique(spec_codes):
    names = [member.name for member in ErrorCode]
    assert len(names) == len(set(names))


def test_every_panel_code_maps_to_an_exception(spec_codes):
    unmapped = sorted(
        code for code in spec_codes if code not in ERRORS and code not in REUSED_CODES
    )
    assert not unmapped, f"Codes without an exception class: {unmapped}"


def test_reused_codes_stay_unmapped(spec_codes):
    """Both belong to two DTOs at once; mapping either one would guess wrong half the time."""
    for code in REUSED_CODES:
        assert len({dto for dto, _ in spec_codes[code]}) > 1
        assert code not in ERRORS


def test_exception_class_matches_the_declaring_dto(spec_codes):
    wrong = []
    for code, entries in spec_codes.items():
        if code in REUSED_CODES:
            continue
        dto, message = entries[0]
        expected = GROUP_EXCEPTION.get(dto)
        if expected is None:  # bad request: "already exists" is reported as a conflict
            expected = ConflictError if "already exists" in message.lower() else BadRequestError
        if ERRORS.get(code) is not expected:
            wrong.append((code, message, ERRORS.get(code), expected))
    assert not wrong, wrong


class TestCodesObservedOnALivePanel:
    """Pairs captured from a real 3.4.3 panel, so they pin the spec's own alignment."""

    OBSERVED = {
        "A019": ("User username already exists", ConflictError),
        "A033": ("Node name already exists", ConflictError),
        "A034": ("Node address already exists", ConflictError),
        "A098": ("User hwid device already exists", ConflictError),
        "A112": ("Create config profile error", ServerError),
        "A144": ("This name is reserved by Remnawave. Please use a different name.", BadRequestError),
        "A145": ("This name is reserved by Remnawave. Please use a different name.", BadRequestError),
        "A152": ("Name or config is required", BadRequestError),
        "A153": ("Name or inbounds is required", BadRequestError),
        "A164": ("Snippet name already exists", ConflictError),
        "A166": ("Snippet cannot be empty", BadRequestError),
        "A167": ("Snippet cannot contain empty objects", BadRequestError),
        "A172": ("This name is reserved. Please use a different name.", BadRequestError),
        "A173": ("Template JSON is not allowed for YAML template", BadRequestError),
        "A189": ("External squad name already exists", ConflictError),
        "A210": ("Config name already exists", ConflictError),
        "A212": ("Reserved subpage config cannot be deleted", BadRequestError),
        "A244": ("Node integration name already exists", ConflictError),
        "A245": ("Shared list not found", NotFoundError),
        "A246": ("Shared list name already exists", ConflictError),
    }

    @pytest.mark.parametrize("code", sorted(OBSERVED))
    def test_message_matches_the_spec(self, spec_codes, code):
        expected_message, _ = self.OBSERVED[code]
        assert expected_message in [message for _, message in spec_codes[code]]

    @pytest.mark.parametrize("code", sorted(OBSERVED))
    def test_exception_class(self, code):
        _, expected = self.OBSERVED[code]
        assert ERRORS[code] is expected


class TestRepointedMembers:
    """Names that were always right but carried a value from an older API version."""

    @pytest.mark.parametrize(
        "member, code",
        [
            ("INBOUND_NOT_FOUND", "A076"),
            ("CONFIG_PROFILE_NOT_FOUND", "A111"),
            ("CREATE_CONFIG_PROFILE_ERROR", "A112"),
            ("INTERNAL_SQUAD_NOT_FOUND", "A118"),
            ("CREATE_INTERNAL_SQUAD_ERROR", "A119"),
            ("UPDATE_INTERNAL_SQUAD_ERROR", "A121"),
            ("DELETE_INTERNAL_SQUAD_ERROR", "A122"),
            ("UPDATE_CONFIG_PROFILE_ERROR", "A146"),
            ("SNIPPET_NOT_FOUND", "A162"),
            ("SNIPPET_NAME_ALREADY_EXISTS", "A164"),
            ("UPDATE_SNIPPET_ERROR", "A165"),
            ("SUBSCRIPTION_TEMPLATE_NOT_FOUND", "A170"),
            ("UPDATE_SUBSCRIPTION_TEMPLATE_ERROR", "A171"),
            ("DELETE_SUBSCRIPTION_TEMPLATE_ERROR", "A177"),
            ("EXTERNAL_SQUAD_NOT_FOUND", "A182"),
            ("CREATE_EXTERNAL_SQUAD_ERROR", "A183"),
            ("UPDATE_EXTERNAL_SQUAD_ERROR", "A184"),
            ("DELETE_EXTERNAL_SQUAD_ERROR", "A185"),
            ("ADD_USERS_TO_EXTERNAL_SQUAD_ERROR", "A186"),
            ("REMOVE_USERS_FROM_EXTERNAL_SQUAD_ERROR", "A187"),
            ("EXTERNAL_SQUAD_NAME_ALREADY_EXISTS", "A189"),
            ("PASSKEY_NOT_FOUND", "A191"),
            ("GET_REMNAWAVE_SETTINGS_ERROR", "A192"),
            ("UPDATE_REMNAWAVE_SETTINGS_ERROR", "A193"),
            ("DELETE_PASSKEY_ERROR", "A199"),
        ],
    )
    def test_value(self, spec_codes, member, code):
        assert getattr(ErrorCode, member).value == code
        # the member name is exactly what the panel's message reduces to
        assert code in spec_codes


class TestCodesKeptOutsideTheSpec:
    """Codes the current DTOs no longer list; the SDK still maps them."""

    @pytest.mark.parametrize(
        "member, code",
        [
            ("UNAUTHORIZED", "A003"),
            ("FORBIDDEN_ROLE_ERROR", "A004"),
            ("ENABLED_NODES_NOT_FOUND", "A054"),
            ("CONFIG_VALIDATION_ERROR", "A061"),
            ("FORBIDDEN_ONE", "A068"),
            ("CREATE_WEBHOOK_ERROR", "A113"),
            ("WEBHOOK_NOT_FOUND", "A114"),
        ],
    )
    def test_still_defined(self, spec_codes, member, code):
        assert getattr(ErrorCode, member).value == code
        assert code not in spec_codes

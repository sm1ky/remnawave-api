"""Route coverage of the bundled Remnawave OpenAPI spec.

Offline test: it introspects the decorated controller methods and compares the
resulting ``(METHOD, path)`` set against ``openapi/remna-3-4-3.json``.
"""
import inspect
import json
import re
from pathlib import Path as FsPath

import pytest
from rapid_api_client.annotations import Path as PathParam
from rapid_api_client.utils import find_annotation

import remnawave.controllers as controllers
from remnawave.rapid import BaseController

SPEC_PATH = FsPath(__file__).resolve().parent.parent / "openapi" / "remna-3-4-3.json"
HTTP_VERBS = {"GET", "POST", "PUT", "PATCH", "DELETE"}

# openapi/ is not tracked by git, so these checks only run in a working copy that
# has the spec next to the sources.
pytestmark = pytest.mark.skipif(
    not SPEC_PATH.exists(), reason=f"OpenAPI spec not available: {SPEC_PATH}"
)


def _sdk_routes() -> dict[tuple[str, str], list[str]]:
    """Map (METHOD, /api/path) -> ["Controller.method", ...] for every SDK route."""
    routes: dict[tuple[str, str], list[str]] = {}
    for controller_name, controller in inspect.getmembers(controllers, inspect.isclass):
        if not issubclass(controller, BaseController) or controller is BaseController:
            continue
        for method_name, func in inspect.getmembers(controller, inspect.isfunction):
            wrapped = getattr(func, "__wrapped__", None)
            closure = func.__closure__ or (wrapped and wrapped.__closure__)
            if not closure:
                continue
            cells = [cell.cell_contents for cell in closure]
            verb = next((c for c in cells if isinstance(c, str) and c in HTTP_VERBS), None)
            path = next((c for c in cells if isinstance(c, str) and c.startswith("/")), None)
            if verb and path:
                routes.setdefault((verb, "/api" + path), []).append(
                    f"{controller_name}.{method_name}"
                )
    return routes


def _spec_routes() -> set[tuple[str, str]]:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    return {
        (method.upper(), path)
        for path, item in spec["paths"].items()
        for method in item
        if method.upper() in HTTP_VERBS
    }


@pytest.fixture(scope="module")
def sdk_routes() -> dict[tuple[str, str], list[str]]:
    return _sdk_routes()


@pytest.fixture(scope="module")
def spec_routes() -> set[tuple[str, str]]:
    return _spec_routes()


def test_spec_version_is_3_4_3():
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    assert spec["info"]["version"] == "3.4.3"


def test_every_spec_route_is_implemented(sdk_routes, spec_routes):
    missing = sorted(spec_routes - set(sdk_routes), key=lambda r: (r[1], r[0]))
    assert not missing, "Routes present in the spec but missing from the SDK: " + ", ".join(
        f"{verb} {path}" for verb, path in missing
    )


def test_no_sdk_route_is_absent_from_the_spec(sdk_routes, spec_routes):
    extra = sorted(set(sdk_routes) - spec_routes, key=lambda r: (r[1], r[0]))
    assert not extra, "Routes implemented by the SDK but absent from the spec: " + ", ".join(
        f"{verb} {path} ({', '.join(sdk_routes[(verb, path)])})" for verb, path in extra
    )


def test_every_path_placeholder_is_bound(sdk_routes):
    """A ``{placeholder}`` without a Path()-annotated argument raises KeyError at call time."""
    unbound = []
    for controller_name, controller in inspect.getmembers(controllers, inspect.isclass):
        if not issubclass(controller, BaseController) or controller is BaseController:
            continue
        for method_name, func in inspect.getmembers(controller, inspect.isfunction):
            wrapped = getattr(func, "__wrapped__", None)
            closure = func.__closure__ or (wrapped and wrapped.__closure__)
            if not closure:
                continue
            cells = [cell.cell_contents for cell in closure]
            verb = next((c for c in cells if isinstance(c, str) and c in HTTP_VERBS), None)
            path = next((c for c in cells if isinstance(c, str) and c.startswith("/")), None)
            if not (verb and path):
                continue
            placeholders = set(re.findall(r"\{(\w+)\}", path))
            if not placeholders:
                continue
            bound = set()
            for parameter in inspect.signature(wrapped or func).parameters.values():
                annotation = find_annotation(parameter, PathParam)
                if annotation is not None:
                    bound.add(getattr(annotation, "alias", None) or parameter.name)
            if placeholders - bound:
                unbound.append(
                    f"{controller_name}.{method_name} ({verb} {path}): "
                    f"{sorted(placeholders - bound)}"
                )
    assert not unbound, "Path placeholders without a Path() annotation: " + "; ".join(unbound)

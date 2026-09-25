"""Route coverage of the bundled Remnawave OpenAPI spec.

Offline test: it introspects the decorated controller methods and compares the
resulting ``(METHOD, path)`` set against ``openapi/remnawave-3-4-4.json``.
"""
import inspect
import json
import re
from pathlib import Path as FsPath

import pytest
from rapid_api_client.annotations import Path as PathParam, Query as QueryParam
from rapid_api_client.utils import find_annotation

import remnawave.controllers as controllers
from remnawave.rapid import BaseController

SPEC_PATH = FsPath(__file__).resolve().parent.parent / "openapi" / "remnawave-3-4-4.json"
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


def test_spec_version_is_3_4_4():
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    assert spec["info"]["version"] == "3.4.4"


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


def _decorated_routes():
    """Yield (controller, method, verb, path, signature) for every decorated endpoint."""
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
                yield (
                    controller_name,
                    method_name,
                    verb,
                    "/api" + path,
                    inspect.signature(wrapped or func),
                )


def test_every_required_query_param_is_exposed():
    """A required query param with no SDK argument makes the endpoint answer 400 every time."""
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    missing = []
    for controller_name, method_name, verb, path, signature in _decorated_routes():
        operation = spec["paths"].get(path, {}).get(verb.lower())
        if not operation:
            continue
        required = {
            p["name"]
            for p in operation.get("parameters", [])
            if p["in"] == "query" and p.get("required")
        }
        if not required:
            continue
        exposed = set()
        for parameter in signature.parameters.values():
            annotation = find_annotation(parameter, QueryParam)
            if annotation is not None:
                exposed.add(getattr(annotation, "alias", None) or parameter.name)
        if required - exposed:
            missing.append(
                f"{controller_name}.{method_name} ({verb} {path}): {sorted(required - exposed)}"
            )
    assert not missing, "Required query params with no SDK argument: " + "; ".join(missing)


def test_a_body_with_required_fields_is_never_optional():
    """`body=None` on a payload the panel validates means the call always answers 400.

    A required body whose schema has no required property of its own is fine: the panel
    accepts those calls without a payload (revoke-subscription, for one).
    """
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    schemas = spec["components"]["schemas"]

    def resolve(schema, depth=0):
        while isinstance(schema, dict) and "$ref" in schema and depth < 20:
            schema = schemas[schema["$ref"].split("/")[-1]]
            depth += 1
        return schema

    offenders = []
    for controller_name, method_name, verb, path, signature in _decorated_routes():
        operation = spec["paths"].get(path, {}).get(verb.lower())
        if not operation:
            continue
        body = operation.get("requestBody")
        if not body or not body.get("required"):
            continue
        schema = resolve(body.get("content", {}).get("application/json", {}).get("schema", {}))
        if not schema.get("required"):
            continue
        parameter = signature.parameters.get("body")
        if parameter is not None and parameter.default is None:
            offenders.append(
                f"{controller_name}.{method_name} ({verb} {path}) needs {schema['required']}"
            )
    assert not offenders, "Request body defaults to None despite required fields: " + "; ".join(
        offenders
    )

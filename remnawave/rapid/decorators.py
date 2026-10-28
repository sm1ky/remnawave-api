from functools import partial, wraps
from inspect import signature
from typing import Any, Callable, Coroutine, Type

from httpx import AsyncClient, Response
from pydantic import TypeAdapter

from .client import BaseController, CustomRapidParameters
from .typing import BM, T


def http(
    method: str,
    path: str,
    response_class: Type[BM | str | bytes | Response] | TypeAdapter[T] = Response,
    timeout: float | None = None,
) -> Callable[
    [Callable], Callable[..., Coroutine[Any, Any, BM | str | bytes | Response | T]]
]:
    def decorator(
        func: Callable,
    ) -> Callable[..., Coroutine[Any, Any, BM | str | bytes | Response | T]]:
        sig = signature(func)
        rapid_parameters = CustomRapidParameters.from_sig(sig)

        @wraps(func)
        async def wrapper(
            api: BaseController, *args, **kwargs
        ) -> BM | str | bytes | Response | T:
            assert isinstance(
                api, BaseController
            ), f"{api} should be an instance of BaseController"
            assert isinstance(
                api.client, AsyncClient
            ), f"{api.client} should be an instance of httpx.AsyncClient"

            # noinspection PyProtectedMember
            request = api._build_request(
                sig, rapid_parameters, method, path, (api,) + args, kwargs, timeout
            )
            response = await api.client.send(request)
            # noinspection PyProtectedMember
            return api._handle_response(response, response_class=response_class)

        return wrapper

    return decorator


get = partial(http, "GET")
post = partial(http, "POST")
delete = partial(http, "DELETE")
put = partial(http, "PUT")
patch = partial(http, "PATCH")

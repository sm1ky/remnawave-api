from typing import Annotated

from rapid_api_client import Path

from remnawave.enums import ClientType
from remnawave.models import GetSubscriptionInfoResponseDto
from remnawave.rapid import BaseController, get


class SubscriptionController(BaseController):
    # Public endpoints below
    @get("/sub/{shortUuid}/info", response_class=GetSubscriptionInfoResponseDto)
    async def get_subscription_info_by_short_uuid(
        self,
        short_uuid: Annotated[str, Path(description="Short UUID of the user", alias="shortUuid")],
    ) -> GetSubscriptionInfoResponseDto:
        """None"""
        ...

    @get("/sub/{shortUuid}", response_class=str)
    async def get_subscription(
        self,
        short_uuid: Annotated[str, Path(description="Short UUID of the user", alias="shortUuid")],
    ) -> str:
        """None"""
        ...

    @get("/sub/{shortUuid}/{clientType}", response_class=str)
    async def get_subscription_by_client_type(
        self,
        client_type: Annotated[ClientType, Path(description="Client type", alias="clientType")],
        short_uuid: Annotated[str, Path(description="Short UUID of the user", alias="shortUuid")],
    ) -> str:
        """None"""
        ...
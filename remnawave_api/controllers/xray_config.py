from typing import Annotated

from rapid_api_client.annotations import JsonBody

from remnawave_api.models import ConfigResponseDto
from remnawave_api.rapid import BaseController, get, put


class XrayConfigController(BaseController):
    @get("/xray", response_class=ConfigResponseDto)
    async def get_config(
        self,
    ) -> ConfigResponseDto:
        """Get Xray Config"""
        ...

    @put("/xray", response_class=ConfigResponseDto)
    async def update_config(
        self,
        body: Annotated[dict, JsonBody()],
    ) -> ConfigResponseDto:
        """Update Xray Config"""
        ...

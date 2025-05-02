from typing import Annotated

from rapid_api_client.annotations import Path, PydanticBody

from remnawave_api.enums import TemplateType
from remnawave_api.models import TemplateResponseDto, UpdateTemplateRequestDto
from remnawave_api.rapid import BaseController, get, put


class SubscriptionsTemplateController(BaseController):
    @get(
        "/subscription-templates/{template_type}",
        response_class=TemplateResponseDto,
    )
    async def get_template(
        self,
        template_type: Annotated[TemplateType, Path(description="Template type")],
    ) -> TemplateResponseDto:
        """Get Template"""
        ...

    @put(
        "/subscription-templates",
        response_class=TemplateResponseDto,
    )
    async def update_template(
        self,
        body: Annotated[UpdateTemplateRequestDto, PydanticBody()],
    ) -> TemplateResponseDto:
        """Update Template"""
        ...

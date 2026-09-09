from typing import Annotated

from rapid_api_client.annotations import Path, PydanticBody

from remnawave.enums import TemplateType
from remnawave.models import (
    CreateSubscriptionTemplateRequestDto,
    CreateSubscriptionTemplateResponseDto,
    DeleteSubscriptionTemplateResponseDto,
    GetTemplateResponseDto,
    GetTemplatesResponseDto,
    ReorderSubscriptionTemplatesRequestDto,
    ReorderSubscriptionTemplatesResponseDto,
    GetSubscriptionTemplatesTagsResponseDto,
    SetSubscriptionTemplatesTagsRequestDto,
    SetSubscriptionTemplatesTagsResponseDto,
    UpdateTemplateRequestDto,
    UpdateTemplateResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class SubscriptionsTemplateController(BaseController):
    @get("/subscription-templates", response_class=GetTemplatesResponseDto)
    async def get_all_templates(self) -> GetTemplatesResponseDto:
        """Get all subscription templates (without content)"""
        ...

    @post("/subscription-templates", response_class=CreateSubscriptionTemplateResponseDto)
    async def create_template(
        self,
        body: Annotated[CreateSubscriptionTemplateRequestDto, PydanticBody()],
    ) -> CreateSubscriptionTemplateResponseDto:
        """Create subscription template"""
        ...

    @patch("/subscription-templates", response_class=UpdateTemplateResponseDto)
    async def update_template(
        self,
        body: Annotated[UpdateTemplateRequestDto, PydanticBody()],
    ) -> UpdateTemplateResponseDto:
        """Update subscription template"""
        ...

    @get("/subscription-templates/{uuid}", response_class=GetTemplateResponseDto)
    async def get_template_by_uuid(
        self,
        uuid: Annotated[str, Path(description="Template UUID")],
    ) -> GetTemplateResponseDto:
        """Get subscription template by uuid"""
        ...

    @delete("/subscription-templates/{uuid}", response_class=None)
    async def delete_template(
        self,
        uuid: Annotated[str, Path(description="Template UUID")],
    ) -> DeleteSubscriptionTemplateResponseDto:
        """Delete subscription template"""
        ...
    @post("/subscription-templates/actions/reorder", response_class=ReorderSubscriptionTemplatesResponseDto)
    async def reorder_templates(
        self,
        body: Annotated[ReorderSubscriptionTemplatesRequestDto, PydanticBody()],
    ) -> ReorderSubscriptionTemplatesResponseDto:
        """Reorder subscription templates"""
        ...

    @get("/subscription-templates/tags", response_class=GetSubscriptionTemplatesTagsResponseDto)
    async def get_subscription_templates_tags(self) -> GetSubscriptionTemplatesTagsResponseDto:
        """Get tags of Subscription Templates"""
        ...

    @patch("/subscription-templates/tags", response_class=SetSubscriptionTemplatesTagsResponseDto)
    async def set_subscription_template_tags(
        self,
        body: Annotated[SetSubscriptionTemplatesTagsRequestDto, PydanticBody()],
    ) -> SetSubscriptionTemplatesTagsResponseDto:
        """Set tags of Subscription Template"""
        ...

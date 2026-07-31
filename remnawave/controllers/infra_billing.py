from typing import Annotated

from rapid_api_client import Path
from rapid_api_client.annotations import PydanticBody

from remnawave.models import (
    CreateInfraBillingHistoryRecordRequestDto,
    CreateInfraBillingHistoryRecordResponseDto,
    CreateInfraBillingNodeRequestDto,
    CreateInfraBillingNodeResponseDto,
    CreateInfraProviderRequestDto,
    CreateInfraProviderResponseDto,
    DeleteInfraBillingHistoryRecordByUuidResponseDto,
    DeleteInfraBillingNodeByUuidResponseDto,
    DeleteInfraProviderByUuidResponseDto,
    GetInfraBillingHistoryRecordsResponseDto,
    GetInfraBillingNodesResponseDto,
    GetInfraProvidersResponseDto,
    GetInfraProviderByUuidResponseDto,
    UpdateInfraBillingNodeRequestDto,
    UpdateInfraBillingNodeResponseDto,
    UpdateInfraProviderRequestDto,
    UpdateInfraProviderResponseDto,
)
from remnawave.rapid import BaseController, delete, get, patch, post


class InfraBillingController(BaseController):
    @get("/infra-billing/providers", response_class=GetInfraProvidersResponseDto)
    async def get_infra_providers(self) -> GetInfraProvidersResponseDto:
        """Get all infra providers"""
        ...

    @post("/infra-billing/providers", response_class=CreateInfraProviderResponseDto)
    async def create_infra_provider(
        self,
        body: Annotated[CreateInfraProviderRequestDto, PydanticBody()],
    ) -> CreateInfraProviderResponseDto:
        """Create infra provider"""
        ...

    @patch("/infra-billing/providers", response_class=UpdateInfraProviderResponseDto)
    async def update_infra_provider(
        self,
        body: Annotated[UpdateInfraProviderRequestDto, PydanticBody()],
    ) -> UpdateInfraProviderResponseDto:
        """Update infra provider"""
        ...

    @get("/infra-billing/providers/{uuid}", response_class=GetInfraProviderByUuidResponseDto)
    async def get_infra_provider_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the infra provider")],
    ) -> GetInfraProviderByUuidResponseDto:
        """Get infra provider by uuid"""
        ...

    @delete("/infra-billing/providers/{uuid}", response_class=None)
    async def delete_infra_provider_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the infra provider")],
    ) -> DeleteInfraProviderByUuidResponseDto:
        """Delete infra provider by uuid"""
        ...

    @post("/infra-billing/history", response_class=CreateInfraBillingHistoryRecordResponseDto)
    async def create_infra_billing_history_record(
        self,
        body: Annotated[CreateInfraBillingHistoryRecordRequestDto, PydanticBody()],
    ) -> CreateInfraBillingHistoryRecordResponseDto:
        """Create infra billing history"""
        ...

    @get("/infra-billing/history", response_class=GetInfraBillingHistoryRecordsResponseDto)
    async def get_infra_billing_history_records(self) -> GetInfraBillingHistoryRecordsResponseDto:
        """Get infra billing history"""
        ...

    @delete("/infra-billing/history/{uuid}", response_class=None)
    async def delete_infra_billing_history_record_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the billing history record")],
    ) -> DeleteInfraBillingHistoryRecordByUuidResponseDto:
        """Delete infra billing history"""
        ...

    @get("/infra-billing/nodes", response_class=GetInfraBillingNodesResponseDto)
    async def get_billing_nodes(self) -> GetInfraBillingNodesResponseDto:
        """Get infra billing nodes"""
        ...

    @patch("/infra-billing/nodes", response_class=UpdateInfraBillingNodeResponseDto)
    async def update_infra_billing_node(
        self,
        body: Annotated[UpdateInfraBillingNodeRequestDto, PydanticBody()],
    ) -> UpdateInfraBillingNodeResponseDto:
        """Update infra billing nodes"""
        ...

    @post("/infra-billing/nodes", response_class=CreateInfraBillingNodeResponseDto)
    async def create_infra_billing_node(
        self,
        body: Annotated[CreateInfraBillingNodeRequestDto, PydanticBody()],
    ) -> CreateInfraBillingNodeResponseDto:
        """Create infra billing node"""
        ...

    @delete("/infra-billing/nodes/{uuid}", response_class=None)
    async def delete_infra_billing_node_by_uuid(
        self,
        uuid: Annotated[str, Path(description="UUID of the infra billing node")],
    ) -> DeleteInfraBillingNodeByUuidResponseDto:
        """Delete infra billing node"""
        ...
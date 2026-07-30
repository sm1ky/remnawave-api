from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class InfraProviderSimpleDto(BaseModel):
    """Упрощенная модель провайдера для billingNodes"""
    uuid: UUID
    name: str
    login_url: Optional[str] = Field(alias="loginUrl")
    favicon_link: Optional[str] = Field(alias="faviconLink")


class InfraBillingHistoryStatsDto(BaseModel):
    """Статистика истории биллинга для провайдера"""
    total_amount: float = Field(alias="totalAmount")
    total_bills: float = Field(alias="totalBills")


class InfraBillingNodeDetailsDto(BaseModel):
    node_uuid: UUID = Field(alias="nodeUuid")
    country_code: str = Field(alias="countryCode")


class InfraBillingNodeSimpleDto(BaseModel):
    """Billing node inside a provider (spec: {name, details})"""
    name: str
    details: InfraBillingNodeDetailsDto


class InfraProviderDto(BaseModel):
    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(None, alias="faviconLink")
    login_url: Optional[str] = Field(None, alias="loginUrl")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    billing_history: InfraBillingHistoryStatsDto = Field(alias="billingHistory")
    billing_nodes: List[InfraBillingNodeSimpleDto] = Field(alias="billingNodes")


class NodeDto(BaseModel):
    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class InfraBillingHistoryProviderDto(BaseModel):
    uuid: UUID
    name: str
    favicon_link: Optional[str] = Field(None, alias="faviconLink")


class InfraBillingHistoryDto(BaseModel):
    uuid: UUID
    provider_uuid: UUID = Field(alias="providerUuid")
    amount: float
    billed_at: Optional[datetime] = Field(None, alias="billedAt")
    provider: Optional[InfraBillingHistoryProviderDto] = None
    # Legacy/optional fields (not part of the 2.8.1 contract)
    node_uuid: Optional[UUID] = Field(None, alias="nodeUuid")
    description: Optional[str] = None
    payment_date: Optional[datetime] = Field(None, alias="paymentDate")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")


class InfraBillingNodeDto(BaseModel):
    uuid: UUID
    node_uuid: UUID = Field(alias="nodeUuid")
    provider_uuid: UUID = Field(alias="providerUuid")
    provider: InfraProviderSimpleDto
    node: NodeDto
    next_billing_at: datetime = Field(alias="nextBillingAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class AvailableBillingNodeDto(BaseModel):
    """Модель для доступных узлов биллинга"""
    uuid: UUID
    name: str
    country_code: str = Field(alias="countryCode")


class BillingStatsDto(BaseModel):
    """Статистика биллинга"""
    upcoming_nodes_count: float = Field(alias="upcomingNodesCount")
    current_month_payments: float = Field(alias="currentMonthPayments")
    total_spent: float = Field(alias="totalSpent")


# Provider models
class CreateInfraProviderRequestDto(BaseModel):
    name: str
    favicon_link: Optional[str] = Field(None, serialization_alias="faviconLink")
    login_url: Optional[str] = Field(None, serialization_alias="loginUrl")


class CreateInfraProviderResponseDto(InfraProviderDto):
    pass


class UpdateInfraProviderRequestDto(BaseModel):
    uuid: UUID
    name: Optional[str] = None
    favicon_link: Optional[str] = Field(None, serialization_alias="faviconLink")
    login_url: Optional[str] = Field(None, serialization_alias="loginUrl")


class UpdateInfraProviderResponseDto(InfraProviderDto):
    pass


class AllInfraProvidersData(BaseModel):
    total: float = Field(alias="total")
    providers: List[InfraProviderDto]


# Исправленные имена моделей согласно OpenAPI
class GetInfraProvidersResponseDto(AllInfraProvidersData):
    pass


class GetInfraProviderByUuidResponseDto(InfraProviderDto):
    pass


class DeleteInfraProviderByUuidResponseDto(BaseModel):
    is_deleted: bool = Field(alias="isDeleted")


# Billing History models
class CreateInfraBillingHistoryRecordRequestDto(BaseModel):
    """Модель для создания записи истории биллинга"""
    provider_uuid: UUID = Field(serialization_alias="providerUuid")
    amount: float = Field(ge=0)
    billed_at: datetime = Field(serialization_alias="billedAt")


class InfraBillingHistoryData(BaseModel):
    records: List[InfraBillingHistoryDto]
    total: float


class CreateInfraBillingHistoryRecordResponseDto(InfraBillingHistoryData):
    pass


class GetInfraBillingHistoryRecordsResponseDto(InfraBillingHistoryData):
    pass


class DeleteInfraBillingHistoryRecordByUuidResponseDto(InfraBillingHistoryData):
    pass


# Billing Nodes models
class CreateInfraBillingNodeRequestDto(BaseModel):
    provider_uuid: UUID = Field(serialization_alias="providerUuid")
    node_uuid: UUID = Field(serialization_alias="nodeUuid")
    name: str = Field(serialization_alias="name", min_length=1, max_length=255)
    next_billing_at: datetime = Field(serialization_alias="nextBillingAt")


# ИСПРАВЛЕНО: API возвращает список всех billing nodes после создания, а не один созданный
class CreateInfraBillingNodeResponseDto(BaseModel):
    total_billing_nodes: float = Field(alias="totalBillingNodes")
    billing_nodes: List[InfraBillingNodeDto] = Field(alias="billingNodes")
    available_billing_nodes: List[AvailableBillingNodeDto] = Field(alias="availableBillingNodes")
    total_available_billing_nodes: float = Field(alias="totalAvailableBillingNodes")
    stats: BillingStatsDto


class UpdateInfraBillingNodeRequestDto(BaseModel):
    uuids: List[UUID]
    next_billing_at: datetime = Field(serialization_alias="nextBillingAt")


class UpdateInfraBillingNodeResponseDto(BaseModel):
    total_billing_nodes: float = Field(alias="totalBillingNodes")
    billing_nodes: List[InfraBillingNodeDto] = Field(alias="billingNodes")
    available_billing_nodes: List[AvailableBillingNodeDto] = Field(alias="availableBillingNodes")
    total_available_billing_nodes: float = Field(alias="totalAvailableBillingNodes")
    stats: BillingStatsDto


class InfraBillingNodesData(BaseModel):
    total_billing_nodes: float = Field(alias="totalBillingNodes")
    billing_nodes: List[InfraBillingNodeDto] = Field(alias="billingNodes")
    available_billing_nodes: List[AvailableBillingNodeDto] = Field(alias="availableBillingNodes")
    total_available_billing_nodes: float = Field(alias="totalAvailableBillingNodes")
    stats: BillingStatsDto


class GetInfraBillingNodesResponseDto(InfraBillingNodesData):
    pass


class DeleteInfraBillingNodeByUuidResponseDto(BaseModel):
    """API возвращает обновленный список billing nodes после удаления"""
    total_billing_nodes: float = Field(alias="totalBillingNodes")
    billing_nodes: List[InfraBillingNodeDto] = Field(alias="billingNodes")
    available_billing_nodes: List[AvailableBillingNodeDto] = Field(alias="availableBillingNodes")
    total_available_billing_nodes: float = Field(alias="totalAvailableBillingNodes")
    stats: BillingStatsDto


# Legacy aliases для обратной совместимости
GetAllInfraProvidersResponseDto = GetInfraProvidersResponseDto
DeleteInfraProviderResponseDto = DeleteInfraProviderByUuidResponseDto
GetAllInfraBillingHistoryResponseDto = GetInfraBillingHistoryRecordsResponseDto
GetInfraBillingHistoryByUuidResponseDto = InfraBillingHistoryDto
GetAllInfraBillingNodesResponseDto = GetInfraBillingNodesResponseDto
GetInfraBillingNodeByUuidResponseDto = InfraBillingNodeDto
DeleteInfraBillingNodeResponseDto = DeleteInfraBillingNodeByUuidResponseDto
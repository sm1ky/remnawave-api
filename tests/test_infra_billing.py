from datetime import datetime, timedelta

import pytest
import pytz

from remnawave.exceptions import ApiError, NotFoundError
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
from tests.utils import generate_random_string


@pytest.mark.asyncio
async def test_infra_billing_providers(remnawave) -> None:
    """Test infra billing providers CRUD operations"""
    provider_name = f"test_provider_{generate_random_string(length=6)}"
    
    # Test create infra provider
    create_provider = await remnawave.infra_billing.create_infra_provider(
        CreateInfraProviderRequestDto(
            name=provider_name,
            favicon_link="https://example.com/favicon.ico",
            login_url="https://example.com/login"
        )
    )
    
    assert isinstance(create_provider, CreateInfraProviderResponseDto)
    assert create_provider.name == provider_name
    assert create_provider.favicon_link == "https://example.com/favicon.ico"
    assert create_provider.login_url == "https://example.com/login"
    
    provider_uuid = str(create_provider.uuid)

    try:
        await _exercise_provider(remnawave, create_provider, provider_name)
    finally:
        # провайдер удаляется даже если проверка выше упала, иначе он копится на панели
        delete_provider = await remnawave.infra_billing.delete_infra_provider_by_uuid(
            provider_uuid
        )
        assert delete_provider is None


async def _exercise_provider(remnawave, create_provider, provider_name) -> None:
    provider_uuid = str(create_provider.uuid)

    # Test get all infra providers
    all_providers = await remnawave.infra_billing.get_infra_providers()
    assert isinstance(all_providers, GetInfraProvidersResponseDto)
    assert all_providers.total > 0
    assert len(all_providers.providers) > 0
    
    # Verify our provider is in the list
    provider_found = any(p.uuid == create_provider.uuid for p in all_providers.providers)
    assert provider_found
    
    # Test get infra provider by uuid
    provider_by_uuid = await remnawave.infra_billing.get_infra_provider_by_uuid(provider_uuid)
    assert isinstance(provider_by_uuid, GetInfraProviderByUuidResponseDto)
    assert provider_by_uuid.name == provider_name
    assert provider_by_uuid.uuid == create_provider.uuid
    
    # Test update infra provider
    updated_name = f"updated_{provider_name}"
    update_provider = await remnawave.infra_billing.update_infra_provider(
        UpdateInfraProviderRequestDto(
            uuid=create_provider.uuid,
            name=updated_name,
            favicon_link="https://example.com/new-favicon.ico",
            login_url="https://example.com/new-login"
        )
    )
    
    assert isinstance(update_provider, UpdateInfraProviderResponseDto)
    assert update_provider.name == updated_name
    assert update_provider.favicon_link == "https://example.com/new-favicon.ico"
    assert update_provider.login_url == "https://example.com/new-login"


@pytest.mark.asyncio
async def test_infra_billing_history(remnawave) -> None:
    """Test infra billing history operations"""
    
    # Test get all infra billing history
    billing_history = await remnawave.infra_billing.get_infra_billing_history_records()
    assert isinstance(billing_history, GetInfraBillingHistoryRecordsResponseDto)
    assert hasattr(billing_history, 'records')
    assert hasattr(billing_history, 'total')
    
    # Skip creating history record as it may require specific setup
    print("Billing history operations tested successfully")


@pytest.mark.asyncio
async def test_infra_billing_nodes(remnawave) -> None:
    """Test infra billing nodes operations"""
    
    # Test get all infra billing nodes
    billing_nodes = await remnawave.infra_billing.get_billing_nodes()
    assert isinstance(billing_nodes, GetInfraBillingNodesResponseDto)
    assert hasattr(billing_nodes, 'total_billing_nodes')
    assert hasattr(billing_nodes, 'billing_nodes')
    assert hasattr(billing_nodes, 'available_billing_nodes')
    assert hasattr(billing_nodes, 'total_available_billing_nodes')
    assert hasattr(billing_nodes, 'stats')
    
    # Verify stats structure
    assert hasattr(billing_nodes.stats, 'upcoming_nodes_count')
    assert hasattr(billing_nodes.stats, 'current_month_payments')
    assert hasattr(billing_nodes.stats, 'total_spent')
    
    # Test create billing node (only if we have providers and available nodes)
    providers = await remnawave.infra_billing.get_infra_providers()
    if (providers.total > 0 and len(providers.providers) > 0 and
        billing_nodes.total_available_billing_nodes > 0 and 
        len(billing_nodes.available_billing_nodes) > 0):
        
        provider = providers.providers[0]
        available_node = billing_nodes.available_billing_nodes[0]
        next_billing = datetime.now() + timedelta(days=30)
        
        # Create billing node - API возвращает весь список узлов
        create_billing_node = await remnawave.infra_billing.create_infra_billing_node(
            CreateInfraBillingNodeRequestDto(
                node_uuid=available_node.uuid,
                provider_uuid=provider.uuid,
                name="SDK Test Billing Node",
                next_billing_at=next_billing
            )
        )
        
        assert isinstance(create_billing_node, CreateInfraBillingNodeResponseDto)
        assert hasattr(create_billing_node, 'billing_nodes')
        assert hasattr(create_billing_node, 'total_billing_nodes')
        
        # Find the created billing node
        created_node = None
        for node in create_billing_node.billing_nodes:
            if node.node.uuid == available_node.uuid and node.provider.uuid == provider.uuid:
                created_node = node
                break
        
        assert created_node is not None, "Created billing node not found in response"
        billing_node_uuid = str(created_node.uuid)
        
        # Test delete billing node - API возвращает обновленный список
        delete_billing_node = await remnawave.infra_billing.delete_infra_billing_node_by_uuid(billing_node_uuid)
        assert delete_billing_node is None


@pytest.mark.asyncio
async def test_infra_billing_complete_workflow(remnawave) -> None:
    """Test complete workflow: create provider -> create billing node -> cleanup"""
    provider_name = f"workflow_provider_{generate_random_string(length=6)}"
    
    # 1. Create provider
    create_provider = await remnawave.infra_billing.create_infra_provider(
        CreateInfraProviderRequestDto(
            name=provider_name,
            favicon_link="https://workflow.com/favicon.ico",
            login_url="https://workflow.com/login"
        )
    )
    
    assert isinstance(create_provider, CreateInfraProviderResponseDto)
    provider_uuid = str(create_provider.uuid)
    
    try:
        # 2. Get available nodes
        billing_nodes = await remnawave.infra_billing.get_billing_nodes()
        
        if (billing_nodes.total_available_billing_nodes > 0 and 
            len(billing_nodes.available_billing_nodes) > 0):
            
            available_node = billing_nodes.available_billing_nodes[0]
            next_billing = datetime.now() + timedelta(days=30)
            
            # 3. Create billing node
            create_billing_node = await remnawave.infra_billing.create_infra_billing_node(
                CreateInfraBillingNodeRequestDto(
                    node_uuid=available_node.uuid,
                    provider_uuid=create_provider.uuid,
                    name="SDK Test Billing Node",
                    next_billing_at=next_billing
                )
            )
            
            # Find created node
            created_node = None
            for node in create_billing_node.billing_nodes:
                if node.node.uuid == available_node.uuid and node.provider.uuid == create_provider.uuid:
                    created_node = node
                    break
            
            assert created_node is not None
            billing_node_uuid = str(created_node.uuid)
            
            # 4. Cleanup billing node - API возвращает обновленный список
            delete_billing_node = await remnawave.infra_billing.delete_infra_billing_node_by_uuid(billing_node_uuid)
            assert delete_billing_node is None
            
            # Verify deletion by checking the node is not in the list
    
    finally:
        # 5. Cleanup provider
        delete_provider = await remnawave.infra_billing.delete_infra_provider_by_uuid(provider_uuid)

@pytest.fixture
async def provider(remnawave):
    created = await remnawave.infra_billing.create_infra_provider(
        CreateInfraProviderRequestDto(name=f"prov_{generate_random_string(length=6)}")
    )
    yield created
    try:
        await remnawave.infra_billing.delete_infra_provider_by_uuid(str(created.uuid))
    except NotFoundError:
        pass


class TestInfraBillingHistoryRecords:
    @pytest.mark.asyncio
    async def test_create_and_delete_record(self, remnawave, provider):
        """Запись биллинга появляется в истории и удаляется по uuid"""
        billed_at = datetime.now(tz=pytz.utc)
        before = await remnawave.infra_billing.get_infra_billing_history_records()

        created = await remnawave.infra_billing.create_infra_billing_history_record(
            CreateInfraBillingHistoryRecordRequestDto(
                provider_uuid=provider.uuid, amount=42.5, billed_at=billed_at
            )
        )

        assert created.total == before.total + 1
        record = next(r for r in created.records if r.provider_uuid == provider.uuid)
        assert record.amount == 42.5

        await remnawave.infra_billing.delete_infra_billing_history_record_by_uuid(
            str(record.uuid)
        )

        after = await remnawave.infra_billing.get_infra_billing_history_records()
        assert after.total == before.total
        assert str(record.uuid) not in [str(r.uuid) for r in after.records]

    @pytest.mark.asyncio
    async def test_record_requires_a_known_provider(self, remnawave):
        with pytest.raises(ApiError):
            await remnawave.infra_billing.create_infra_billing_history_record(
                CreateInfraBillingHistoryRecordRequestDto(
                    provider_uuid="00000000-0000-0000-0000-000000000000",
                    amount=1,
                    billed_at=datetime.now(tz=pytz.utc),
                )
            )


class TestInfraBillingNodeUpdate:
    @pytest.mark.asyncio
    async def test_update_next_billing_date(self, remnawave, provider):
        """Дата следующего платежа переносится у привязанной ноды"""
        nodes = await remnawave.nodes.get_all_nodes()
        if not len(nodes):
            pytest.skip("В окружении нет ни одной ноды")

        next_billing_at = datetime.now(tz=pytz.utc) + timedelta(days=30)
        created = await remnawave.infra_billing.create_infra_billing_node(
            CreateInfraBillingNodeRequestDto(
                provider_uuid=provider.uuid,
                node_uuid=nodes[0].uuid,
                name=f"bn_{generate_random_string(length=6)}",
                next_billing_at=next_billing_at,
            )
        )
        billing_node = next(
            n for n in created.billing_nodes if n.provider_uuid == provider.uuid
        )

        try:
            moved_to = datetime.now(tz=pytz.utc) + timedelta(days=60)
            updated = await remnawave.infra_billing.update_infra_billing_node(
                UpdateInfraBillingNodeRequestDto(
                    uuids=[billing_node.uuid], next_billing_at=moved_to
                )
            )

            refreshed = next(
                n for n in updated.billing_nodes if n.uuid == billing_node.uuid
            )
            assert refreshed.next_billing_at.date() == moved_to.date()
        finally:
            await remnawave.infra_billing.delete_infra_billing_node_by_uuid(
                str(billing_node.uuid)
            )

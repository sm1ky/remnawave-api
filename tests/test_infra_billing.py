from datetime import datetime, timedelta

import pytest

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
    
    # Test delete infra provider
    delete_provider = await remnawave.infra_billing.delete_infra_provider_by_uuid(provider_uuid)
    assert isinstance(delete_provider, DeleteInfraProviderByUuidResponseDto)
    assert delete_provider.is_deleted is True


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
        assert isinstance(delete_billing_node, DeleteInfraBillingNodeByUuidResponseDto)
        assert hasattr(delete_billing_node, 'billing_nodes')
        assert hasattr(delete_billing_node, 'total_billing_nodes')
        
        # Verify the node was deleted (not in the response list)
        node_still_exists = any(
            node.uuid == created_node.uuid 
            for node in delete_billing_node.billing_nodes
        )
        assert not node_still_exists, "Billing node should be deleted but still found in response"


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
            assert isinstance(delete_billing_node, DeleteInfraBillingNodeByUuidResponseDto)
            
            # Verify deletion by checking the node is not in the list
            node_still_exists = any(
                node.uuid == created_node.uuid 
                for node in delete_billing_node.billing_nodes
            )
            assert not node_still_exists, "Billing node should be deleted"
    
    finally:
        # 5. Cleanup provider
        delete_provider = await remnawave.infra_billing.delete_infra_provider_by_uuid(provider_uuid)
        assert delete_provider.is_deleted is True
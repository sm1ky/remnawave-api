import pytest

from remnawave.models import (
    CloneSubscriptionPageConfigRequestDto,
    CloneSubscriptionPageConfigResponseDto,
    CreateSubscriptionPageConfigRequestDto,
    CreateSubscriptionPageConfigResponseDto,
    DeleteSubscriptionPageConfigResponseDto,
    GetSubscriptionPageConfigResponseDto,
    GetSubscriptionPageConfigsResponseDto,
    ReorderSubscriptionPageConfigItem,
    ReorderSubscriptionPageConfigsRequestDto,
    ReorderSubscriptionPageConfigsResponseDto,
    UpdateSubscriptionPageConfigRequestDto,
    UpdateSubscriptionPageConfigResponseDto,
)


def random_string(length=10):
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@pytest.mark.asyncio
async def test_get_all_configs(remnawave):
    """Test getting all subscription page configs"""
    configs = await remnawave.subscription_page_config.get_all_configs()
    assert isinstance(configs, GetSubscriptionPageConfigsResponseDto)
    assert configs.total >= 0
    assert isinstance(configs.configs, list)


@pytest.mark.asyncio
async def test_subscription_page_config_full_workflow(remnawave):
    """Test full workflow: create, get, update, reorder, clone, delete"""
    
    # Create config
    config_name = f"test_config_{random_string()}"
    create_request = CreateSubscriptionPageConfigRequestDto(name=config_name)
    created_config = await remnawave.subscription_page_config.create_config(create_request)
    assert isinstance(created_config, CreateSubscriptionPageConfigResponseDto)
    assert created_config.name == config_name
    
    config_uuid = str(created_config.uuid)
    
    # Get config by UUID
    config = await remnawave.subscription_page_config.get_config_by_uuid(config_uuid)
    assert isinstance(config, GetSubscriptionPageConfigResponseDto)
    assert config.name == config_name
    
    # Update config
    updated_name = f"updated_{config_name}"
    update_request = UpdateSubscriptionPageConfigRequestDto(
        uuid=created_config.uuid,
        name=updated_name,
        config=config.config
    )
    updated_config = await remnawave.subscription_page_config.update_config(update_request)
    assert isinstance(updated_config, UpdateSubscriptionPageConfigResponseDto)
    assert updated_config.name == updated_name
    
    # Clone config
    clone_request = CloneSubscriptionPageConfigRequestDto(
        clone_from_uuid=created_config.uuid
    )
    cloned_config = await remnawave.subscription_page_config.clone_config(clone_request)
    assert isinstance(cloned_config, CloneSubscriptionPageConfigResponseDto)
    
    # Reorder configs
    reorder_request = ReorderSubscriptionPageConfigsRequestDto(
        items=[
            ReorderSubscriptionPageConfigItem(
                uuid=created_config.uuid,
                view_position=1
            ),
            ReorderSubscriptionPageConfigItem(
                uuid=cloned_config.uuid,
                view_position=2
            )
        ]
    )
    reordered = await remnawave.subscription_page_config.reorder_configs(reorder_request)
    assert isinstance(reordered, ReorderSubscriptionPageConfigsResponseDto)
    
    # Delete cloned config
    delete_response = await remnawave.subscription_page_config.delete_config(
        str(cloned_config.uuid)
    )
    assert delete_response is None
    
    # Delete original config
    delete_response = await remnawave.subscription_page_config.delete_config(config_uuid)
    assert delete_response is None
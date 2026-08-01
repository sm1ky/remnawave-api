import pytest

from remnawave.enums import ClientType
from remnawave.exceptions.general import ApiError
from remnawave.models import (
    GetSubscriptionInfoResponseDto,
    GetRawSubscriptionByShortUuidResponseDto,
    GetAllSubscriptionsResponseDto,
    GetSubscriptionByUsernameResponseDto,
    GetSubpageConfigByShortUuidRequestBodyDto,
    GetSubpageConfigByShortUuidResponseDto,
    SubpageConfigData,
)
from tests.conftest import REMNAWAVE_SHORT_UUID, REMNAWAVE_USER_USERNAME


class TestSubscriptionInfo:
    """Тесты для получения информации о подписках"""
    
    @pytest.mark.asyncio
    async def test_get_subscription_info_by_short_uuid(self, remnawave):
        """Тест получения информации о подписке по короткому UUID"""
        subscription_info = await remnawave.subscription.get_subscription_info_by_short_uuid(
            short_uuid=REMNAWAVE_SHORT_UUID
        )
        assert isinstance(subscription_info, GetSubscriptionInfoResponseDto)
        assert subscription_info.is_found is True
        assert hasattr(subscription_info, 'user')
    
    @pytest.mark.asyncio
    async def test_get_raw_subscription_by_short_uuid(self, remnawave):
        """Тест получения сырой подписки по короткому UUID"""

        raw_subscription = await remnawave.subscriptions.get_raw_subscription(
            short_uuid=REMNAWAVE_SHORT_UUID
        )
        assert isinstance(raw_subscription, GetRawSubscriptionByShortUuidResponseDto)

class TestSubscriptionContent:
    """Тесты для получения контента подписок"""
    
    @pytest.mark.asyncio
    async def test_get_subscription(self, remnawave):
        """Тест получения подписки по короткому UUID"""
        subscription = await remnawave.subscription.get_subscription(
            short_uuid=REMNAWAVE_SHORT_UUID
        )
        assert isinstance(subscription, str)


class TestSubscriptionsManagement:
    """Тесты для управления подписками"""
    
    @pytest.mark.asyncio
    async def test_get_all_subscriptions(self, remnawave):
        """Тест получения всех подписок"""
        all_subscriptions = await remnawave.subscriptions.get_all_subscriptions()
        assert isinstance(all_subscriptions, GetAllSubscriptionsResponseDto)
        assert hasattr(all_subscriptions, 'subscriptions')
        assert hasattr(all_subscriptions, 'total')

    @pytest.mark.asyncio
    async def test_get_subscription_by_username(self, remnawave):
        """Тест получения подписки по имени пользователя"""
        subscription_by_username = await remnawave.subscriptions.get_subscription_by_username(
            username=REMNAWAVE_USER_USERNAME
        )
        assert isinstance(subscription_by_username, GetSubscriptionByUsernameResponseDto)

    @pytest.mark.asyncio
    async def test_get_subpage_config(self, remnawave):
        """Тест получения конфига страницы подписки по short UUID"""
        body = GetSubpageConfigByShortUuidRequestBodyDto(request_headers={})
        subpage_config = await remnawave.subscriptions.get_subpage_config(
            short_uuid=REMNAWAVE_SHORT_UUID,
            body=body,
        )
        # Client auto-unwraps single "response" field → returns SubpageConfigData
        assert isinstance(subpage_config, (GetSubpageConfigByShortUuidResponseDto, SubpageConfigData))
        assert hasattr(subpage_config, 'webpage_allowed')
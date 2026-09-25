"""Tests for the protected Subscriptions controller."""
import pytest

from remnawave.enums import ClientType
from remnawave.exceptions import ApiError
from remnawave.models import (
    GetAllSubscriptionsResponseDto,
    GetConnectionKeysByUuidResponseDto,
    GetSubscriptionByShortUUIDResponseDto,
    GetSubscriptionByUUIDResponseDto,
)


@pytest.fixture
async def some_user(remnawave):
    users = await remnawave.users.get_all_users(size=1)
    if not users.users:
        pytest.skip("В окружении нет ни одного пользователя")
    return users.users[0]


class TestSubscriptionLookup:
    @pytest.mark.asyncio
    async def test_get_all_subscriptions(self, remnawave):
        response = await remnawave.subscriptions.get_all_subscriptions(start=0, size=5)

        assert isinstance(response, GetAllSubscriptionsResponseDto)
        assert response.total >= len(response.subscriptions)
        assert len(response.subscriptions) <= 5

    @pytest.mark.asyncio
    async def test_get_subscription_by_id(self, remnawave, some_user):
        response = await remnawave.subscriptions.get_subscription_by_id(
            user_id=some_user.id
        )

        assert isinstance(response, GetSubscriptionByUUIDResponseDto)
        assert response.is_found is True
        # объект подписки описывает пользователя через short_uuid/username, без id
        assert response.user.short_uuid == some_user.short_uuid
        assert response.user.username == some_user.username
        assert response.subscription_url

    @pytest.mark.asyncio
    async def test_get_subscription_by_short_uuid(self, remnawave, some_user):
        response = await remnawave.subscriptions.get_subscription_by_short_uuid(
            short_uuid=some_user.short_uuid
        )

        assert isinstance(response, GetSubscriptionByShortUUIDResponseDto)
        assert response.is_found is True
        assert response.user.short_uuid == some_user.short_uuid

    @pytest.mark.asyncio
    async def test_both_lookups_agree(self, remnawave, some_user):
        """by-id и by-short-uuid описывают одного и того же пользователя"""
        by_id = await remnawave.subscriptions.get_subscription_by_id(user_id=some_user.id)
        by_short = await remnawave.subscriptions.get_subscription_by_short_uuid(
            short_uuid=some_user.short_uuid
        )

        assert by_id.user.username == by_short.user.username
        assert by_id.subscription_url == by_short.subscription_url

    @pytest.mark.asyncio
    async def test_unknown_short_uuid(self, remnawave):
        """Несуществующая подписка не выдаётся за найденную"""
        try:
            response = await remnawave.subscriptions.get_subscription_by_short_uuid(
                short_uuid="sdkMissingShortUu"
            )
        except ApiError:
            return  # панель вправе ответить ошибкой вместо isFound=false
        assert response.is_found is False


class TestConnectionKeys:
    @pytest.mark.asyncio
    async def test_get_connection_keys(self, remnawave, some_user):
        response = await remnawave.subscriptions.get_connection_keys_by_user_id(
            user_id=some_user.id
        )

        assert isinstance(response, GetConnectionKeysByUuidResponseDto)
        for bucket in (response.enabled_keys, response.hidden_keys, response.disabled_keys):
            assert isinstance(bucket, list)


class TestSubscriptionByClientType:
    @pytest.mark.parametrize(
        "client_type",
        [ClientType.V2RAY_JSON, ClientType.CLASH, ClientType.SINGBOX, ClientType.STASH],
    )
    @pytest.mark.asyncio
    async def test_returns_a_config(self, remnawave, some_user, client_type):
        """Публичная выдача подписки отдаёт непустой конфиг под каждый тип клиента"""
        body = await remnawave.subscription.get_subscription_by_client_type(
            short_uuid=some_user.short_uuid, client_type=client_type
        )

        assert isinstance(body, str)
        assert body.strip()

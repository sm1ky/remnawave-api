import random
from datetime import datetime, timedelta

import pytest
import pytz

from remnawave.enums import ErrorCode, UserStatus
from remnawave.exceptions import ApiError
from remnawave.models import (
    CreateUserBodyDto,
    ExtendUserBodyDto,
    GetUserAccessibleNodesResponseDto,
    UpdateUserBodyDto,
    UserResponseDto,
    UsersResponseDto,
    TagsResponseDto,
)
from remnawave.models.users import GetUserSubscriptionRequestHistoryResponseDto
from tests.utils import generate_email, generate_random_string


class TestUsersCRUD:
    """Базовые CRUD операции для пользователей (Remnawave API v3.0.0 — по числовому id)."""

    @pytest.mark.asyncio
    async def test_create_user(self, remnawave):
        email = generate_email(length=8)
        username = generate_random_string(length=8)
        telegram_id = random.randint(100000000, 999999999)
        expire_at = datetime.now(tz=pytz.UTC) + timedelta(days=7)

        create_user = await remnawave.users.create_user(
            CreateUserBodyDto(
                username=username,
                email=email,
                telegram_id=telegram_id,
                expire_at=expire_at,
            )
        )

        assert isinstance(create_user, UserResponseDto)
        assert isinstance(create_user.id, int)
        assert create_user.username == username
        assert create_user.email == email
        assert create_user.telegram_id == telegram_id
        assert create_user.expire_at.isoformat(timespec="seconds") == expire_at.isoformat(
            timespec="seconds"
        )

        # Clean up
        await remnawave.users.delete_user(user_id=create_user.id)

    @pytest.mark.asyncio
    async def test_update_user(self, remnawave):
        username = generate_random_string(length=8)
        expire_at = datetime.now(tz=pytz.UTC) + timedelta(days=7)

        create_user = await remnawave.users.create_user(
            CreateUserBodyDto(username=username, expire_at=expire_at)
        )

        # Update by numeric id
        update_description = "TEST"
        update_status = UserStatus.DISABLED
        update_user = await remnawave.users.update_user(
            UpdateUserBodyDto(
                id=create_user.id, status=update_status, description=update_description
            )
        )
        assert isinstance(update_user, UserResponseDto)
        assert update_user.id == create_user.id
        assert update_user.status == update_status
        assert update_user.description == update_description

        # Clean up
        await remnawave.users.delete_user(user_id=create_user.id)

    @pytest.mark.asyncio
    async def test_delete_user(self, remnawave):
        username = generate_random_string(length=8)
        expire_at = datetime.now(tz=pytz.UTC) + timedelta(days=7)

        create_user = await remnawave.users.create_user(
            CreateUserBodyDto(username=username, expire_at=expire_at)
        )

        # DELETE now returns 204 No Content -> None
        result = await remnawave.users.delete_user(user_id=create_user.id)
        assert result is None


class TestUsersFetch:
    """Получение информации о пользователях."""

    @pytest.mark.asyncio
    async def test_get_all_users(self, remnawave):
        all_users = await remnawave.users.get_all_users()
        assert isinstance(all_users, UsersResponseDto)

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, remnawave):
        # v3.0.0: пользователь запрашивается по числовому id (панельный user id=1)
        user = await remnawave.users.get_user_by_id(user_id=1)
        assert isinstance(user, UserResponseDto)
        assert user.id == 1

    @pytest.mark.asyncio
    async def test_get_user_by_short_uuid(self, remnawave, test_user):
        user = await remnawave.users.get_user_by_short_uuid(short_uuid=test_user.short_uuid)
        assert isinstance(user, UserResponseDto)
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_user_by_username(self, remnawave, test_user):
        user = await remnawave.users.get_user_by_username(username=test_user.username)
        assert isinstance(user, UserResponseDto)
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_get_all_tags(self, remnawave):
        users_tags = await remnawave.users.get_all_tags()
        assert isinstance(users_tags, TagsResponseDto)

    @pytest.mark.asyncio
    async def test_get_user_accessible_nodes(self, remnawave, test_user):
        try:
            nodes = await remnawave.users.get_user_accessible_nodes(user_id=test_user.id)
            assert isinstance(nodes, GetUserAccessibleNodesResponseDto)
            assert isinstance(nodes.active_nodes, list)
        except ApiError as e:
            assert e.error.code in [ErrorCode.USER_NOT_FOUND]

    @pytest.mark.asyncio
    async def test_get_subscription_requests(self, remnawave, test_user):
        """Test fetching user subscription request history."""
        try:
            history = await remnawave.users.get_user_subscription_request_history(
                user_id=test_user.id
            )
            assert isinstance(history, GetUserSubscriptionRequestHistoryResponseDto)
            assert hasattr(history, "total")
            assert hasattr(history, "records")
        except ApiError as e:
            assert e.error.code in [ErrorCode.USER_NOT_FOUND]


class TestUserActions:
    """Действия над пользователями."""

    @pytest.mark.asyncio
    async def test_reset_user_traffic(self, remnawave, test_user):
        user = await remnawave.users.reset_user_traffic(user_id=test_user.id)
        assert isinstance(user, UserResponseDto)
        assert user.id == test_user.id
        assert user.used_traffic_bytes == 0

    @pytest.mark.asyncio
    async def test_disable_enable_user(self, remnawave, test_user):
        try:
            disable_user = await remnawave.users.disable_user(user_id=test_user.id)
            assert isinstance(disable_user, UserResponseDto)
            assert disable_user.id == test_user.id
            assert disable_user.status == UserStatus.DISABLED
        except ApiError as e:
            assert e.error.code == ErrorCode.USER_ALREADY_DISABLED

        try:
            enable_user = await remnawave.users.enable_user(user_id=test_user.id)
            assert isinstance(enable_user, UserResponseDto)
            assert enable_user.id == test_user.id
            assert enable_user.status == UserStatus.ACTIVE
        except ApiError as e:
            assert e.error.code == ErrorCode.USER_ALREADY_ENABLED

    @pytest.mark.asyncio
    async def test_extend_user(self, remnawave, test_user):
        # v3.0.0: новый эндпоинт продления срока
        user = await remnawave.users.extend_user(
            user_id=test_user.id, body=ExtendUserBodyDto(days=7)
        )
        assert isinstance(user, UserResponseDto)
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_revoke_user_subscription(self, remnawave, test_user):
        old_short_uuid = test_user.short_uuid
        revoke = await remnawave.users.revoke_user_subscription(user_id=test_user.id)
        assert isinstance(revoke, UserResponseDto)
        assert revoke.id == test_user.id
        assert revoke.short_uuid != old_short_uuid


@pytest.fixture
async def test_user(remnawave):
    """Fixture: create a test user (cleaned up by numeric id)."""
    username = generate_random_string(length=8)
    expire_at = datetime.now(tz=pytz.UTC) + timedelta(days=7)

    user = await remnawave.users.create_user(
        CreateUserBodyDto(username=username, expire_at=expire_at)
    )

    yield user

    await remnawave.users.delete_user(user_id=user.id)

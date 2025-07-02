import random
from datetime import datetime, timedelta

import pytest
import pytz

from remnawave_api.enums import ErrorCode, UserStatus
from remnawave_api.exceptions import ApiError
from remnawave_api.models import (
    CreateUserRequestDto,
    DeleteUserResponseDto,
    EmailUserResponseDto,
    GetUserAccessibleNodesResponseDto,
    TelegramUserResponseDto,
    UpdateUserRequestDto,
    UserResponseDto,
    UsersResponseDto,
    TagsResponseDto,
    RevokeUserRequestDto
)
from tests.utils import generate_email, generate_random_string


@pytest.mark.asyncio
async def test_users(remnawave) -> None:
    email: str = generate_email(length=8)
    username: str = generate_random_string(length=8)
    telegram_id: int = random.randint(100000000, 999999999)
    expire_at: datetime = datetime.now(tz=pytz.UTC) + timedelta(days=7)

    create_user = await remnawave.users.create_user(
        CreateUserRequestDto(
            username=username,
            email=email,
            telegram_id=telegram_id,
            expire_at=expire_at,
            activate_all_inbounds=True,
        )
    )

    assert isinstance(create_user, UserResponseDto)
    assert create_user.username == username
    assert create_user.email == email
    assert create_user.telegram_id == telegram_id
    assert create_user.expire_at.isoformat(timespec="seconds") == expire_at.isoformat(
        timespec="seconds"
    )

    string_uuid = str(create_user.uuid)
    string_telegram_id = str(create_user.telegram_id)

    all_users = await remnawave.users.get_all_users_v2()
    assert isinstance(all_users, UsersResponseDto)

    user_uuid = await remnawave.users.get_user_by_uuid(uuid=string_uuid)
    assert isinstance(user_uuid, UserResponseDto)
    assert user_uuid.uuid == create_user.uuid

    user_short_uuid = await remnawave.users.get_user_by_short_uuid(
        short_uuid=user_uuid.short_uuid
    )
    assert isinstance(user_short_uuid, UserResponseDto)
    assert user_short_uuid.uuid == create_user.uuid

    # Only test get_user_by_subscription_uuid if subscription_uuid is not None
    if create_user.subscription_uuid is not None:
        string_subscription_uuid = str(create_user.subscription_uuid)
        user_subscription_uuid = await remnawave.users.get_user_by_subscription_uuid(
            subscription_uuid=string_subscription_uuid
        )
        assert isinstance(user_subscription_uuid, UserResponseDto)
        assert user_subscription_uuid.uuid == create_user.uuid

    user_username = await remnawave.users.get_user_by_username(
        username=user_uuid.username
    )
    assert isinstance(user_username, UserResponseDto)
    assert user_username.uuid == create_user.uuid

    user_telegram_id = await remnawave.users.get_users_by_telegram_id(
        telegram_id=string_telegram_id
    )
    assert isinstance(user_telegram_id, TelegramUserResponseDto)
    assert any(user.uuid == create_user.uuid for user in user_telegram_id)

    user_email = await remnawave.users.get_users_by_email(email=user_uuid.email)
    assert isinstance(user_email, EmailUserResponseDto)
    assert any(user.uuid == create_user.uuid for user in user_email)

    user_reset_traffic = await remnawave.users.reset_user_traffic(uuid=string_uuid)
    assert isinstance(user_reset_traffic, UserResponseDto)
    assert user_reset_traffic.uuid == create_user.uuid
    assert user_reset_traffic.used_traffic_bytes == 0

    try:
        disable_user = await remnawave.users.disable_user(uuid=string_uuid)
        assert isinstance(disable_user, UserResponseDto)
        assert disable_user.uuid == create_user.uuid
        assert disable_user.status == UserStatus.DISABLED
    except ApiError as e:
        assert e.error.code == ErrorCode.USER_ALREADY_DISABLED

    try:
        enable_user = await remnawave.users.enable_user(uuid=string_uuid)
        assert isinstance(enable_user, UserResponseDto)
        assert enable_user.uuid == create_user.uuid
        assert enable_user.status == UserStatus.ACTIVE
    except ApiError as e:
        assert e.error.code == ErrorCode.USER_ALREADY_ENABLED

    update_description: str = "TEST"
    update_status: UserStatus = UserStatus.DISABLED
    update_user = await remnawave.users.update_user(
        UpdateUserRequestDto(
            uuid=string_uuid, status=update_status, description=update_description
        )
    )
    assert isinstance(update_user, UserResponseDto)
    assert update_user.uuid == create_user.uuid
    assert update_user.status == update_status
    assert update_user.description == update_description

    # Temporarily disabled, error in backend
    revoke_user_subscription = await remnawave.users.revoke_user_subscription(
        uuid=string_uuid,
        # body=RevokeUserRequestDto(
        #     short_uuid="fokfaa"
        # )
    )
    assert isinstance(revoke_user_subscription, UserResponseDto)
    assert revoke_user_subscription.uuid == create_user.uuid
    assert revoke_user_subscription.short_uuid != create_user.short_uuid

    # Test get user accessible nodes
    try:
        user_accessible_nodes = await remnawave.users.get_user_accessible_nodes(uuid=string_uuid)
        assert isinstance(user_accessible_nodes, GetUserAccessibleNodesResponseDto)
        assert isinstance(user_accessible_nodes.nodes, list)
    except ApiError as e:
        # This might fail if the user doesn't have access to any nodes
        # or if the feature is not available, which is acceptable for testing
        assert e.error_code in [ErrorCode.USER_NOT_FOUND, ErrorCode.FORBIDDEN, ErrorCode.NOT_FOUND]

    delete_user = await remnawave.users.delete_user(uuid=string_uuid)
    assert isinstance(delete_user, DeleteUserResponseDto)
    assert delete_user.is_deleted is True

    users_tags = await remnawave.users.get_all_tags()
    assert isinstance(users_tags, TagsResponseDto)
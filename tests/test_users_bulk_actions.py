from datetime import datetime, timedelta

import pytest
import pytz

from remnawave.controllers.users_bulk_actions import UsersBulkActionsController
from remnawave.exceptions import NotFoundError
from remnawave.models import (
    BulkDeleteUsersRequestDto,
    BulkExtendExpirationDateRequestDto,
    BulkResetTrafficUsersRequestDto,
    BulkRevokeUsersSubscriptionRequestDto,
    BulkUpdateUsersRequestDto,
    BulkUpdateUsersSquadsRequestDto,
    CreateInternalSquadRequestDto,
    CreateUserBodyDto,
    UpdateUserFields,
)
from tests.conftest import REMNAWAVE_INBOUND_UUID
from tests.utils import generate_random_string


@pytest.mark.asyncio
async def test_users_bulk_actions(remnawave):
    expire_at = datetime.now(tz=pytz.utc) + timedelta(days=14)
    description = "TEST_DESCRIPTION"

    # v3.0.0: users are addressed by numeric id (userIds); bulk operations run in
    # the background and return 202 Accepted with no body -> None.
    result = await remnawave.users_bulk_actions.bulk_update_users(
        body=BulkUpdateUsersRequestDto(
            user_ids=[1],
            fields=UpdateUserFields(
                expire_at=expire_at,
                description=description,
            ),
        ),
    )
    assert result is None


@pytest.fixture
async def bulk_users(remnawave):
    """Три собственных пользователя; массовые операции идут только по их id"""
    expire_at = datetime.now(tz=pytz.utc) + timedelta(days=7)
    created = [
        await remnawave.users.create_user(
            CreateUserBodyDto(
                username=f"bulk_{generate_random_string(length=10)}", expire_at=expire_at
            )
        )
        for _ in range(3)
    ]
    yield created
    for user in created:
        try:
            await remnawave.users.delete_user(user_id=user.id)
        except NotFoundError:
            pass


class TestScopedBulkActions:
    """Операции, ограниченные списком userIds"""

    @pytest.mark.asyncio
    async def test_bulk_extend_expiration_date(self, remnawave, bulk_users):
        before = {u.id: u.expire_at for u in bulk_users}

        await remnawave.users_bulk_actions.bulk_extend_expiration_date(
            BulkExtendExpirationDateRequestDto(
                user_ids=[u.id for u in bulk_users], extend_days=5
            )
        )

        for user in bulk_users:
            fetched = await remnawave.users.get_user_by_id(user_id=user.id)
            assert fetched.expire_at > before[user.id]

    @pytest.mark.asyncio
    async def test_bulk_update_users(self, remnawave, bulk_users):
        description = f"bulk_{generate_random_string(length=8)}"

        await remnawave.users_bulk_actions.bulk_update_users(
            BulkUpdateUsersRequestDto(
                user_ids=[u.id for u in bulk_users],
                fields=UpdateUserFields(description=description),
            )
        )

        for user in bulk_users:
            fetched = await remnawave.users.get_user_by_id(user_id=user.id)
            assert fetched.description == description

    @pytest.mark.asyncio
    async def test_bulk_revoke_subscription(self, remnawave, bulk_users):
        """Отзыв подписки меняет short_uuid каждому перечисленному пользователю"""
        before = {u.id: u.short_uuid for u in bulk_users}

        await remnawave.users_bulk_actions.bulk_revoke_users_subscription(
            BulkRevokeUsersSubscriptionRequestDto(user_ids=[u.id for u in bulk_users])
        )

        for user in bulk_users:
            fetched = await remnawave.users.get_user_by_id(user_id=user.id)
            assert fetched.short_uuid != before[user.id]

    @pytest.mark.asyncio
    async def test_bulk_reset_traffic(self, remnawave, bulk_users):
        response = await remnawave.users_bulk_actions.bulk_reset_user_traffic(
            BulkResetTrafficUsersRequestDto(user_ids=[u.id for u in bulk_users])
        )

        assert response is None
        for user in bulk_users:
            fetched = await remnawave.users.get_user_by_id(user_id=user.id)
            assert fetched.user_traffic.used_traffic_bytes == 0

    @pytest.mark.asyncio
    async def test_bulk_update_internal_squads(self, remnawave, bulk_users):
        """Список сквадов проставляется всем перечисленным пользователям"""
        squad = await remnawave.internal_squads.create_internal_squad(
            CreateInternalSquadRequestDto(
                name=f"bulk_{generate_random_string(length=6)}",
                inbounds=[REMNAWAVE_INBOUND_UUID],
            )
        )
        try:
            await remnawave.users_bulk_actions.bulk_update_users_internal_squads(
                BulkUpdateUsersSquadsRequestDto(
                    user_ids=[u.id for u in bulk_users],
                    active_internal_squads=[squad.uuid],
                )
            )

            for user in bulk_users:
                fetched = await remnawave.users.get_user_by_id(user_id=user.id)
                assert squad.uuid in [s.uuid for s in fetched.active_internal_squads]
        finally:
            await remnawave.internal_squads.delete_internal_squad(str(squad.uuid))

    @pytest.mark.asyncio
    async def test_bulk_delete_users(self, remnawave):
        """Массовое удаление убирает ровно перечисленных пользователей"""
        expire_at = datetime.now(tz=pytz.utc) + timedelta(days=7)
        created = [
            await remnawave.users.create_user(
                CreateUserBodyDto(
                    username=f"bulk_{generate_random_string(length=10)}", expire_at=expire_at
                )
            )
            for _ in range(2)
        ]

        await remnawave.users_bulk_actions.bulk_delete_users(
            BulkDeleteUsersRequestDto(user_ids=[u.id for u in created])
        )

        for user in created:
            with pytest.raises(NotFoundError):
                await remnawave.users.get_user_by_id(user_id=user.id)


class TestPanelWideBulkActions:
    """Операции без списка id затрагивают всех пользователей панели и здесь не выполняются"""

    @pytest.mark.parametrize(
        "action",
        [
            "bulk_all_update_users",
            "bulk_all_reset_user_traffic",
            "bulk_all_extend_expiration_date",
            "bulk_delete_users_by_status",
        ],
    )
    def test_is_available_but_not_exercised(self, action):
        method = {
            "bulk_all_update_users": "bulk_update_all_users",
            "bulk_all_reset_user_traffic": "bulk_all_reset_user_traffic",
            "bulk_all_extend_expiration_date": "bulk_all_extend_expiration_date",
            "bulk_delete_users_by_status": "bulk_delete_users_by_status",
        }[action]
        assert callable(getattr(UsersBulkActionsController, method))
        pytest.skip(
            f"{method} изменяет всех пользователей панели — не запускается автоматически"
        )

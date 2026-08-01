from datetime import datetime, timedelta

import pytest
import pytz

from remnawave.models import UpdateUserFields, BulkUpdateUsersRequestDto


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

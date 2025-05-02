from typing import Annotated

from rapid_api_client import Path, Query

from remnawave_api.models import UserUsageByRangeResponseDto
from remnawave_api.rapid import BaseController, get


class UsersStatsController(BaseController):
    @get(
        "/users/stats/usage/{uuid}/range",
        response_class=UserUsageByRangeResponseDto,
    )
    async def get_user_usage_by_range(
        self,
        uuid: Annotated[str, Path(description="UUID of the user")],
        start: Annotated[str, Query(description="Start date in ISO format")],
        end: Annotated[str, Query(description="End date in ISO format")],
    ) -> UserUsageByRangeResponseDto:
        """Get User Usage By Range"""
        ...

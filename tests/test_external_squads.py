"""Tests for the External Squads controller."""
import pytest

from remnawave.controllers.external_squads import ExternalSquadsController
from remnawave.exceptions import ApiError, NotFoundError
from remnawave.models import (
    CreateExternalSquadRequestDto,
    ExternalSquadHostOverridesDto,
    GetExternalSquadByUuidResponseDto,
    GetExternalSquadsResponseDto,
    ReorderExternalSquadItem,
    ReorderExternalSquadsRequestDto,
    ReorderExternalSquadsResponseDto,
    UpdateExternalSquadRequestDto,
    UpdateExternalSquadResponseDto,
)
from tests.utils import generate_random_string


@pytest.fixture
async def squad(remnawave):
    created = await remnawave.external_squads.create_external_squad(
        CreateExternalSquadRequestDto(name=f"ext_{generate_random_string(length=6)}")
    )
    yield created
    try:
        await remnawave.external_squads.delete_external_squad(str(created.uuid))
    except NotFoundError:
        pass


class TestExternalSquadsListing:
    @pytest.mark.asyncio
    async def test_get_external_squads(self, remnawave, squad):
        response = await remnawave.external_squads.get_external_squads()

        assert isinstance(response, GetExternalSquadsResponseDto)
        assert response.total == len(response.external_squads)
        assert squad.uuid in [s.uuid for s in response.external_squads]

    @pytest.mark.asyncio
    async def test_get_by_uuid_matches_the_listing(self, remnawave, squad):
        fetched = await remnawave.external_squads.get_external_squad_by_uuid(str(squad.uuid))

        assert isinstance(fetched, GetExternalSquadByUuidResponseDto)
        assert fetched.name == squad.name
        assert fetched.info.members_count == 0

    @pytest.mark.asyncio
    async def test_unknown_uuid(self, remnawave):
        with pytest.raises(ApiError):
            await remnawave.external_squads.get_external_squad_by_uuid(
                "00000000-0000-0000-0000-000000000000"
            )


class TestExternalSquadUpdate:
    @pytest.mark.asyncio
    async def test_rename(self, remnawave, squad):
        new_name = f"ext_{generate_random_string(length=6)}"

        updated = await remnawave.external_squads.update_external_squad(
            UpdateExternalSquadRequestDto(uuid=squad.uuid, name=new_name)
        )

        assert isinstance(updated, UpdateExternalSquadResponseDto)
        assert updated.name == new_name
        assert (
            await remnawave.external_squads.get_external_squad_by_uuid(str(squad.uuid))
        ).name == new_name

    @pytest.mark.asyncio
    async def test_host_overrides_round_trip(self, remnawave, squad):
        """Вложенный объект настроек сохраняется и читается обратно"""
        await remnawave.external_squads.update_external_squad(
            UpdateExternalSquadRequestDto(
                uuid=squad.uuid,
                host_overrides=ExternalSquadHostOverridesDto(
                    server_description="sdk test", vless_route_id=7
                ),
            )
        )

        fetched = await remnawave.external_squads.get_external_squad_by_uuid(str(squad.uuid))
        assert fetched.host_overrides is not None
        assert fetched.host_overrides.server_description == "sdk test"
        assert fetched.host_overrides.vless_route_id == 7


class TestExternalSquadsReorder:
    @pytest.mark.asyncio
    async def test_reorder(self, remnawave, squad):
        listing = await remnawave.external_squads.get_external_squads()
        items = [
            ReorderExternalSquadItem(view_position=index, uuid=s.uuid)
            for index, s in enumerate(reversed(listing.external_squads))
        ]

        response = await remnawave.external_squads.reorder_external_squads(
            ReorderExternalSquadsRequestDto(items=items)
        )

        assert isinstance(response, ReorderExternalSquadsResponseDto)
        positions = {
            s.uuid: s.view_position
            for s in (await remnawave.external_squads.get_external_squads()).external_squads
        }
        for item in items:
            assert positions[item.uuid] == item.view_position


class TestPanelWideMembership:
    """add-users / remove-users работают по всем пользователям панели сразу"""

    @pytest.mark.parametrize(
        "method", ["add_users_to_external_squad", "remove_users_from_external_squad"]
    )
    def test_is_available_but_not_exercised(self, method):
        assert callable(getattr(ExternalSquadsController, method))
        pytest.skip(
            f"{method} перемещает всех пользователей панели — не запускается автоматически"
        )

"""Tests for bulk host operations, scoped to hosts the suite creates itself."""
import random

import pytest

from remnawave.exceptions import NotFoundError
from remnawave.models import CreateHostRequestDto, UpdateManyHostsRequestDto
from tests.conftest import REMNAWAVE_CONFIG_PROFILE_UUID, REMNAWAVE_INBOUND_UUID
from tests.utils import generate_random_string


@pytest.fixture
async def hosts(remnawave):
    """Пара собственных хостов; массовые операции идут только по их uuid"""
    created = []
    for _ in range(2):
        created.append(
            await remnawave.hosts.create_host(
                CreateHostRequestDto(
                    inbound_uuid=REMNAWAVE_INBOUND_UUID,
                    config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                    remark=generate_random_string(),
                    address=f"{random.randint(500, 800)}.0.0.1",
                    port=random.randint(5000, 8000),
                )
            )
        )
    yield created
    for host in created:
        try:
            await remnawave.hosts.delete_host(uuid=str(host.uuid))
        except NotFoundError:
            pass


async def _states(remnawave, uuids):
    all_hosts = await remnawave.hosts.get_all_hosts()
    return {h.uuid: h.is_disabled for h in all_hosts if h.uuid in uuids}


class TestHostsBulkActions:
    @pytest.mark.asyncio
    async def test_disable_then_enable(self, remnawave, hosts):
        uuids = [h.uuid for h in hosts]
        assert all(v is False for v in (await _states(remnawave, set(uuids))).values())

        await remnawave.hosts_bulk_actions.disable_hosts(uuids=uuids)
        assert all(v is True for v in (await _states(remnawave, set(uuids))).values())

        await remnawave.hosts_bulk_actions.enable_hosts(uuids=uuids)
        assert all(v is False for v in (await _states(remnawave, set(uuids))).values())

    @pytest.mark.asyncio
    async def test_other_hosts_are_untouched(self, remnawave, hosts):
        """Массовое отключение не задевает хосты, которых нет в списке"""
        uuids = {h.uuid for h in hosts}
        before = {h.uuid: h.is_disabled for h in await remnawave.hosts.get_all_hosts() if h.uuid not in uuids}

        await remnawave.hosts_bulk_actions.disable_hosts(uuids=list(uuids))
        try:
            after = {h.uuid: h.is_disabled for h in await remnawave.hosts.get_all_hosts() if h.uuid not in uuids}
            assert after == before
        finally:
            await remnawave.hosts_bulk_actions.enable_hosts(uuids=list(uuids))

    @pytest.mark.asyncio
    async def test_update_many_hosts(self, remnawave, hosts):
        """Общее поле проставляется сразу всем перечисленным хостам"""
        uuids = [h.uuid for h in hosts]
        description = generate_random_string(length=12)

        await remnawave.hosts_bulk_actions.update_hosts(
            UpdateManyHostsRequestDto(uuids=uuids, server_description=description)
        )

        for uuid in uuids:
            fetched = await remnawave.hosts.get_one_host(uuid=str(uuid))
            assert fetched.server_description == description

    @pytest.mark.asyncio
    async def test_delete_many_hosts(self, remnawave):
        """Массовое удаление убирает ровно перечисленные хосты"""
        created = []
        for _ in range(2):
            created.append(
                await remnawave.hosts.create_host(
                    CreateHostRequestDto(
                        inbound_uuid=REMNAWAVE_INBOUND_UUID,
                        config_profile_inbound_uuid=REMNAWAVE_CONFIG_PROFILE_UUID,
                        remark=generate_random_string(),
                        address=f"{random.randint(500, 800)}.0.0.1",
                        port=random.randint(5000, 8000),
                    )
                )
            )
        uuids = [h.uuid for h in created]

        await remnawave.hosts_bulk_actions.delete_hosts(uuids=uuids)

        remaining = {h.uuid for h in await remnawave.hosts.get_all_hosts()}
        assert not (set(uuids) & remaining)

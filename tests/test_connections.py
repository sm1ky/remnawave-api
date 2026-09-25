"""Tests for the Connections controller, including geocheck (Remnawave API v3.4.0+)."""
import asyncio

import pytest

from remnawave.exceptions import ApiError, NotFoundError
from remnawave.models import (
    DropByIpAddresses,
    DropByUserUuids,
    DropConnectionsRequestDto,
    FetchIpsResponseDto,
    FetchIpsResultResponseDto,
    FetchUsersIpsResponseDto,
    FetchUsersIpsResultResponseDto,
    GeocheckByNodeRequestDto,
    GeocheckByNodeResponseDto,
    GeocheckByNodeResultResponseDto,
    GeocheckImageDto,
    GeocheckResult,
    TargetAllNodes,
    TargetSpecificNodes,
)


@pytest.fixture
async def node_uuid(remnawave) -> str:
    """UUID любой существующей ноды панели"""
    nodes = await remnawave.nodes.get_all_nodes()
    if not len(nodes):
        pytest.skip("В окружении нет ни одной ноды")
    return str(nodes[0].uuid)


def _skip_without_connected_nodes(exc: ApiError) -> None:
    """Панель отвечает A219, когда ни одна нода не подключена."""
    if "Connected nodes not found" in str(exc):
        pytest.skip("В окружении нет подключённых нод")
    raise exc


async def _poll_geocheck(remnawave, job_id: str, attempts: int = 15, delay: float = 2.0):
    """Дождаться завершения geocheck-джобы"""
    for _ in range(attempts):
        result = await remnawave.connections.get_geocheck_by_node(job_id=job_id)
        if result.is_completed or result.is_failed:
            return result
        await asyncio.sleep(delay)
    return None


class TestGeocheck:
    """Geocheck ноды (Remnawave API v3.4.0+)"""

    @pytest.mark.asyncio
    async def test_request_geocheck_returns_job_id(self, remnawave, node_uuid):
        """Запрос geocheck ставит задачу и возвращает jobId"""
        response = await remnawave.connections.request_geocheck_by_node(
            node_uuid=node_uuid,
            body=GeocheckByNodeRequestDto(),
        )

        assert isinstance(response, GeocheckByNodeResponseDto)
        assert isinstance(response.job_id, str)
        assert response.job_id

    @pytest.mark.asyncio
    async def test_request_geocheck_with_source_ip(self, remnawave, node_uuid):
        """Тело запроса с ip/interface принимается панелью"""
        response = await remnawave.connections.request_geocheck_by_node(
            node_uuid=node_uuid,
            body=GeocheckByNodeRequestDto(ip="1.1.1.1"),
        )

        assert isinstance(response, GeocheckByNodeResponseDto)
        assert response.job_id

    @pytest.mark.asyncio
    async def test_geocheck_job_result(self, remnawave, node_uuid):
        """Результат geocheck-джобы разбирается моделью"""
        started = await remnawave.connections.request_geocheck_by_node(
            node_uuid=node_uuid,
            body=GeocheckByNodeRequestDto(),
        )

        result = await _poll_geocheck(remnawave, started.job_id)
        if result is None:
            pytest.skip("Нода не ответила на geocheck за отведённое время")

        assert isinstance(result, GeocheckByNodeResultResponseDto)
        assert isinstance(result.is_completed, bool)
        assert isinstance(result.is_failed, bool)

        if result.result is not None:
            assert isinstance(result.result, GeocheckResult)
            assert str(result.result.node_uuid) == node_uuid
            if result.result.image is not None:
                assert isinstance(result.result.image, GeocheckImageDto)
                assert result.result.image.format == "svg"
                assert result.result.image.encoding == "base64"
                assert result.result.image.media_type == "image/svg+xml"

    @pytest.mark.asyncio
    async def test_unknown_geocheck_job_raises_not_found(self, remnawave):
        """Неизвестный jobId даёт NotFoundError (A218)"""
        with pytest.raises(NotFoundError):
            await remnawave.connections.get_geocheck_by_node(job_id="sdk-missing-job")


class TestConnectionsByNode:
    """Ранее существовавшие маршруты connections остаются рабочими"""

    @pytest.mark.asyncio
    async def test_fetch_and_read_connections_by_node(self, remnawave, node_uuid):
        """Запрос IP-адресов по ноде возвращает jobId, результат читается"""
        started = await remnawave.connections.fetch_connections_by_node(node_uuid=node_uuid)
        assert isinstance(started, FetchUsersIpsResponseDto)
        assert started.job_id

        result = await remnawave.connections.get_connections_by_node(job_id=started.job_id)
        assert isinstance(result, FetchUsersIpsResultResponseDto)


class TestConnectionsByUser:
    """`result` приходит с числовым `userId` и без `userUuid` (панель >= 3.0)"""

    @pytest.fixture
    async def user_id(self, remnawave) -> int:
        users = await remnawave.users.get_all_users(size=1)
        if not users.users:
            pytest.skip("В окружении нет ни одного пользователя")
        return users.users[0].id

    @pytest.mark.asyncio
    async def test_fetch_and_read_connections_by_user(self, remnawave, user_id):
        started = await remnawave.connections.fetch_connections_by_user(user_id=user_id)
        assert isinstance(started, FetchIpsResponseDto)
        assert started.job_id

        result = None
        for _ in range(15):
            result = await remnawave.connections.get_connections_by_user(
                job_id=started.job_id
            )
            if result.is_completed or result.is_failed:
                break
            await asyncio.sleep(2.0)

        assert isinstance(result, FetchIpsResultResponseDto)
        if result.result is not None:
            assert result.result.user_id == user_id
            assert isinstance(result.result.user_id, int)
            assert isinstance(result.result.nodes, list)


class TestDropConnections:
    """Сброс активных подключений (202 Accepted)"""

    @pytest.mark.asyncio
    async def test_drop_by_user_ids_on_all_nodes(self, remnawave):
        users = await remnawave.users.get_all_users(size=1)
        if not users.users:
            pytest.skip("В окружении нет ни одного пользователя")

        try:
            response = await remnawave.connections.drop_connections(
                DropConnectionsRequestDto(
                    drop_by=DropByUserUuids(user_ids=[users.users[0].id]),
                    target_nodes=TargetAllNodes(),
                )
            )
        except ApiError as exc:
            _skip_without_connected_nodes(exc)

        assert response is None

    @pytest.mark.asyncio
    async def test_drop_by_ip_on_specific_nodes(self, remnawave, node_uuid):
        try:
            response = await remnawave.connections.drop_connections(
                DropConnectionsRequestDto(
                    drop_by=DropByIpAddresses(ip_addresses=["198.51.100.20"]),
                    target_nodes=TargetSpecificNodes(node_uuids=[node_uuid]),
                )
            )
        except ApiError as exc:
            _skip_without_connected_nodes(exc)

        assert response is None

    def test_selectors_serialise_with_their_discriminator(self):
        """dropBy/targetNodes уходят с полем-дискриминатором, иначе панель не разберёт"""
        dto = DropConnectionsRequestDto(
            drop_by=DropByUserUuids(user_ids=[1, 2]),
            target_nodes=TargetAllNodes(),
        )

        payload = dto.model_dump(exclude_none=True, by_alias=True, mode="json")
        assert payload["dropBy"] == {"by": "userIds", "userIds": [1, 2]}
        assert payload["targetNodes"] == {"target": "allNodes"}

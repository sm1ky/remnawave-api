"""Tests for the Node Integrations controller (Remnawave API v3.4.0+)."""
import pytest

from remnawave.exceptions import ConflictError, NotFoundError
from remnawave.models import (
    CreateNodeIntegrationRequestDto,
    CreateNodeIntegrationResponseDto,
    GetNodeIntegrationResponseDto,
    GetNodeIntegrationsResponseDto,
    UpdateNodeIntegrationRequestDto,
    UpdateNodeIntegrationResponseDto,
)
from tests.utils import generate_random_string


@pytest.fixture
async def node_integration(remnawave):
    """Создать временную интеграцию и удалить её после теста"""
    created = await remnawave.node_integrations.create_node_integration(
        CreateNodeIntegrationRequestDto(
            name=f"ni_{generate_random_string(length=8)}",
            description="Created by the SDK test suite",
            config={"kind": "test", "enabled": False},
        )
    )
    yield created
    try:
        await remnawave.node_integrations.delete_node_integration(uuid=str(created.uuid))
    except NotFoundError:
        pass


class TestNodeIntegrations:
    """Тесты для Node Integrations контроллера"""

    @pytest.mark.asyncio
    async def test_get_all_node_integrations(self, remnawave):
        """Тест получения списка всех интеграций"""
        response = await remnawave.node_integrations.get_all_node_integrations()

        assert isinstance(response, GetNodeIntegrationsResponseDto)
        assert isinstance(response.node_integrations, list)
        assert response.total >= len(response.node_integrations)

    @pytest.mark.asyncio
    async def test_create_node_integration(self, remnawave, node_integration):
        """Тест создания интеграции"""
        assert isinstance(node_integration, CreateNodeIntegrationResponseDto)
        assert node_integration.uuid is not None
        assert node_integration.description == "Created by the SDK test suite"
        assert node_integration.config == {"kind": "test", "enabled": False}

    @pytest.mark.asyncio
    async def test_get_node_integration_by_uuid(self, remnawave, node_integration):
        """Тест получения интеграции по uuid"""
        fetched = await remnawave.node_integrations.get_node_integration_by_uuid(
            uuid=str(node_integration.uuid)
        )

        assert isinstance(fetched, GetNodeIntegrationResponseDto)
        assert fetched.uuid == node_integration.uuid
        assert fetched.name == node_integration.name
        assert fetched.config == node_integration.config

    @pytest.mark.asyncio
    async def test_created_integration_is_listed(self, remnawave, node_integration):
        """Созданная интеграция присутствует в общем списке"""
        response = await remnawave.node_integrations.get_all_node_integrations()
        uuids = [integration.uuid for integration in response.node_integrations]

        assert node_integration.uuid in uuids

    @pytest.mark.asyncio
    async def test_update_node_integration(self, remnawave, node_integration):
        """Тест обновления интеграции"""
        updated_name = f"upd_{generate_random_string(length=8)}"
        updated = await remnawave.node_integrations.update_node_integration(
            UpdateNodeIntegrationRequestDto(
                uuid=node_integration.uuid,
                name=updated_name,
                description="Updated by the SDK test suite",
                config={"kind": "test", "enabled": True},
            )
        )

        assert isinstance(updated, UpdateNodeIntegrationResponseDto)
        assert updated.uuid == node_integration.uuid
        assert updated.name == updated_name
        assert updated.description == "Updated by the SDK test suite"
        assert updated.config == {"kind": "test", "enabled": True}

        fetched = await remnawave.node_integrations.get_node_integration_by_uuid(
            uuid=str(node_integration.uuid)
        )
        assert fetched.name == updated_name

    @pytest.mark.asyncio
    async def test_delete_node_integration(self, remnawave):
        """Тест удаления интеграции (204 No Content)"""
        created = await remnawave.node_integrations.create_node_integration(
            CreateNodeIntegrationRequestDto(
                name=f"ni_{generate_random_string(length=8)}",
                config={"kind": "test"},
            )
        )

        deleted = await remnawave.node_integrations.delete_node_integration(
            uuid=str(created.uuid)
        )
        assert deleted is None

        with pytest.raises(NotFoundError):
            await remnawave.node_integrations.get_node_integration_by_uuid(
                uuid=str(created.uuid)
            )

    @pytest.mark.asyncio
    async def test_duplicate_name_conflicts(self, remnawave, node_integration):
        """Повторное имя интеграции отклоняется (A244)"""
        with pytest.raises(ConflictError):
            await remnawave.node_integrations.create_node_integration(
                CreateNodeIntegrationRequestDto(
                    name=node_integration.name,
                    config={"kind": "test"},
                )
            )

    @pytest.mark.asyncio
    async def test_get_unknown_uuid_raises_not_found(self, remnawave):
        """Неизвестный uuid интеграции даёт NotFoundError (A238)"""
        with pytest.raises(NotFoundError):
            await remnawave.node_integrations.get_node_integration_by_uuid(
                uuid="00000000-0000-0000-0000-000000000000"
            )

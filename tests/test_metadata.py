import os
from datetime import datetime, timedelta, timezone

import pytest

from remnawave.exceptions import NotFoundError
from remnawave.models import (
    CreateUserBodyDto,
    GetNodeMetadataResponseDto,
    GetUserMetadataResponseDto,
    UpsertNodeMetadataRequestBodyDto,
    UpsertNodeMetadataResponseDto,
    UpsertUserMetadataRequestBodyDto,
    UpsertUserMetadataResponseDto,
)
from tests.utils import generate_random_string


REMNAWAVE_NODE_UUID = os.getenv("REMNAWAVE_NODE_UUID")


class TestUserMetadata:
    """Тесты для User Metadata контроллера"""

    @pytest.mark.asyncio
    async def test_upsert_and_get_user_metadata(self, remnawave):
        """Тест создания/обновления и получения метаданных пользователя"""
        # Create test user first
        username = generate_random_string(length=8)
        expire_at = datetime.now(timezone.utc) + timedelta(days=7)
        create_user = await remnawave.users.create_user(
            CreateUserBodyDto(username=username, expire_at=expire_at)
        )
        user_id = create_user.id
        
        try:
            # Upsert metadata
            test_metadata = {
                "custom_field_1": "test_value_1",
                "custom_field_2": 123,
                "nested": {
                    "field": "value"
                }
            }
            
            upsert_response = await remnawave.metadata.upsert_user_metadata(
                user_id=user_id,
                body=UpsertUserMetadataRequestBodyDto(metadata=test_metadata)
            )
            
            assert isinstance(upsert_response, UpsertUserMetadataResponseDto)
            
            # Get metadata
            get_response = await remnawave.metadata.get_user_metadata(user_id=user_id)
            
            assert isinstance(get_response, GetUserMetadataResponseDto)
            assert hasattr(get_response, "metadata")
            assert get_response.metadata is not None
            assert get_response.metadata.get("custom_field_1") == "test_value_1"
            assert get_response.metadata.get("custom_field_2") == 123
            assert get_response.metadata.get("nested") == {"field": "value"}
            
        finally:
            # Cleanup
            await remnawave.users.delete_user(user_id=user_id)

    @pytest.mark.asyncio
    async def test_update_existing_user_metadata(self, remnawave):
        """Тест обновления существующих метаданных пользователя"""
        # Create test user
        username = generate_random_string(length=8)
        expire_at = datetime.now(timezone.utc) + timedelta(days=7)
        create_user = await remnawave.users.create_user(
            CreateUserBodyDto(username=username, expire_at=expire_at)
        )
        user_id = create_user.id
        
        try:
            # Initial metadata
            initial_metadata = {"field1": "value1"}
            await remnawave.metadata.upsert_user_metadata(
                user_id=user_id,
                body=UpsertUserMetadataRequestBodyDto(metadata=initial_metadata)
            )
            
            # Update metadata
            updated_metadata = {
                "field1": "updated_value1",
                "field2": "value2"
            }
            upsert_response = await remnawave.metadata.upsert_user_metadata(
                user_id=user_id,
                body=UpsertUserMetadataRequestBodyDto(metadata=updated_metadata)
            )
            
            assert isinstance(upsert_response, UpsertUserMetadataResponseDto)
            
            # Verify update
            get_response = await remnawave.metadata.get_user_metadata(user_id=user_id)
            assert get_response.metadata.get("field1") == "updated_value1"
            assert get_response.metadata.get("field2") == "value2"
            
        finally:
            # Cleanup
            await remnawave.users.delete_user(user_id=user_id)

    @pytest.mark.asyncio
    async def test_get_user_metadata_empty(self, remnawave):
        """Тест получения пустых метаданных пользователя"""
        # Create test user without metadata
        username = generate_random_string(length=8)
        expire_at = datetime.now(timezone.utc) + timedelta(days=7)
        create_user = await remnawave.users.create_user(
            CreateUserBodyDto(username=username, expire_at=expire_at)
        )
        user_id = create_user.id
        
        try:
            # Get metadata (API может вернуть пустой объект или 404, если метаданные не созданы)
            try:
                get_response = await remnawave.metadata.get_user_metadata(user_id=user_id)
                assert isinstance(get_response, GetUserMetadataResponseDto)
                assert get_response.metadata is None or get_response.metadata == {}
            except NotFoundError:
                # Ожидаемое поведение для пользователя без метаданных
                assert True

        finally:
            # Cleanup
            await remnawave.users.delete_user(user_id=user_id)


class TestNodeMetadata:
    """Тесты для Node Metadata контроллера"""

    @pytest.mark.asyncio
    async def test_upsert_and_get_node_metadata(self, remnawave):
        """Тест создания/обновления и получения метаданных ноды"""
        # Skip if no node UUID configured
        if not REMNAWAVE_NODE_UUID:
            pytest.skip("REMNAWAVE_NODE_UUID not set in environment")
        
        node_uuid = REMNAWAVE_NODE_UUID
        
        # Upsert metadata
        test_metadata = {
            "location": "datacenter-1",
            "region": "us-east",
            "capacity": 1000,
            "config": {
                "max_users": 100
            }
        }
        
        upsert_response = await remnawave.metadata.upsert_node_metadata(
            uuid=node_uuid,
            body=UpsertNodeMetadataRequestBodyDto(metadata=test_metadata)
        )
        
        assert isinstance(upsert_response, UpsertNodeMetadataResponseDto)
        
        # Get metadata
        get_response = await remnawave.metadata.get_node_metadata(uuid=node_uuid)
        
        assert isinstance(get_response, GetNodeMetadataResponseDto)
        assert hasattr(get_response, "metadata")
        assert get_response.metadata is not None
        assert get_response.metadata.get("location") == "datacenter-1"
        assert get_response.metadata.get("region") == "us-east"
        assert get_response.metadata.get("capacity") == 1000
        assert get_response.metadata.get("config") == {"max_users": 100}

    @pytest.mark.asyncio
    async def test_update_existing_node_metadata(self, remnawave):
        """Тест обновления существующих метаданных ноды"""
        if not REMNAWAVE_NODE_UUID:
            pytest.skip("REMNAWAVE_NODE_UUID not set in environment")
        
        node_uuid = REMNAWAVE_NODE_UUID
        
        # Initial metadata
        initial_metadata = {"status": "active"}
        await remnawave.metadata.upsert_node_metadata(
            uuid=node_uuid,
            body=UpsertNodeMetadataRequestBodyDto(metadata=initial_metadata)
        )
        
        # Update metadata
        updated_metadata = {
            "status": "maintenance",
            "last_check": "2026-03-09"
        }
        upsert_response = await remnawave.metadata.upsert_node_metadata(
            uuid=node_uuid,
            body=UpsertNodeMetadataRequestBodyDto(metadata=updated_metadata)
        )
        
        assert isinstance(upsert_response, UpsertNodeMetadataResponseDto)
        
        # Verify update
        get_response = await remnawave.metadata.get_node_metadata(uuid=node_uuid)
        assert get_response.metadata.get("status") == "maintenance"
        assert get_response.metadata.get("last_check") == "2026-03-09"

    @pytest.mark.asyncio
    async def test_get_node_metadata(self, remnawave):
        """Тест получения метаданных ноды"""
        if not REMNAWAVE_NODE_UUID:
            pytest.skip("REMNAWAVE_NODE_UUID not set in environment")
        
        node_uuid = REMNAWAVE_NODE_UUID
        
        # Get metadata
        get_response = await remnawave.metadata.get_node_metadata(uuid=node_uuid)
        
        assert isinstance(get_response, GetNodeMetadataResponseDto)
        assert hasattr(get_response, "metadata")
        # Metadata can be empty dict or None or contain data depending on previous tests

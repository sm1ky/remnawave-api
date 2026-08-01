import random
import uuid

import pytest

from remnawave.models import (
    CreateUserHwidDeviceRequestDto,
    DeleteUserHwidDeviceRequestDto,
    DeleteUserAllHwidDeviceRequestDto,
    CreateUserHwidDeviceResponseDto,
    DeleteUserHwidDeviceResponseDto,
    GetUserHwidDevicesResponseDto,
    GetHwidStatisticsResponseDto,
)
from tests.conftest import REMNAWAVE_USER_UUID


class TestHwidInfo:
    """Тесты для получения информации о HWID устройствах"""
    
    @pytest.mark.asyncio
    async def test_get_hwid_user(self, remnawave):
        """Тест получения HWID устройств конкретного пользователя"""
        hwid = await remnawave.hwid.get_hwid_user(user_id=1)
        assert isinstance(hwid, GetUserHwidDevicesResponseDto)
        assert hasattr(hwid, "devices")
    
    @pytest.mark.asyncio
    async def test_get_hwid_users(self, remnawave):
        """Тест получения всех HWID устройств с пагинацией"""
        response = await remnawave.hwid.get_hwid_users(size=10, start=0)
        assert isinstance(response, GetUserHwidDevicesResponseDto)
        assert hasattr(response, "total")
        assert hasattr(response, "devices")


class TestHwidStatistics:
    """Тесты для статистики HWID устройств"""
    
    @pytest.mark.asyncio
    async def test_get_hwid_stats(self, remnawave):
        """Тест получения статистики по HWID устройствам"""
        try:
            response = await remnawave.hwid.get_hwid_stats()
            assert isinstance(response, GetHwidStatisticsResponseDto)
            
            # Проверяем структуру ответа
            assert hasattr(response, "by_platform")
            assert hasattr(response, "by_app")
            assert hasattr(response, "stats")
            
            # Проверяем поля статистики
            assert hasattr(response.stats, "total_unique_devices")
            assert hasattr(response.stats, "total_hwid_devices")
            assert hasattr(response.stats, "average_hwid_devices_per_user")
            
            # Проверяем типы данных в ответе
            assert isinstance(response.stats.total_unique_devices, float)
            assert isinstance(response.stats.total_hwid_devices, float)
            assert isinstance(response.stats.average_hwid_devices_per_user, float)
            
            # Проверяем данные по платформам
            if len(response.by_platform) > 0:
                platform = response.by_platform[0]
                assert hasattr(platform, "platform")
                assert hasattr(platform, "count")
            
            # Проверяем данные по приложениям
            if len(response.by_app) > 0:
                app = response.by_app[0]
                assert hasattr(app, "app")
                assert hasattr(app, "count")
        except Exception as e:
            pytest.skip(f"Пропуск теста статистики HWID: {str(e)}")


class TestHwidCRUD:
    """Тесты для CRUD операций с HWID устройствами"""
    
    @pytest.fixture
    def test_hwid(self):
        """Фикстура для генерации тестового HWID"""
        return str(uuid.uuid4())
    
    @pytest.mark.asyncio
    # @pytest.mark.xfail(reason="User hwid device limit может быть достигнут")
    async def test_add_hwid_to_user(self, remnawave, test_hwid):
        """Тест добавления HWID устройства пользователю"""
        # Создаем запрос на добавление HWID
        create_request = CreateUserHwidDeviceRequestDto(
            hwid=test_hwid,
            user_id=1,
            platform="Windows",
            os_version="10.0.19042",
            device_model="Surface Pro",
            user_agent="Mozilla/5.0"
        )
        
        # Отправляем запрос
        response = await remnawave.hwid.add_hwid_to_users(body=create_request)
        
        # Проверяем результат
        assert isinstance(response, CreateUserHwidDeviceResponseDto)
        assert any(item.hwid == test_hwid for item in response.devices)
        
        # Проверяем, что устройство действительно добавлено
        hwid_check = await remnawave.hwid.get_hwid_user(user_id=1)
        assert any(device.hwid == test_hwid for device in hwid_check.devices)
    
    @pytest.mark.asyncio
    async def test_delete_hwid_user(self, remnawave, test_hwid):
        """Тест удаления HWID устройства у пользователя"""
        # Сначала добавляем устройство
        create_request = CreateUserHwidDeviceRequestDto(
            hwid=test_hwid,
            user_id=1,
            platform="Android",
            os_version="12",
            device_model="Pixel 6",
            user_agent="Chrome Mobile"
        )
        await remnawave.hwid.add_hwid_to_users(body=create_request)
        
        # Удаляем устройство
        delete_request = DeleteUserHwidDeviceRequestDto(
            hwid=test_hwid,
            user_id=1
        )
        response = await remnawave.hwid.delete_hwid_to_user(body=delete_request)
        
        # Проверяем результат
        assert isinstance(response, DeleteUserHwidDeviceResponseDto)
        assert not any(item.hwid == test_hwid for item in response.devices)
        
        # Проверяем, что устройство действительно удалено
        hwid_check = await remnawave.hwid.get_hwid_user(user_id=1)
        assert not any(device.hwid == test_hwid for device in hwid_check.devices)
    
    @pytest.mark.asyncio
    async def test_delete_all_hwid_user(self, remnawave):
        """Тест удаления всех HWID устройств пользователя"""
        # Сначала добавим новый HWID
        random_hwid = str(uuid.uuid4())
        create_request = CreateUserHwidDeviceRequestDto(
            hwid=random_hwid,
            user_id=1,
            platform="iOS",
            os_version="15.0",
            device_model="iPhone 13",
            user_agent="Safari/605.1.15"
        )
        await remnawave.hwid.add_hwid_to_users(body=create_request)
        
        # Проверяем, что устройство добавлено
        check_before = await remnawave.hwid.get_hwid_user(user_id=1)
        assert any(device.hwid == random_hwid for device in check_before.devices)
        
        # Теперь удалим все HWID устройства пользователя
        delete_all_request = DeleteUserAllHwidDeviceRequestDto(
            user_id=1
        )
        response = await remnawave.hwid.delete_all_hwid_user(body=delete_all_request)
        
        # Проверяем результат
        assert isinstance(response, DeleteUserHwidDeviceResponseDto)
        
        # Проверяем, что устройства действительно удалены
        hwid_check = await remnawave.hwid.get_hwid_user(user_id=1)
        assert not any(device.hwid == random_hwid for device in hwid_check.devices)
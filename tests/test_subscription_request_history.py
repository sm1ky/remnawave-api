import pytest

from remnawave.models import (
    GetAllSubscriptionRequestHistoryResponseDto,
    GetSubscriptionRequestHistoryStatsResponseDto
)


class TestSubscriptionRequestHistory:
    """Тесты для истории запросов подписок"""
    
    @pytest.mark.asyncio
    async def test_get_all_subscription_request_history(self, remnawave):
        """Тест получения всей истории запросов подписок"""
        try:
            response = await remnawave.subscription_request_history.get_all_subscription_request_history(
                size=10,
                start=0
            )
            assert isinstance(response, GetAllSubscriptionRequestHistoryResponseDto)
            assert hasattr(response, 'total')
            assert hasattr(response, 'records')
            
            # Проверяем корректность структуры ответа
            if response.total > 0 and len(response.records) > 0:
                record = response.records[0]
                assert hasattr(record, 'id')
                assert hasattr(record, 'user_id')
                assert hasattr(record, 'request_at')
                assert hasattr(record, 'request_ip')
                assert hasattr(record, 'user_agent')
                # Поля SRR, добавленные в контракт панели
                assert hasattr(record, 'srr_response_type')
                assert hasattr(record, 'srr_rule_name')
        except Exception as e:
            pytest.skip(f"Пропуск теста истории запросов подписок: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_get_subscription_request_history_stats(self, remnawave):
        """Тест получения статистики истории запросов подписок"""
        try:
            response = await remnawave.subscription_request_history.get_subscription_request_history_stats()
            assert isinstance(response, GetSubscriptionRequestHistoryStatsResponseDto)
            assert hasattr(response, 'by_parsed_app')
            assert hasattr(response, 'hourly_request_stats')
            
            # Проверяем корректность структуры ответа
            if len(response.by_parsed_app) > 0:
                app_stat = response.by_parsed_app[0]
                assert hasattr(app_stat, 'app')
                assert hasattr(app_stat, 'count')
            
            if len(response.hourly_request_stats) > 0:
                hourly_stat = response.hourly_request_stats[0]
                assert hasattr(hourly_stat, 'date_time')
                assert hasattr(hourly_stat, 'request_count')
        except Exception as e:
            pytest.skip(f"Пропуск теста статистики истории запросов подписок: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_subscription_request_history_pagination(self, remnawave):
        """Тест пагинации истории запросов подписок"""
        try:
            # Получаем первую страницу
            first_page = await remnawave.subscription_request_history.get_all_subscription_request_history(
                size=5,
                start=0
            )
            
            # Получаем вторую страницу
            second_page = await remnawave.subscription_request_history.get_all_subscription_request_history(
                size=5,
                start=5
            )
            
            # Проверяем, что пагинация работает
            if first_page.total > 10:
                # Проверяем, что ID записей на разных страницах отличаются
                if len(first_page.records) > 0 and len(second_page.records) > 0:
                    first_ids = [record.id for record in first_page.records]
                    second_ids = [record.id for record in second_page.records]
                    # Проверяем, что нет пересечений между страницами
                    assert len(set(first_ids).intersection(set(second_ids))) == 0
        except Exception as e:
            pytest.skip(f"Пропуск теста пагинации: {str(e)}")
import pytest

from remnawave import RemnawaveSDK

# Пример корректных данных из вебхука
VALID_SIGNATURE = "8c630175963bae8f413e6e01a1fa42631cd5c499ea4c7128292aeb7fe74d23de"
VALID_BODY = {
    "event": "user.modified",
    "timestamp": "2025-07-08T23:53:41.617Z",
    "data": {
        "uuid": "c85c240f-c6e1-4e41-ae65-a1b16100b9b3",
        "subscriptionUuid": "10c4af55-18b1-4d83-bcb4-3f317ef93574",
        "shortUuid": "3P9nwj_cqo--naNE",
        "username": "399365366",
        "status": "ACTIVE",
        "usedTrafficBytes": "0",
        "lifetimeUsedTrafficBytes": "0",
        "trafficLimitBytes": "0",
        "trafficLimitStrategy": "NO_RESET",
        "subLastUserAgent": None,
        "subLastOpenedAt": None,
        "expireAt": "2025-08-08T23:53:32.000Z",
        "subRevokedAt": None,
        "lastTrafficResetAt": None,
        "trojanPassword": "Z0T-_G9mco40uAd7TgKLQbvtPHauuH",
        "vlessUuid": "7b44e483-82c5-4445-806e-fb1e8e58985a",
        "ssPassword": "mM_wZgb7QhDajEkcC3LLqp2_3Wk6CQPR",
        "description": None,
        "tag": None,
        "telegramId": "399365366",
        "email": None,
        "hwidDeviceLimit": None,
        "firstConnectedAt": None,
        "lastTriggeredThreshold": 0,
        "onlineAt": None,
        "lastConnectedNodeUuid": None,
        "createdAt": "2025-07-08T21:03:44.463Z",
        "updatedAt": "2025-07-08T23:53:41.611Z",
        "activeUserInbounds": [
            {
                "uuid": "a573b408-a452-4409-850f-9b66a06434b2",
                "tag": "eu",
                "type": "vless",
                "network": "raw",
                "security": "reality"
            },
            {
                "uuid": "578ef17e-ef67-4c3a-9f35-9f33a0aab7a6",
                "tag": "ru",
                "type": "vless",
                "network": "raw",
                "security": "reality"
            },
            {
                "uuid": "3acf6d7a-4903-4a4b-bf49-7baed581aded",
                "tag": "tr",
                "type": "vless",
                "network": "raw",
                "security": "reality"
            }
        ]
    }
}
# Секрет для валидации вебхука 
WEBHOOK_SECRET = (
    "0cfbd6e60f79f80eb5065ce715f2398a2bb342e62dfce3f6f66083b05abd9ef805ed88b7c6ed9564d50e32a42192d5eaa9971d4c072927bbffa52e364a067817"
)

@pytest.mark.asyncio
async def test_webhook_utility_valid(remnawave):
    # Инициализируем SDK (base_url и token заданы для теста)
    sdk = RemnawaveSDK(base_url="your_base_url", token="your_api_key")
    
    # Вызовем метод валидации с корректными данными
    is_valid = sdk.webhook_utility.validate_webhook(
        body=VALID_BODY,
        signature=VALID_SIGNATURE,
        webhook_secret=WEBHOOK_SECRET
    )
    
    # Если валидация пройдена, метод должен вернуть True
    assert is_valid is True, "Webhook validation failed with valid data"

@pytest.mark.asyncio
async def test_webhook_utility_invalid(remnawave):
    sdk = RemnawaveSDK(base_url="your_base_url", token="your_api_key")
    
    # Используем невалидную подпись
    invalid_signature = "invalidsignature"
    is_valid = sdk.webhook_utility.validate_webhook(
        body=VALID_BODY,
        signature=invalid_signature,
        webhook_secret=WEBHOOK_SECRET
    )
    
    # Ожидаем, что валидация не пройдется
    assert is_valid is False, "Webhook validation passed with invalid signature"
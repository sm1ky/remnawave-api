from remnawave.models.webhook import HwidUserDeviceDto, UserDto, WebhookPayloadDto

TIMESTAMP = "2026-08-06T00:00:00Z"
VLESS_UUID = "00000000-0000-0000-0000-000000000001"


def _user_payload() -> dict:
    """User object as emitted by panel >=3.0 webhooks — no top-level ``uuid``."""
    return {
        "id": 1,
        "shortUuid": "short-uuid",
        "username": "test-user",
        "status": "ACTIVE",
        "userTraffic": {
            "usedTrafficBytes": 0,
            "lifetimeUsedTrafficBytes": 0,
        },
        "trafficLimitBytes": 0,
        "trafficLimitStrategy": "NO_RESET",
        "expireAt": TIMESTAMP,
        "trojanPassword": "trojan-password",
        "vlessUuid": VLESS_UUID,
        "ssPassword": "ss-password",
        "lastTriggeredThreshold": 0,
        "subscriptionUrl": "https://example.com/subscription",
        "createdAt": TIMESTAMP,
        "updatedAt": TIMESTAMP,
    }


def test_hwid_webhook_device_parses_v32_user_id():
    device = HwidUserDeviceDto.model_validate(
        {
            "hwid": "device-hwid",
            "userId": 42,
            "requestIp": "192.0.2.1",
            "createdAt": TIMESTAMP,
            "updatedAt": TIMESTAMP,
        }
    )

    assert device.user_id == 42
    assert device.request_ip == "192.0.2.1"


def test_user_webhook_event_parses_without_uuid():
    payload = WebhookPayloadDto.from_dict(
        {
            "event": "user.modified",
            "timestamp": TIMESTAMP,
            "data": _user_payload(),
        }
    )

    assert isinstance(payload.data, UserDto)
    assert payload.data.uuid is None
    assert payload.data.id == 1
    assert payload.data.username == "test-user"


def test_hwid_webhook_payload_parses_without_user_uuid():
    payload = WebhookPayloadDto.from_dict(
        {
            "event": "user_hwid_devices.added",
            "timestamp": TIMESTAMP,
            "data": {
                "user": _user_payload(),
                "hwidUserDevice": {
                    "hwid": "device-hwid",
                    "userId": 42,
                    "requestIp": "192.0.2.1",
                    "createdAt": TIMESTAMP,
                    "updatedAt": TIMESTAMP,
                },
            },
        }
    )

    assert payload.data.user.uuid is None
    assert payload.data.hwid_user_device.user_id == 42
    assert payload.data.hwid_user_device.request_ip == "192.0.2.1"

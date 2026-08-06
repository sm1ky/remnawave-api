from remnawave.models.webhook import HwidUserDeviceDto, WebhookPayloadDto


def test_hwid_webhook_device_parses_v32_user_id():
    device = HwidUserDeviceDto.model_validate(
        {
            "hwid": "device-hwid",
            "userId": 42,
            "requestIp": "192.0.2.1",
            "createdAt": "2026-08-06T00:00:00Z",
            "updatedAt": "2026-08-06T00:00:00Z",
        }
    )

    assert device.user_id == 42
    assert device.request_ip == "192.0.2.1"


def test_hwid_webhook_payload_parses_without_user_uuid():
    user_uuid = "00000000-0000-0000-0000-000000000001"
    timestamp = "2026-08-06T00:00:00Z"
    payload = WebhookPayloadDto.from_dict(
        {
            "event": "user_hwid_devices.added",
            "timestamp": timestamp,
            "data": {
                "user": {
                    "uuid": user_uuid,
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
                    "expireAt": timestamp,
                    "trojanPassword": "trojan-password",
                    "vlessUuid": user_uuid,
                    "ssPassword": "ss-password",
                    "lastTriggeredThreshold": 0,
                    "subscriptionUrl": "https://example.com/subscription",
                    "createdAt": timestamp,
                    "updatedAt": timestamp,
                },
                "hwidUserDevice": {
                    "hwid": "device-hwid",
                    "userId": 42,
                    "requestIp": "192.0.2.1",
                    "createdAt": timestamp,
                    "updatedAt": timestamp,
                },
            },
        }
    )

    assert payload.data.hwid_user_device.user_id == 42

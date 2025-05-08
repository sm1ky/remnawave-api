import os

import pytest
from dotenv import load_dotenv

from remnawave_api import RemnawaveSDK

load_dotenv()
REMNAWAVE_BASE_URL = os.getenv("REMNAWAVE_BASE_URL")
REMNAWAVE_TOKEN = os.getenv("REMNAWAVE_TOKEN")
REMNAWAVE_ADMIN_USERNAME = os.getenv("REMNAWAVE_ADMIN_USERNAME")
REMNAWAVE_ADMIN_PASSWORD = os.getenv("REMNAWAVE_ADMIN_PASSWORD")
REMNAWAVE_INBOUND_UUID = os.getenv("REMNAWAVE_INBOUND_UUID")
REMNAWAVE_USER_UUID = os.getenv("REMNAWAVE_USER_UUID")
REMNAWAVE_SHORT_UUID = os.getenv("REMNAWAVE_SHORT_UUID")

@pytest.fixture
async def remnawave() -> RemnawaveSDK:
    assert REMNAWAVE_TOKEN
    assert REMNAWAVE_BASE_URL

    sdk = RemnawaveSDK(
        base_url=REMNAWAVE_BASE_URL,
        token=REMNAWAVE_TOKEN,
    )

    assert sdk.api_tokens_management is not None
    assert sdk.auth
    assert sdk.bandwidthstats is not None
    assert sdk.hosts is not None
    assert sdk.hosts_bulk_actions is not None
    assert sdk.inbounds is not None
    assert sdk.inbounds_bulk_actions is not None
    assert sdk.keygen is not None
    assert sdk.nodes is not None
    assert sdk.subscription is not None
    assert sdk.subscriptions_settings is not None
    assert sdk.subscriptions_template is not None
    assert sdk.system is not None
    assert sdk.users is not None
    assert sdk.users_bulk_actions is not None
    assert sdk.users_stats is not None
    assert sdk.xray_config is not None
    assert sdk.hwid is not None
    return sdk

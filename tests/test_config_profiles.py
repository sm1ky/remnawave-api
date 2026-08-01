import pytest

from remnawave.models import (
    CreateConfigProfileRequestDto,
    CreateConfigProfileResponseDto,
    DeleteConfigProfileResponseDto,
    GetAllConfigProfilesResponseDto,
    GetAllInboundsResponseDto,
    GetConfigProfileByUuidResponseDto,
    GetInboundsByProfileUuidResponseDto,
    ReorderConfigProfileItem,
    ReorderConfigProfilesRequestDto,
    ReorderConfigProfilesResponseDto,
    UpdateConfigProfileRequestDto,
    UpdateConfigProfileResponseDto,
)
from tests.utils import generate_random_string


@pytest.mark.asyncio
async def test_config_profiles(remnawave) -> None:
    profile_name = f"test_profile_{generate_random_string(length=6)}"
    config = {
        "log": {
            "dnsLog": False,
            "loglevel": "warning"
        },
        "dns": {
            "hosts": {
                "dns.fxccc.cc": "138.199.175.237"
            },
            "servers": [
                "https://dns.fxccc.cc/dns-query"
            ],
            "disableCache": False,
            "queryStrategy": "UseIPv4",
            "disableFallbackIfMatch": True
        },
        "inbounds": [
            {
                "tag": f"Shadowsocks TCP [{profile_name}]",
                "port": 1080,
                "listen": "0.0.0.0",
                "protocol": "shadowsocks",
                "settings": {
                    "clients": [],
                    "network": "tcp,udp"
                }
            }
        ],
        "outbounds": [
            {
                "tag": "DIRECT",
                "protocol": "freedom"
            },
            {
                "tag": "BLOCK",
                "protocol": "blackhole"
            },
            {
                "tag": "dns-out",
                "protocol": "dns"
            }
        ],
        "routing": {
            "rules": [
                {
                    "ip": [
                        "geoip:private"
                    ],
                    "type": "field",
                    "domain": [
                        "geosite:private"
                    ],
                    "protocol": [
                        "bittorrent"
                    ],
                    "outboundTag": "BLOCK"
                },
                {
                    "type": "field",
                    "network": "tcp,udp",
                    "outboundTag": "DIRECT"
                }
            ],
            "domainStrategy": "IPIfNonMatch"
        }
    }
    # Test create config profile
    create_profile = await remnawave.config_profiles.create_config_profile(
        CreateConfigProfileRequestDto(
            name=profile_name,
            config=config
        )
    )
    
    assert isinstance(create_profile, CreateConfigProfileResponseDto)
    assert create_profile.name == profile_name

    profile_uuid = str(create_profile.uuid)

    # Test get all config profiles
    all_profiles = await remnawave.config_profiles.get_config_profiles()
    assert isinstance(all_profiles, GetAllConfigProfilesResponseDto)
    assert all_profiles.total > 0
    assert len(all_profiles.config_profiles) > 0
    
    # Test get config profile by uuid
    profile_by_uuid = await remnawave.config_profiles.get_config_profile_by_uuid(profile_uuid)
    assert isinstance(profile_by_uuid, GetConfigProfileByUuidResponseDto)
    assert profile_by_uuid.name == profile_name
    
    # Test update config profile
    updated_name = f"updated_{profile_name}"
    update_profile = await remnawave.config_profiles.update_config_profile(
        UpdateConfigProfileRequestDto(
            uuid=create_profile.uuid,
            # name=updated_name,
            config=profile_by_uuid.config
        )
    )
    
    assert isinstance(update_profile, UpdateConfigProfileResponseDto)
    assert update_profile.config == profile_by_uuid.config

    # Test get all inbounds
    all_inbounds = await remnawave.config_profiles.get_all_inbounds()
    assert isinstance(all_inbounds, GetAllInboundsResponseDto)
    
    # Test get inbounds by profile uuid
    inbounds_by_profile = await remnawave.config_profiles.get_inbounds_by_profile_uuid(profile_uuid)
    assert isinstance(inbounds_by_profile, GetInboundsByProfileUuidResponseDto)
    
    # Test reorder config profiles
    all_profiles_before_reorder = await remnawave.config_profiles.get_config_profiles()
    if len(all_profiles_before_reorder.config_profiles) >= 2:
        items = [
            ReorderConfigProfileItem(
                uuid=profile.uuid,
                view_position=idx
            )
            for idx, profile in enumerate(all_profiles_before_reorder.config_profiles)
        ]
        reorder_result = await remnawave.config_profiles.reorder_config_profiles(
            ReorderConfigProfilesRequestDto(items=items)
        )
        assert isinstance(reorder_result, ReorderConfigProfilesResponseDto)
    
    # Test delete config profile
    delete_profile = await remnawave.config_profiles.delete_config_profile_by_uuid(profile_uuid)
    assert delete_profile is None

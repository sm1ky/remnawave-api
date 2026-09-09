"""Tests for the per-resource /tags endpoints (Remnawave API v3.4.0+)."""
import pytest

from remnawave.enums import TemplateType
from remnawave.exceptions import NotFoundError
from remnawave.models import (
    CreateConfigProfileRequestDto,
    CreateExternalSquadRequestDto,
    CreateInternalSquadRequestDto,
    CreateSubscriptionPageConfigRequestDto,
    CreateSubscriptionTemplateRequestDto,
    GetConfigProfilesTagsResponseDto,
    GetExternalSquadsTagsResponseDto,
    GetInternalSquadsTagsResponseDto,
    GetSubpageConfigsTagsResponseDto,
    GetSubscriptionTemplatesTagsResponseDto,
    SetConfigProfilesTagsRequestDto,
    SetConfigProfilesTagsResponseDto,
    SetExternalSquadsTagsRequestDto,
    SetExternalSquadsTagsResponseDto,
    SetInternalSquadsTagsRequestDto,
    SetInternalSquadsTagsResponseDto,
    SetSubpageConfigsTagsRequestDto,
    SetSubpageConfigsTagsResponseDto,
    SetSubscriptionTemplatesTagsRequestDto,
    SetSubscriptionTemplatesTagsResponseDto,
)
from tests.conftest import REMNAWAVE_INBOUND_UUID
from tests.utils import generate_random_string

TAGS = ["SDK_TEST", "TAGS:CHECK"]


def _minimal_xray_config(name: str) -> dict:
    return {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "tag": f"Shadowsocks TCP [{name}]",
                "port": 1080,
                "listen": "0.0.0.0",
                "protocol": "shadowsocks",
                "settings": {"clients": [], "network": "tcp,udp"},
            }
        ],
        "outbounds": [
            {"tag": "DIRECT", "protocol": "freedom"},
            {"tag": "BLOCK", "protocol": "blackhole"},
        ],
        "routing": {"rules": [], "domainStrategy": "IPIfNonMatch"},
    }


class TestConfigProfilesTags:
    @pytest.fixture
    async def config_profile(self, remnawave):
        name = f"tags_profile_{generate_random_string(length=6)}"
        created = await remnawave.config_profiles.create_config_profile(
            CreateConfigProfileRequestDto(name=name, config=_minimal_xray_config(name))
        )
        yield created
        try:
            await remnawave.config_profiles.delete_config_profile_by_uuid(str(created.uuid))
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_get_tags(self, remnawave):
        response = await remnawave.config_profiles.get_config_profiles_tags()
        assert isinstance(response, GetConfigProfilesTagsResponseDto)
        assert isinstance(response.tags, list)

    @pytest.mark.asyncio
    async def test_new_profile_has_empty_tags(self, config_profile):
        assert config_profile.tags == []

    @pytest.mark.asyncio
    async def test_set_tags(self, remnawave, config_profile):
        response = await remnawave.config_profiles.set_config_profile_tags(
            SetConfigProfilesTagsRequestDto(uuid=config_profile.uuid, tags=TAGS)
        )

        assert isinstance(response, SetConfigProfilesTagsResponseDto)
        assert response.uuid == config_profile.uuid
        assert sorted(response.tags) == sorted(TAGS)

        fetched = await remnawave.config_profiles.get_config_profile_by_uuid(
            str(config_profile.uuid)
        )
        assert sorted(fetched.tags) == sorted(TAGS)

        all_tags = await remnawave.config_profiles.get_config_profiles_tags()
        assert set(TAGS).issubset(set(all_tags.tags))


class TestInternalSquadsTags:
    @pytest.fixture
    async def internal_squad(self, remnawave):
        created = await remnawave.internal_squads.create_internal_squad(
            CreateInternalSquadRequestDto(
                name=f"tags_squad_{generate_random_string(length=6)}",
                inbounds=[REMNAWAVE_INBOUND_UUID],
            )
        )
        yield created
        try:
            await remnawave.internal_squads.delete_internal_squad(str(created.uuid))
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_get_tags(self, remnawave):
        response = await remnawave.internal_squads.get_internal_squads_tags()
        assert isinstance(response, GetInternalSquadsTagsResponseDto)
        assert isinstance(response.tags, list)

    @pytest.mark.asyncio
    async def test_new_squad_has_empty_tags(self, internal_squad):
        assert internal_squad.tags == []

    @pytest.mark.asyncio
    async def test_set_tags(self, remnawave, internal_squad):
        response = await remnawave.internal_squads.set_internal_squad_tags(
            SetInternalSquadsTagsRequestDto(uuid=internal_squad.uuid, tags=TAGS)
        )

        assert isinstance(response, SetInternalSquadsTagsResponseDto)
        assert response.uuid == internal_squad.uuid
        assert sorted(response.tags) == sorted(TAGS)

        fetched = await remnawave.internal_squads.get_internal_squad_by_uuid(
            str(internal_squad.uuid)
        )
        assert sorted(fetched.tags) == sorted(TAGS)


class TestExternalSquadsTags:
    @pytest.fixture
    async def external_squad(self, remnawave):
        created = await remnawave.external_squads.create_external_squad(
            CreateExternalSquadRequestDto(
                name=f"tags_ext_{generate_random_string(length=6)}"
            )
        )
        yield created
        try:
            await remnawave.external_squads.delete_external_squad(str(created.uuid))
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_get_tags(self, remnawave):
        response = await remnawave.external_squads.get_external_squads_tags()
        assert isinstance(response, GetExternalSquadsTagsResponseDto)
        assert isinstance(response.tags, list)

    @pytest.mark.asyncio
    async def test_new_squad_has_empty_tags(self, external_squad):
        assert external_squad.tags == []

    @pytest.mark.asyncio
    async def test_set_tags(self, remnawave, external_squad):
        response = await remnawave.external_squads.set_external_squad_tags(
            SetExternalSquadsTagsRequestDto(uuid=external_squad.uuid, tags=TAGS)
        )

        assert isinstance(response, SetExternalSquadsTagsResponseDto)
        assert response.uuid == external_squad.uuid
        assert sorted(response.tags) == sorted(TAGS)

        fetched = await remnawave.external_squads.get_external_squad_by_uuid(
            str(external_squad.uuid)
        )
        assert sorted(fetched.tags) == sorted(TAGS)


class TestSubpageConfigsTags:
    @pytest.fixture
    async def subpage_config(self, remnawave):
        created = await remnawave.subscription_page_config.create_config(
            CreateSubscriptionPageConfigRequestDto(
                name=f"tags_subpage_{generate_random_string(length=6)}"
            )
        )
        yield created
        try:
            await remnawave.subscription_page_config.delete_config(str(created.uuid))
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_get_tags(self, remnawave):
        response = await remnawave.subscription_page_config.get_subpage_configs_tags()
        assert isinstance(response, GetSubpageConfigsTagsResponseDto)
        assert isinstance(response.tags, list)

    @pytest.mark.asyncio
    async def test_new_config_has_empty_tags(self, subpage_config):
        assert subpage_config.tags == []

    @pytest.mark.asyncio
    async def test_set_tags(self, remnawave, subpage_config):
        response = await remnawave.subscription_page_config.set_subpage_config_tags(
            SetSubpageConfigsTagsRequestDto(uuid=subpage_config.uuid, tags=TAGS)
        )

        assert isinstance(response, SetSubpageConfigsTagsResponseDto)
        assert response.uuid == subpage_config.uuid
        assert sorted(response.tags) == sorted(TAGS)

        fetched = await remnawave.subscription_page_config.get_config_by_uuid(
            str(subpage_config.uuid)
        )
        assert sorted(fetched.tags) == sorted(TAGS)


class TestSubscriptionTemplatesTags:
    @pytest.fixture
    async def template(self, remnawave):
        created = await remnawave.subscriptions_template.create_template(
            CreateSubscriptionTemplateRequestDto(
                name=f"tags_tpl_{generate_random_string(length=6)}",
                template_type=TemplateType.SINGBOX,
            )
        )
        yield created
        try:
            await remnawave.subscriptions_template.delete_template(str(created.uuid))
        except NotFoundError:
            pass

    @pytest.mark.asyncio
    async def test_get_tags(self, remnawave):
        response = await remnawave.subscriptions_template.get_subscription_templates_tags()
        assert isinstance(response, GetSubscriptionTemplatesTagsResponseDto)
        assert isinstance(response.tags, list)

    @pytest.mark.asyncio
    async def test_new_template_has_empty_tags(self, template):
        assert template.tags == []

    @pytest.mark.asyncio
    async def test_set_tags(self, remnawave, template):
        response = await remnawave.subscriptions_template.set_subscription_template_tags(
            SetSubscriptionTemplatesTagsRequestDto(uuid=template.uuid, tags=TAGS)
        )

        assert isinstance(response, SetSubscriptionTemplatesTagsResponseDto)
        assert response.uuid == template.uuid
        assert sorted(response.tags) == sorted(TAGS)

        fetched = await remnawave.subscriptions_template.get_template_by_uuid(
            str(template.uuid)
        )
        assert sorted(fetched.tags) == sorted(TAGS)

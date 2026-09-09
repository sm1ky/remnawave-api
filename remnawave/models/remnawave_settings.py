from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class PasskeySettings(BaseModel):
    """Passkey authentication settings"""
    enabled: bool
    rp_id: str | None = Field(alias="rpId")
    origin: str | None


class GitHubOAuth2Settings(BaseModel):
    """GitHub OAuth2 settings"""
    enabled: bool
    client_id: str | None = Field(alias="clientId")
    client_secret: str | None = Field(alias="clientSecret")
    allowed_emails: List[str] = Field(alias="allowedEmails")


class PocketIdOAuth2Settings(BaseModel):
    """PocketID OAuth2 settings"""
    enabled: bool
    client_id: str | None = Field(alias="clientId")
    client_secret: str | None = Field(alias="clientSecret")
    frontend_domain: str | None = Field(None, alias="frontendDomain")
    plain_domain: str | None = Field(alias="plainDomain")
    allowed_emails: List[str] = Field(alias="allowedEmails")


class YandexOAuth2Settings(BaseModel):
    """Yandex OAuth2 settings"""
    enabled: bool
    client_id: str | None = Field(alias="clientId")
    client_secret: str | None = Field(alias="clientSecret")
    allowed_emails: List[str] = Field(alias="allowedEmails")


class KeycloakOAuth2Settings(BaseModel):
    """Keycloak OAuth2 settings"""
    enabled: bool
    realm: str | None
    client_id: str | None = Field(alias="clientId")
    client_secret: str | None = Field(alias="clientSecret")
    frontend_domain: str | None = Field(alias="frontendDomain")
    keycloak_domain: str | None = Field(alias="keycloakDomain")
    allowed_emails: List[str] = Field(alias="allowedEmails")


class GenericOAuth2Settings(BaseModel):
    """Generic OAuth2 settings"""
    enabled: bool
    client_id: str | None = Field(alias="clientId")
    client_secret: str | None = Field(alias="clientSecret")
    with_pkce: bool = Field(alias="withPkce")
    authorization_url: str | None = Field(alias="authorizationUrl")
    token_url: str | None = Field(alias="tokenUrl")
    frontend_domain: str | None = Field(alias="frontendDomain")
    allowed_emails: List[str] = Field(alias="allowedEmails")


class TelegramOAuth2Settings(BaseModel):
    """Telegram OAuth2 settings"""
    enabled: bool
    client_id: str | None = Field(alias="clientId")
    client_secret: str | None = Field(alias="clientSecret")
    allowed_ids: List[str] = Field(alias="allowedIds")
    frontend_domain: str | None = Field(alias="frontendDomain")


class OAuth2Settings(BaseModel):
    """OAuth2 authentication settings"""
    github: GitHubOAuth2Settings
    pocketid: PocketIdOAuth2Settings
    yandex: YandexOAuth2Settings
    keycloak: Optional[KeycloakOAuth2Settings] = None
    generic: Optional[GenericOAuth2Settings] = None
    telegram: Optional[TelegramOAuth2Settings] = None


class TelegramAuthSettings(BaseModel):
    """Telegram authentication settings"""
    enabled: bool
    client_id: str | None = Field(alias="clientId")
    client_secret: str | None = Field(alias="clientSecret")
    allowed_ids: List[str] = Field(alias="allowedIds")
    frontend_domain: str | None = Field(alias="frontendDomain")


class PasswordSettings(BaseModel):
    """Password authentication settings"""
    enabled: bool


class BrandingSettings(BaseModel):
    """Branding settings"""
    title: Optional[str] = None
    logo_url: Optional[HttpUrl] = Field(None, alias="logoUrl")


class RemnawaveSettingsData(BaseModel):
    """Remnawave settings data"""
    passkey_settings: PasskeySettings | None = Field(alias="passkeySettings")
    oauth2_settings: OAuth2Settings | None = Field(alias="oauth2Settings")
    password_settings: Optional[PasswordSettings] = Field(None, alias="passwordSettings")
    branding_settings: Optional[BrandingSettings] = Field(None, alias="brandingSettings")


class GetRemnawaveSettingsResponseDto(RemnawaveSettingsData):
    """Get Remnawave settings response"""
    pass


class UpdateRemnawaveSettingsRequestDto(BaseModel):
    """Update Remnawave settings request"""
    passkey_settings: Optional[PasskeySettings] = Field(None, serialization_alias="passkeySettings")
    oauth2_settings: Optional[OAuth2Settings] = Field(None, serialization_alias="oauth2Settings")
    password_settings: Optional[PasswordSettings] = Field(None, serialization_alias="passwordSettings")
    branding_settings: Optional[BrandingSettings] = Field(None, serialization_alias="brandingSettings")


class UpdateRemnawaveSettingsResponseDto(RemnawaveSettingsData):
    """Update Remnawave settings response"""
    pass
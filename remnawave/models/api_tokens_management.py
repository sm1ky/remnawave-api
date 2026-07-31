from datetime import datetime
from typing import Annotated, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints

from remnawave.enums import Scope


class CreateApiTokenRequestDto(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=30)] = Field(
        serialization_alias="name"
    )
    expires_in_days: float = Field(serialization_alias="expiresInDays", ge=1)
    scopes: List[str] = Field(
        default_factory=lambda: [Scope.WILDCARD],
        description='API token scopes. Pass :class:`remnawave.enums.Scope` members (or raw strings). Defaults to ["*"] (full access). See GET /api/tokens/scopes for the catalog.',
    )

    def __init__(self, **data):
        # Backward compatibility: `token_name` was renamed to `name` in v2.8.0
        if "token_name" in data and "name" not in data:
            data["name"] = data.pop("token_name")
        super().__init__(**data)


class CreateApiTokenResponseData(BaseModel):
    uuid: UUID
    name: str
    expire_at: datetime = Field(alias="expireAt")
    scopes: List[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    token: str


class CreateApiTokenResponseDto(CreateApiTokenResponseData):
    pass


class DeleteApiTokenResponseDto(BaseModel):
    is_deleted: bool = Field(..., alias="isDeleted")


class ApiTokenDto(BaseModel):
    uuid: UUID
    name: str
    expire_at: datetime = Field(..., alias="expireAt")
    scopes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    @property
    def token_name(self) -> str:
        """Backward compatibility property (renamed to `name` in v2.8.0)"""
        return self.name


class DocsInfoDto(BaseModel):
    enabled: bool = Field(..., alias="enabled")
    scalar_path: Optional[str] = Field(None, alias="scalarPath")
    swagger_path: Optional[str] = Field(None, alias="swaggerPath")

    @property
    def is_docs_enabled(self) -> bool:
        """Backward compatibility property (renamed to `enabled` in v2.8.0)"""
        return self.enabled


class FindAllApiTokensResponseData(BaseModel):
    tokens: List[ApiTokenDto] = Field(..., alias="tokens")

    @property
    def api_keys(self) -> List[ApiTokenDto]:
        """Backward compatibility property (renamed to `tokens` in v2.8.0)"""
        return self.tokens


class FindAllApiTokensResponseDto(FindAllApiTokensResponseData):
    pass


class ApiTokenScopeEndpointDto(BaseModel):
    key: str
    kind: Literal["read", "write"]
    method: str
    path: str
    description: str


class ApiTokenScopeResourceDto(BaseModel):
    resource: str
    resource_scopes: List[str] = Field(..., alias="resourceScopes")
    endpoints: List[ApiTokenScopeEndpointDto]


class GetApiTokenScopesResponseData(BaseModel):
    wildcard: str
    resources: List[ApiTokenScopeResourceDto]


class GetApiTokenScopesResponseDto(GetApiTokenScopesResponseData):
    pass

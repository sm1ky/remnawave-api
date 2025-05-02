from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CreateApiTokenRequestDto(BaseModel):
    token_name: str = Field(serialization_alias="tokenName")
    token_description: Optional[str] = Field(
        None, serialization_alias="tokenDescription"
    )


class CreateApiTokenResponseDto(BaseModel):
    token: str
    uuid: str


class DeleteApiTokenResponseDto(BaseModel):
    response: bool


class ApiTokenDto(BaseModel):
    uuid: str
    token: str
    token_name: str = Field(..., alias="tokenName")
    token_description: Optional[str] = Field(None, alias="tokenDescription")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class DocsInfoDto(BaseModel):
    is_docs_enabled: bool = Field(..., alias="isDocsEnabled")
    scalar_path: Optional[str] = Field(None, alias="scalarPath")
    swagger_path: Optional[str] = Field(None, alias="swaggerPath")


class FindAllApiTokensResponseDto(BaseModel):
    api_keys: List[ApiTokenDto] = Field(..., alias="apiKeys")
    docs: DocsInfoDto

    model_config = ConfigDict(populate_by_name=True)
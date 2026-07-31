from pydantic import BaseModel, Field


class NodeSecretKeyData(BaseModel):
    secret_key: str = Field(alias="secretKey")


class GetNodeSecretKeyResponseDto(BaseModel):
    secret_key: str = Field(alias="secretKey")

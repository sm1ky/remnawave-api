"""Metadata management models for Users and Nodes"""

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GetUserMetadataResponseDto(BaseModel):
    """Get user metadata response"""
    metadata: Optional[Dict[str, Any]] = None


class UpsertUserMetadataRequestBodyDto(BaseModel):
    """Request body for upserting user metadata"""
    metadata: Dict[str, Any]


class UpsertUserMetadataResponseDto(BaseModel):
    """Response for upserting user metadata"""
    metadata: Dict[str, Any]


class GetNodeMetadataResponseDto(BaseModel):
    """Get node metadata response"""
    metadata: Optional[Dict[str, Any]] = None


class UpsertNodeMetadataRequestBodyDto(BaseModel):
    """Request body for upserting node metadata"""
    metadata: Dict[str, Any]


class UpsertNodeMetadataResponseDto(BaseModel):
    """Response for upserting node metadata"""
    metadata: Dict[str, Any]

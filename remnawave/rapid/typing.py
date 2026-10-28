from typing import TypeVar

from pydantic import BaseModel
from rapid_api_client.annotations import BaseAnnotation

BA = TypeVar("BA", bound=BaseAnnotation)
BM = TypeVar("BM", bound=BaseModel)
T = TypeVar("T")

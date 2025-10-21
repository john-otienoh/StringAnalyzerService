from pydantic import BaseModel
from datetime import datetime


class stringProperty(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: dict


class stringCreate(BaseModel):
    value: str


class stringResponse(BaseModel):
    id: str
    value: str
    properties: stringProperty
    created_at: datetime
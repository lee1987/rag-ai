from pydantic import BaseModel

from enum import Enum


class OpenAIRoleEnum(str, Enum):
    system = 'system'
    user = 'user'
    assistant = 'assistant'


class Conversation(BaseModel):
    ID: int
    Content: str
    Role: OpenAIRoleEnum

from pydantic import BaseModel


class Prompt(BaseModel):
    input: str

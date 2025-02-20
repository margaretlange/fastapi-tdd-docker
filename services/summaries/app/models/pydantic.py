# project/app/models/pydantic.py

from typing import Annotated
from pydantic import AnyHttpUrl, BaseModel, StringConstraints


# summary schema
class SummaryPayloadSchema(BaseModel):
    url: AnyHttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


# user schema add here
class UserPayloadSchema(BaseModel):
    username: Annotated[str, StringConstraints(max_length=50)]


class UserResponseSchema(UserPayloadSchema):
    id: int

# project/app/models/pydantic.py

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class SummaryPayloadSchema(BaseModel):
    user_id: int
    query: Annotated[
        str,
        Field(
            pattern=r".*\?$",
            description="Query must be a question ending with a question mark.",
        ),
    ]


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int
    user_id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


class UserPayloadSchema(BaseModel):
    username: Annotated[str, StringConstraints(max_length=50)]


class UserResponseSchema(UserPayloadSchema):
    id: int

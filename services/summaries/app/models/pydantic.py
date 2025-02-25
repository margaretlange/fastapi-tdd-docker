# project/app/models/pydantic.py

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


# summary schema
class SummaryPayloadSchema(BaseModel):
    query: Annotated[
        str,
        Field(
            pattern=r".*\?$",
            description="Query must be a question ending with a question mark.",
        ),
    ]


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


# user schema add here
class UserPayloadSchema(BaseModel):
    username: Annotated[str, StringConstraints(max_length=50)]


class UserResponseSchema(UserPayloadSchema):
    id: int

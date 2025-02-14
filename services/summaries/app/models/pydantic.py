# project/app/models/pydantic.py


from pydantic import AnyHttpUrl, BaseModel


# summary schema
class SummaryPayloadSchema(BaseModel):
    url: AnyHttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


# user schema add here

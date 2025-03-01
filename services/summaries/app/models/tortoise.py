# project/app/models/tortoise.py
from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    username = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    text_summaries = fields.ReverseRelation["TextSummary"]

    def __str__(self):
        return self.username


class TextSummary(models.Model):
    query = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    user_id = fields.ForeignKeyField("models.User", related_name="text_summaries")

    def __str__(self):
        return self.query


Tortoise.init_models(["app.models.tortoise"], "models")
SummarySchema = pydantic_model_creator(TextSummary)  # new
UserSchema = pydantic_model_creator(User)

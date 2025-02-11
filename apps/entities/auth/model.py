from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class User(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=15)
    user_name = fields.CharField(max_length=20)
    password = fields.CharField(max_length=256)


User_Pydantic = pydantic_model_creator(User)

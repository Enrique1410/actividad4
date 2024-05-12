from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, min_length=1)
    email = fields.CharField(max_length=50, min_length=1)
    password = fields.CharField(max_length=300, min_length=1)
    auth_token = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "users"

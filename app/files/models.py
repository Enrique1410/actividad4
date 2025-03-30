from tortoise.models import Model
from tortoise import fields


class File(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    object_name = fields.CharField(max_length=255)  # MinIO object key
    user_id = fields.IntField(null=True)

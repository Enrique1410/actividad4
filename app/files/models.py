from tortoise import fields
from tortoise.models import Model

class File(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=50, min_length=1)
    content = fields.CharField(max_length=50, min_length=1)

    class Meta:
        table = "files"

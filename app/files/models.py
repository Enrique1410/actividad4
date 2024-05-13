from tortoise import fields
from tortoise.models import Model

class File(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='files')
    description = fields.CharField(max_length=50, min_length=1)
    content = fields.CharField(max_length=50, min_length=1)
    name = fields.CharField(max_length=255)

    class Meta:
        table = "files"

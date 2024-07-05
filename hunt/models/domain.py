from peewee import TextField
from hunt.models.base import BaseModel


class Domain(BaseModel):
    domain = TextField(null=False, unique=True)
    registrar = TextField(null=True)
    tag = TextField(null=True)
    status = TextField(default="N/A")

    class Meta:
        table_name = "domains"

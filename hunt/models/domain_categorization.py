from peewee import TextField, DateTimeField, ForeignKeyField
import datetime
from hunt.models.base import BaseModel
from hunt.models.domain import Domain


class DomainCategorization(BaseModel):
    source = TextField()
    category = TextField()
    checked_at = DateTimeField(default=datetime.datetime.now)
    domain = ForeignKeyField(Domain, backref='categories')

    class Meta:
        table_name = "domaincategorizations"

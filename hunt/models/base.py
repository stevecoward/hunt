from peewee import Model
from hunt import db

class BaseModel(Model):
    class Meta:
        database = db

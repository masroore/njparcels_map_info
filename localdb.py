from peewee import *

db = SqliteDatabase("njpr-quick.db")


class BaseModel(Model):
    class Meta:
        database = db


class PropertyInfo(BaseModel):
    pin = CharField(unique=True, index=True)
    property_location = CharField(null=True)
    additional_lots = CharField(null=True)
    deed_book = CharField(null=True)
    deed_page = CharField(null=True)
    owner_address = CharField(null=True)
    owner_city = CharField(null=True)
    owner_name = CharField(null=True)
    owner_zip = CharField(null=True)
    improvement_value = IntegerField(null=True)
    land_value = IntegerField(null=True)
    net_value = IntegerField(null=True)


def init_db():
    db.connect()
    db.create_tables(
        [PropertyInfo],
    )


def apn_exists(pin: str) -> bool:
    return PropertyInfo.select().where(PropertyInfo.pin == pin).exists()

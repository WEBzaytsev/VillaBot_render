from os import environ
import datetime
from peewee import Model, CharField, DateTimeField, IntegerField, ForeignKeyField, BooleanField,\
    SmallIntegerField, PostgresqlDatabase, AutoField,  BigIntegerField, DateTimeField
from playhouse.db_url import connect

REQUIRED_ENV = ['POSTGRES_DB', 'POSTGRES_USER',
                'POSTGRES_PASSWORD', 'DB_ADDRESS', 'DB_PORT']
for var in REQUIRED_ENV:
    if var not in environ:
        raise EnvironmentError(f"{var} is not set.")

db = PostgresqlDatabase(environ.get('POSTGRES_DB'), user=environ.get('POSTGRES_USER'), password=environ.get('POSTGRES_PASSWORD'),
                        host=environ.get('DB_ADDRESS'), port=environ.get('DB_PORT'), autorollback=True)


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    tgid = BigIntegerField(unique=True)
    # fbid =
    name = CharField(null=True)
    phone = CharField(null=True)
    is_admin = BooleanField(default=False)
    is_rentee = BooleanField(default=False)
    is_renter = BooleanField(default=False)
    # TODO: FOLLOW UP: Recheck each hour and send differences.
    last_search_params = None
    last_search_followup_date = DateTimeField(null=True)
    notifications = BooleanField(default=True)


class Location(BaseModel):
    name = CharField()


class Apartment(BaseModel):
    # TODO: Create user for each unique group from parser
    user = ForeignKeyField(Client, backref='apartments')
    bedrooms = IntegerField()
    location = ForeignKeyField(Location, backref='apartments')
    # defined if from Facebook, overriding user.phone
    phone = CharField(max_length=15, null=True)
    # defined if from Facebook, overriding user.name
    name = CharField(null=True)
    listdate = DateTimeField(default=datetime.datetime.now)
    delistdate = DateTimeField(null=True)
    checkindate = DateTimeField(null=True)
    # probably should keep this on script side, not on database
    source = SmallIntegerField(default=0)
    shortcode = CharField(null=True)
    delisted = BooleanField(default=False)
    deleted = BooleanField(default=False)


class ApartmentMedia(BaseModel):
    apartment = ForeignKeyField(
        Apartment, backref='media', on_delete='CASCADE')
    file_id = CharField()
    # file_type = CharField() # there would be videos in media


class Term(BaseModel):
    termid = AutoField()
    name = CharField()


class PricesTerm(BaseModel):
    apartment = ForeignKeyField(
        Apartment, backref='prices', on_delete='CASCADE')
    term = ForeignKeyField(Term, backref='terms')
    price = IntegerField()


class ClientSearches(BaseModel):
    user = ForeignKeyField(Client, backref='searches')
    last_search_params = None
    last_search_followup_date = DateTimeField(null=True)


class ClientFavorite(BaseModel):
    user = ForeignKeyField(Client, backref='favorites')
    apartment = ForeignKeyField(Apartment)


class Facility(BaseModel):
    facilityid = AutoField()
    name = CharField()


class ApartmentFacility(BaseModel):
    apartment = ForeignKeyField(
        Apartment, backref='facilities', on_delete='CASCADE')
    facility = ForeignKeyField(Facility)


class Appointment(BaseModel):
    apartment = ForeignKeyField(Apartment, backref='appointments')
    client = ForeignKeyField(Client, backref='appointments')
    datestart = DateTimeField(null=True)
    dateend = DateTimeField(null=True)
    canceled = BooleanField(null=True)


class UserActions(BaseModel):
    client = ForeignKeyField(Client, backref='actions')
    action = CharField()
    time = DateTimeField(default=datetime.datetime.now)


class Feedback(BaseModel):
    user = ForeignKeyField(Client, backref='feedback')
    message = CharField()


db.create_tables([Client, Apartment, Appointment, ApartmentMedia, ApartmentFacility,
                 ClientFavorite, ClientSearches, Facility, PricesTerm, Term, Location])

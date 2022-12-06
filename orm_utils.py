from playhouse.shortcuts import model_to_dict, prefetch
from models import Client, Apartment, ApartmentFacility, Facility, ApartmentMedia, Location, PricesTerm, Term
from peewee import fn
from hashids import Hashids

hashids = Hashids("villabot_salt_k39p", 5)


def start_user(tgid):
    client = Client.get_or_none(Client.tgid == tgid)
    if client:
        if not client.name or not client.phone:
            return True
        return False
    client = Client()
    client.tgid = tgid
    client.save()

    return True


def change_pii(tgid, name, phone):
    client = Client.get_or_none(Client.tgid == tgid)
    if client:
        if name:
            client.name = name
        if phone:
            client.phone = phone
        client.save()
        return True
    return False


# These functions currently being rewrited.

def get_apartment(rid):
    query = Apartment.get(Apartment.shortcode == rid)
    return query


def set_appart_facitilies(apartid, apart: list):
    raise NotImplementedError

    # TODO query to "delete" all previous facilties
    for facility in apart:
        facility = ApartmentFacility()
        facility.apartment = Apartment.get(Apartment.tgid == apartid)
        facility.facility = Facility.get(Facility.name == facility)
        facility.save()
    facility.facility = Facility.get(Facility.name == facility)
    facility.save()


def new_apartment(tgid, bedrooms, location, facilitylist, pricelist):
    print(tgid, bedrooms, location, facilitylist)
    apartment = Apartment()
    apartment.user = Client.get(Client.tgid == tgid)
    apartment.bedrooms = bedrooms
    apartment.location = Location.get(Location.name == location)
    apartment.save()
    apartment.shortcode = hashids.encode(apartment.id)
    apartment.save()
    for facility1 in facilitylist:
        print(facility1)
        facility2 = ApartmentFacility()
        facility2.apartment = apartment.id
        facility2.facility = Facility.get(Facility.name == facility1)
        facility2.save()
    print(pricelist)
    for key, value in pricelist.items():
        if value:
            pricesterm = PricesTerm()
            pricesterm.apartment = apartment.id
            pricesterm.term = Term.get(Term.name == key)
            pricesterm.price = value
            pricesterm.save()
    return apartment.id


def set_apartment_media(apartid, fileid):
    media = ApartmentMedia()
    media.apartment = Apartment.get(Apartment.id == apartid)
    media.file_id = fileid
    media.save()


def get_user_apartments(userid, count=10, page=1):
    if userid:
        query = Apartment.select().join(Client).where(Client.tgid == userid)
        data = list(query.dicts())
        print(data)
        #p = prefetch(query,  Apartment, ApartmentFacility, Facility, ApartmentMedia, Location, PricesTerm,Term)
        #
        #returnlist = []
        # for res in p:
        #    return.append(model_to_dict(res, backrefs=True))
        # print(accum)
        if data:
            return data
        return None


def get_apart_prices(apartid, term_str=None):
    if term_str:
        query = PricesTerm.select().where((PricesTerm.apartment == apartid) &
                                          (PricesTerm.term == Term.get(Term.name == term_str)))
        data = list(query.dicts())
        if data:
            return data[0]['price']
    else:
        print(apartid)
        query = PricesTerm.select(PricesTerm, Term).where(
            PricesTerm.apartment == apartid).join(Term)
        data = list(query.dicts())
        print(data)
        if data:
            return data


def get_appart_media(apartid):
    query = ApartmentMedia.select().where(ApartmentMedia.apartment == apartid)
    data = list(query.dicts())
    if data:
        return data


def get_appart_facilities(apartid):
    query = ApartmentFacility.select(ApartmentFacility, Facility).where(
        ApartmentFacility.apartment == apartid).join(Facility)
    data = list(query.dicts())
    returnarray = []
    print(data)
    if data:
        for facility in data:
            returnarray.append(facility['name'])
        return returnarray

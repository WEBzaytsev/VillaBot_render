from aiogram.dispatcher.filters.state import State, StatesGroup


class NewUser(StatesGroup):
    name = State()
    phone = State()


class Menu(StatesGroup):
    main = State()
    change_personal_info = State()
    # appointments = State() # TODO: target
    listed_villas = State()  # TODO: WIP


class NewVilla(StatesGroup):
    """
    term -> location -> pricing  -> bedrooms -> facilities -> media -> checkindate -> preview
    """
    term = State()
    location = State()
    pricing = State()
    bedrooms = State()
    facilities = State()
    media = State()
    checkindate = State()
    preview = State()


class Pricing(StatesGroup):
    DAY = State()
    MONTH = State()
    YEAR = State()


class ChangeVilla(StatesGroup):
    villalist = State()
    villa = State()
    change = State()

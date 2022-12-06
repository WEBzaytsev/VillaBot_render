
from aiogram import types
from orm_utils import get_user_apartments, get_appart_facilities, get_appart_media, get_apart_prices, get_apartment
from aiogram.dispatcher import FSMContext
import keyboards
from aiogram.dispatcher.filters import Text
from misc import dp
import states

# hadnler button -> show text with added willas and their params with inline keyboard with numbers -> after click send info about villa with "Change something" button


POSSIBLE_CHOICES = {'term': {
    "DAY": False,
    "MONTH": False,
    "YEAR": False,
    "_multiple": True,
},
    'location': {
    "CANGGU": False,
    "SEMINYAK": False,
    "ULUWATU": False,
    "UBUD": False,
    "JIMBARAN": False,
    "LAVINA": False,
    "SUKAWATI": False,
    "_multiple": False,
},
    'price': {
    "DAY": None,
    "MONTH": None,
    "YEAR": None
},
    'bedrooms': {'1': False,
                 '2': False,
                 '3': False,
                 '4+': False,
                 "_multiple": False},
    'media': [],
    'checkindate': None,
    'facilities': {'PRIVATEPOOL': False,
                   'SHAREDPOOL': False,
                   'BATHTUBE': False,
                   'KITCHEN': False,
                   'CLEANING': False,
                   'WIFI': False,
                   'AC': False,
                   'LAUNDRY': False,
                   'DISHWASHER': False,
                   'PETFRIENDLY': False,
                   "_multiple": True,
                   },
}


def get_keyboard(userid, page_id: int = 1):
    text = str()
    markup = types.InlineKeyboardMarkup()
    aparts = get_user_apartments(userid=userid, page=page_id)
    if aparts:
        for count, apart in enumerate(aparts):
            if apart['shortcode']:
                print(f"APART: {apart}")
                prices = get_apart_prices(apart['id'])
                facilities = ", ".join(get_appart_facilities(apart['id']))
                pricestext = str()
                if prices:
                    for price in prices:
                            pricestext += f"{price['name']}: {price['price']}\n"
                # TODO: Delisted emoji.
                text += f"""{count}. Bedrooms: {apart['bedrooms']}\nLocation: {apart['location']}\nShortcode: {apart['shortcode']}\nFacilities: {facilities}\nPrices:\n{pricestext}\n"""
                # text += f"""bedrooms: {apart.bedrooms}, prices:\n"""
                # for term in statedata['term']:
                #     if not term.startswith("_"):
                #         if statedata['term'][term]:
                #             text += f'{term} price: {statedata["price"][term] if statedata["price"][term] is not None else "not set"}\n'
                markup.add(
                    types.InlineKeyboardButton(
                        f'{count}',
                        callback_data=keyboards.villalist_cb.new(id=apart['shortcode'], action='view')),
                )

    return text, markup


def format_request(apartid, apart):
#     text = f"""Term: {apart.terms}
# Location: {apart.location}
# Facilities: {apart.facilities}
# Bedrooms: {apart.bedrooms}
# Prices:\n"""
    text = f"""
Bedrooms: {apart.bedrooms}
Prices:\n"""
    # for term in statedata['term']:
    #     if not term.startswith("_"):
    #         if statedata['term'][term]:
    #             text += f'{term} price: {statedata["price"][term] if statedata["price"][term] is not None else "not set"}\n'

    markup = keyboards.villa_keyboard(apartid)

    return text, markup


@dp.callback_query_handler(Text(equals='change_villa', ignore_case=True))
@dp.callback_query_handler(keyboards.villalist_cb.filter(action='list'), state=states.ChangeVilla.villa)
async def process_change(query: types.CallbackQuery):
    print('test')
    text, keyboard = get_keyboard(userid=query.from_user.id, page_id=1)
    print(keyboard)
    if keyboard:
        await query.message.edit_text(text, reply_markup=keyboard)
        await states.ChangeVilla.villalist.set()
    else:
        await query.answer('Nothing added!')


@dp.callback_query_handler(keyboards.villalist_cb.filter(action='view'), state=states.ChangeVilla.villalist)
async def query_view(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.answer()
    if callback_data['action']:
        print(callback_data['action'])

    apartment_id = callback_data['id']

    request = get_apartment(apartment_id)
    if not request:
         return await query.answer('Такой записи не существует!')

    await state.update_data(apartment_id=apartment_id)

    text, markup = format_request(apartment_id, request)
    await query.message.edit_text(text, reply_markup=markup)
    await states.ChangeVilla.change.set()


@dp.callback_query_handler(keyboards.villalist_cb.filter(), state=states.ChangeVilla.change)
async def process_villalist_button(query: types.CallbackQuery, callback_data: dict, state: FSMContext)):
    await query.answer()
    if callback_data['action']:
        await state.update_data(changing = callback_data['action'])

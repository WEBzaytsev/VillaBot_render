from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    KeyboardButton
from aiogram.utils.callback_data import CallbackData

choicer_cb = CallbackData('toggle', 'state', 'button')
pager_cb = CallbackData('page', 'state', 'button')
price_cb = CallbackData('price', 'action', 'term')
villalist_cb = CallbackData('villa', 'id', 'action')

main_menu = InlineKeyboardMarkup(row_width=1) \
    .add(InlineKeyboardButton('📥 Add villa', callback_data='add_villa')) \
    .add(InlineKeyboardButton('👤 Fill out contact information', callback_data='change_pii'))\
    # WIP: .add(InlineKeyboardButton('✏ Change villa info', callback_data='change_villa'))\
    # TODO: .add(InlineKeyboardButton('🙋 Feedback', callback_data='feedback'))\

search_menu = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) \
    .add(KeyboardButton("Main menu"))

remove_kb = ReplyKeyboardRemove()


def villa_keyboard(apart_id):
    markup = InlineKeyboardMarkup(row_width=2)\
        .add(InlineKeyboardButton('Change term', callback_data=villalist_cb.new(
            id=apart_id, action='term')))\
        .add(InlineKeyboardButton('Change location', callback_data=villalist_cb.new(
            id=apart_id, action='location')))\
        .add(InlineKeyboardButton('Change price', callback_data=villalist_cb.new(
            id=apart_id, action='price')))\
        .add(InlineKeyboardButton('Change bedrooms', callback_data=villalist_cb.new(
            id=apart_id, action='bedrooms')))\
        .add(InlineKeyboardButton('Change facilities', callback_data=villalist_cb.new(
            id=apart_id, action='facilities')))\
        .add(InlineKeyboardButton('Change photos', callback_data=villalist_cb.new(
            id=apart_id, action='photos')))

    return markup

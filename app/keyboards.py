from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database.scripts.db import Data

db = Data('database/bgpu.db')

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🫶🏻Меры поддержки')],
    [KeyboardButton(text='📋Контактная информация и образцы заявления')],
    [KeyboardButton(text='🏠Клуб молодых семей БГПУ «Очаг»')],
    [KeyboardButton(text='❓Мы стали молодой семьей, что дальше?')],
    [KeyboardButton(text='✏️Вопрос-ответ')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Меню ниже')

support_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='👩‍❤️‍👨Меры поддержки молодых семей')],
    [KeyboardButton(text='🪖Меры поддержки участников СВО')],
    [KeyboardButton(text='👨‍🦽Меры поддержки детей сирот и инвалидов')],
    [KeyboardButton(text='⬅️В главное меню')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Меню ниже')

level_support = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='️🏛БГПУ')],
    [KeyboardButton(text='🗺Амурская область')],
    [KeyboardButton(text='⬅️В главное меню')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Меню ниже')

contacts_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🏫БГПУ')],
    [KeyboardButton(text='🌏Амурская область')],
    [KeyboardButton(text='📑Образцы заявлений')],
    [KeyboardButton(text='⬅️В главное меню')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Меню ниже')

club_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='ℹ️О клубе')],
    [KeyboardButton(text='👫Мероприятия и встречи')],
    [KeyboardButton(text='📞Контакты')],
    [KeyboardButton(text='⬅️В главное меню')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Меню ниже')

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='👮🏻‍♂️Администраторы')],
    [KeyboardButton(text='❓Ответить на вопрос')],
    [KeyboardButton(text='⬅️В главное меню')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Меню ниже')

registration_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Форма регистрации", callback_data="contacts", url='https://forms.yandex.ru/u/67a05475e010db29150fbb49/')]
])

cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отложить ответ на вопрос", callback_data="cancel")]
])

async def inline_admins():
    keyboard = InlineKeyboardBuilder()
    db.get_all_admins()
    for admin in db.data:
        keyboard.add(InlineKeyboardButton(text=admin[0], callback_data=f'user_id: {admin[0]}'))
    keyboard.add(InlineKeyboardButton(text='Добавить', callback_data='append'))
    return keyboard.adjust(1).as_markup()

async def inline_questions():
    keyboard = InlineKeyboardBuilder()
    db.get_all_questions_without_answer()
    for question in db.data:
        keyboard.add(InlineKeyboardButton(text=question[3], callback_data=f'id_question: {question[0]}'))
    return keyboard.adjust(1).as_markup()
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='👩‍❤️‍👨Меры поддержки молодых семей')],
    [KeyboardButton(text='📋Контактная информация и образцы заявления')],
    [KeyboardButton(text='🏠Клуб молодых семей БГПУ «Очаг»')],
    [KeyboardButton(text='❓Мы стали молодой семьей, что дальше?')],
    [KeyboardButton(text='✏️Вопрос-ответ')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Меню ниже')

support_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='️🏛БГПУ.')],
    [KeyboardButton(text='🗺Амурская область.')],
    [KeyboardButton(text='⬅️В главное меню')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Меню ниже')

contacts_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='️🏛БГПУ')],
    [KeyboardButton(text='🗺Амурская область')],
    [KeyboardButton(text='📑Образцы заявлений')],
    [KeyboardButton(text='⬅️В главное меню')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Меню ниже')

club_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='️ℹ️О клубе')],
    [KeyboardButton(text='👫Мероприятия и встречи')],
    [KeyboardButton(text='⬅️В главное меню')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Меню ниже')


admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить админа')],
    [KeyboardButton(text='👫Мероприятия и встречи')],
    [KeyboardButton(text='⬅️В главное меню')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Меню ниже')

registration_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Форма регистрации", callback_data="contacts", url='new.bgpu.ru')]
])

# async def inline_subscribes():
#     keyboard = InlineKeyboardBuilder()
#     subscription = read_config()["newsletter"]['subscription']
#     for user in subscription:
#         keyboard.add(InlineKeyboardButton(text=user, url=subscription[user]))
#     keyboard.add(InlineKeyboardButton(text='Проверить подписки и подписаться на рассылку', callback_data='check'))
#     return keyboard.adjust(1).as_markup()
#
#
# async def inline_admins():
#     keyboard = InlineKeyboardBuilder()
#     for user in read_config()["Admins"]:
#         keyboard.add(InlineKeyboardButton(text=user, callback_data=f'user: {user}'))
#     keyboard.add(InlineKeyboardButton(text='Добавить', callback_data='append'))
#     return keyboard.adjust(1).as_markup()
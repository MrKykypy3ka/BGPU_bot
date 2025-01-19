from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.keyboards as kb


router = Router()
scheduler = AsyncIOScheduler()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(
        f"""Привет {message.from_user.username}! На связи бот @careBGPUbot
Я готов помочь тебе.""",
        reply_markup=kb.main_keyboard)


@router.message(F.text == '👩‍❤️‍👨Меры поддержки молодых семей')
async def set_message_list(message: Message):
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.support_keyboard)

@router.message(F.text == '📋Контактная информация и образцы заявления')
async def set_message_list(message: Message):
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.contacts_keyboard)

@router.message(F.text == '🏠Клуб молодых семей БГПУ «Очаг»')
async def set_message_list(message: Message):
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.club_keyboard)

@router.message(F.text == '❓Мы стали молодой семьей, что дальше?')
async def set_message_list(message: Message):
    await message.answer(text="Регистрация семьи в системе БГПУ", reply_markup=kb.registration_keyboard)

@router.message(F.text == '✏️Вопрос-ответ')
async def set_message_list(message: Message):
    await message.answer(text="Задайте свой вопрос (по умолчанию вопрос анонимный, если хотите себя обозначить, представитесь и укажите свою группу)")


@router.message(F.text == '⬅️В главное меню')
async def set_message_list(message: Message):
    await message.answer(text="Служба заботы🤗", reply_markup=kb.main_keyboard)

# @router.message(F.text.lower() == 'admin')
# async def admin_menu(message: Message):
#     if message.from_user.username in read_config()["Admins"]:
#         await message.answer(f'Для изменения',
#                              reply_markup=kb.admin_keyboard)
#     else:
#         await message.answer(f'Ты не админ😡')
#
# @router.callback_query(F.data.startswith('user'))
# async def del_admin(callback: CallbackQuery):
#     data = read_config()
#     if callback.data.split(": ")[1] not in ["Mrkykypy3a", "lilith_sl"]:
#         data["Admins"].remove(callback.data.split(": ")[1])
#         write_config(data)
#         await callback.message.answer(f'Админ удёлён', reply_markup=await kb.inline_admins())
#     else:
#         await callback.message.answer(f'Их нельзя удалять!', reply_markup=await kb.inline_admins())
#
# @router.callback_query(F.data == 'append')
# async def write_admin(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(Admin.login)
#     await callback.message.answer("Введите логин нового админа:")
#
# @router.message(Admin.login)
# async def add_admin(message: Message, state: FSMContext):
#     await state.update_data(login=message.text)
#     data = read_config()
#     login = await state.get_data()
#     data["Admins"].append(login["login"])
#     write_config(data)
#     await state.clear()
#     await message.answer(f'Админ добавлен', reply_markup=await kb.inline_admins())
#
# @router.message(Newsletter.subscription)
# async def write_link(message: Message, state: FSMContext):
#     await state.update_data(subscription=message.text)
#     await state.set_state(Newsletter.link)
#     await message.answer("Введите ссылку на материалы:")
#
#
# @router.message(Newsletter.link)
# async def write_link(message: Message, state: FSMContext):
#     await state.update_data(link=message.text)
#     await state.set_state(Newsletter.data)
#     await message.answer("""Введите дату рассылки:\n
# Формат даты (МСК): Год Месяц День Час Минуты""")
#
#
# @router.message(Newsletter.data)
# async def edit_message_list(message: Message, state: FSMContext):
#     await state.update_data(date=message.text)
#     config = read_config()
#     data = await state.get_data()
#     try:
#         temp = dict()
#         scheduler.remove_all_jobs()
#         scheduler.add_job(send_newsletter_everyone, 'date', run_date=str(custom_date))
#         await message.answer(f'Рассылка настроена', reply_markup=kb.admin_keyboard)
#     except Exception as e:
#         print(e)
#         await message.answer('Некорректные данные')
#     await state.clear()
#
# @router.message(People.login)
# async def send_newsletter(message: Message, state: FSMContext):
#     scheduler.add_job(send_newsletter_one, 'date',
#                       run_date=str(datetime.now() + timedelta(seconds=5)),
#                       args=[message.text])
#     await message.answer(f"""Через 5 секунд придёт рассылка""")
#     await state.clear()


# @router.message()
# async def handle_unmatched_message(message: Message):
#     await message.answer("Извините, я не понимаю это сообщение.", reply_markup=kb.main_keyboard)

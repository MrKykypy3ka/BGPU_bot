from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.keyboards as kb
from app.states import Admin, Question
from database.scripts.db import Data

router = Router()
scheduler = AsyncIOScheduler()
db = Data('database/bgpu.db')


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
async def edit_message_list(message: Message, state: FSMContext):
    await state.set_state(Question.text)
    await message.answer(text="Задайте свой вопрос")

@router.message(Question.text)
async def add_question(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Question.user)
    await message.answer('Как вас зовут? (если хотите задать анонимный вопрос, напишите «Аноним»)')

@router.message(Question.user)
async def add_question(message: Message, state: FSMContext):
    await state.update_data(user=message.text)
    data = await state.get_data()
    db.add_question(user_id=message.from_user.id, user=data['user'], text=data['text'])
    await message.answer('Спасибо за Ваш вопрос! Мы постараемся ответить на него как можно скорее🤗')
    await message.bot.send_message(text=f"Кто-то задал новый вопрос", chat_id='1425132540')
    await state.clear()

@router.message(F.text == '⬅️В главное меню')
async def set_message_list(message: Message):
    await message.answer(text="Служба заботы🤗", reply_markup=kb.main_keyboard)

@router.message(F.text.lower() == 'admin')
async def admin_menu(message: Message):
    db.get_all_admins()
    if message.from_user.username in [username[0] for username in db.data]:
        await message.answer(f'Добро пожаловать {message.from_user.username}',
                             reply_markup=kb.admin_keyboard)
    else:
        await message.answer(f'Ты не админ😡')

@router.message(F.text == '👮🏻‍♂️Администраторы')
async def set_message_list(message: Message):
    await message.answer(f'Администраторы (Нажмите чтобы удалить):', reply_markup=await kb.inline_admins())

@router.message(F.text == '❓Ответить на вопрос')
async def set_message_list(message: Message):
    await message.answer(f'Список вопросов которые ждут ответа:', reply_markup=await kb.inline_questions())

@router.callback_query(F.data.startswith('user'))
async def del_admin(callback: CallbackQuery):
    if callback.data.split(": ")[1] != "Mrkykypy3a":
        db.delete_admin(username=callback.data.split(": ")[1])
        await callback.message.answer(f'Админ удёлён', reply_markup=await kb.inline_admins())
    else:
        await callback.message.answer(f'Их нельзя удалять!', reply_markup=await kb.inline_admins())

@router.callback_query(F.data == 'append')
async def write_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.login)
    await callback.message.answer("Введите логин нового админа:")

@router.message(Admin.login)
async def add_admin(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    username = await state.get_data()
    print(username['login'])
    db.add_admins(username=username['login'])
    await state.clear()
    await message.answer(f'Админ добавлен', reply_markup=await kb.inline_admins())

@router.message()
async def handle_unmatched_message(message: Message):
    await message.answer("Извините, я не понимаю это сообщение.", reply_markup=kb.main_keyboard)

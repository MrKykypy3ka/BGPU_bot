from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.keyboards as kb
from app.states import Admin, Question, Answer, Keyboard
from database.scripts.db import Data

router = Router()
scheduler = AsyncIOScheduler()
db = Data('database/bgpu.db')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(
        f"""Привет {message.from_user.username}! На связи бот @ZabotaBGPUbot
Я готов помочь тебе.""",
        reply_markup=kb.main_keyboard)

@router.message(F.text == '🫶🏻Меры поддержки')
async def menu_support(message: Message):
    await message.answer(text="Выберите вид поддержки:", reply_markup=kb.support_keyboard)

@router.message(F.text == '👩‍❤️‍👨Меры поддержки молодых семей')
async def support_young_family(message: Message, state: FSMContext):
    await state.update_data(keyboard='young')
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.level_support)

@router.message(F.text == '🪖Меры поддержки участников СВО')
async def support_veterans(message: Message, state: FSMContext):
    await state.update_data(keyboard='veteran')
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.level_support)

@router.message(F.text == '👨‍🦽Меры поддержки детей сирот и инвалидов')
async def support_disabilities(message: Message, state: FSMContext):
    await state.update_data(keyboard='disabilities')
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.level_support)


@router.message(F.text == '️🏛БГПУ')
async def support_BGPU(message: Message, state: FSMContext):
    data = await state.get_data()
    if data['keyboard'] == 'young':
        print('young')
    elif data['keyboard'] == 'veteran':
        print('veteran')
    elif data['keyboard'] == 'disabilities':
        print('disabilities')
    await state.clear()

@router.message(F.text == '🗺Амурская область')
async def support_BGPU(message: Message, state: FSMContext):
    data = await state.get_data()
    if data['keyboard'] == 'young':
        print('young')
    elif data['keyboard'] == 'veteran':
        print('veteran')
    elif data['keyboard'] == 'disabilities':
        print('disabilities')
    await state.clear()

@router.message(F.text == '📋Контактная информация и образцы заявления')
async def menu_contacts_and_documents(message: Message):
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.contacts_keyboard)

@router.message(F.text == '🏠Клуб молодых семей БГПУ «Очаг»')
async def menu_club_ochag(message: Message):
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.club_keyboard)

@router.message(F.text == 'ℹ️О клубе')
async def club_info(message: Message):
    await message.answer_document(document=FSInputFile(path='data/files/Ochag/info.pdf'))

@router.message(F.text == '👫Мероприятия и встречи')
async def club_events(message: Message):
    await message.answer_document(document=FSInputFile(path='data/files/Ochag/events.pdf'))

@router.message(F.text == '📞Контакты')
async def club_contacts(message: Message):
    await message.answer_document(document=FSInputFile(path='data/files/Ochag/contacts.pdf'))

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

@router.callback_query(F.data.startswith('user_id'))
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
    db.add_admins(username=username['login'])
    await state.clear()
    await message.answer(f'Админ добавлен', reply_markup=await kb.inline_admins())

@router.message(F.text == 'cancel')
async def close_FSM(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f"""Отправка ответа отменена""", reply_markup=kb.admin_keyboard)

@router.callback_query(F.data.startswith('id_question'))
async def write_answer(callback: CallbackQuery, state: FSMContext):
    db.get_question(id_question=callback.data.split(": ")[1])
    await state.update_data(user=db.data[0])
    await callback.message.answer(f"""
🤔Вопрос от <i>{db.data[0][2]}</i>
<i>Вопрос:</i> {db.data[0][3]}
    
Введите ваш ответ""", reply_markup=kb.cancel_keyboard, parse_mode="HTML")
    await state.set_state(Answer.text)


@router.message(Answer.text)
async def add_answer(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    db.update_question(answer=data['text'], id_question=data['user'][0])
    await message.answer(f'✅Ваш ответ отправлен пользователю - {data['user'][2]}')
    await message.bot.send_message(text=f"""
⭐️Вам пришёл ответ на ваш вопрос⭐️
<i>Ваш вопрос:</i> {data['user'][3]}
<i>Ответ:</i> {data['text']}""", chat_id=data['user'][1],parse_mode='HTML')
    await state.clear()


@router.message()
async def handle_unmatched_message(message: Message):
    await message.answer("Извините, я не понимаю это сообщение.", reply_markup=kb.main_keyboard)

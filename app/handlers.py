from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaDocument
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.keyboards as kb
from app.states import Admin, Question, Answer
from database.scripts.db import Data
from data.labels import *

router = Router()
scheduler = AsyncIOScheduler()
db = Data('database/bgpu.db')

file_cache = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"""Привет {message.from_user.username}! На связи бот @ZabotaBGPUbot
Я готов помочь тебе c получением информации о доступных мерах поддержки для различных групп граждан. Удобно, быстро и понятно!
Выбери пожалуйста один из пунктов меню""",
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
        await message.answer_photo(photo=FSInputFile(path='data/images/young_BSPU.jpg'),
                                   caption=YOUNG_FAMALY,
                                   reply_markup=kb.support_keyboard,
                                   parse_mode='HTML')
        if 'young_BSPU_pdf' in file_cache:
            await message.answer_document(document=file_cache['young_BSPU_pdf'])
        else:
            msg = await message.answer_document(document=FSInputFile(path='data/files/young.pdf'))
            file_cache['young_BSPU_pdf'] = msg.document.file_id
    elif data['keyboard'] == 'veteran':
        await message.answer_photo(photo=FSInputFile(path='data/images/veterans_BSPU.jpg'),
                                   caption=VETERANS,
                                   reply_markup=kb.support_keyboard,
                                   parse_mode='HTML')
        if 'veteran_BSPU_pdf' in file_cache:
            await message.answer_document(document=file_cache['veteran_BSPU_pdf'])
        else:
            msg = await message.answer_document(document=FSInputFile(path='data/files/veterans.pdf'))

            file_cache['veteran_BSPU_pdf'] = msg.document.file_id
    elif data['keyboard'] == 'disabilities':
        await message.answer_photo(photo=FSInputFile(path='data/images/disabilities_BSPU.jpg'),
                                   caption=ORPHANS,
                                   reply_markup=kb.support_keyboard,
                                   parse_mode='HTML')
        if 'orphans_pdf' in file_cache:
            await message.answer_document(document=file_cache['orphans_pdf'])
        else:
            msg = await message.answer_document(document=FSInputFile(path='data/files/orphans.pdf'))
            file_cache['orphans_pdf'] = msg.document.file_id
        await message.answer(text=DISABILITIES)

        if 'disabilities_pdf' in file_cache:
            await message.answer_document(document=file_cache['disabilities_pdf'])
        else:
            msg = await message.answer_document(document=FSInputFile(path='data/files/disabilities.pdf'))
            file_cache['disabilities_pdf'] = msg.document.file_id
    await state.clear()

@router.message(F.text == '🗺Амурская область')
async def support_BGPU(message: Message, state: FSMContext):
    data = await state.get_data()
    if data['keyboard'] == 'young':
        await message.answer_photo(photo=FSInputFile(path='data/images/young_amur.jpg'),
                                   reply_markup=kb.support_keyboard)
    elif data['keyboard'] == 'veteran':
        cache_key = 'veterans_amur_pdf'
        if cache_key in file_cache:
            await message.answer_document(document=file_cache[cache_key])
        else:
            msg = await message.answer_document(document=FSInputFile(path='data/files/veterans_amur.docx'),
                                      reply_markup=kb.support_keyboard)
            file_cache[cache_key] = msg.document.file_id
    elif data['keyboard'] == 'disabilities':
        await message.answer_photo(photo=FSInputFile(path='data/images/disabilities_amur.jpg'),
                                   reply_markup=kb.support_keyboard)
    await state.clear()

@router.message(F.text == '📋Контактная информация и образцы заявления')
async def menu_contacts_and_documents(message: Message):
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.contacts_keyboard)

@router.message(F.text == '🏫БГПУ')
async def contacts_BGPU(message: Message):
    await message.answer_photo(photo=FSInputFile(path='data/images/contacts_BSPU.jpg'),
                               caption=CONTACTS_BSPU,
                               reply_markup=kb.contacts_keyboard,
                               parse_mode='HTML')

@router.message(F.text == '🌏Амурская область')
async def contacts_amur(message: Message):
    await message.answer_photo(photo=FSInputFile(path='data/images/contacts_amur.jpg'),
                               caption=CONTACTS_REGION,
                               reply_markup=kb.contacts_keyboard,
                               parse_mode='HTML')

@router.message(F.text == '📑Образцы заявлений')
async def support_BGPU(message: Message):
    cache_key = 'statements_doc_ids'
    await message.answer_photo(photo=FSInputFile(path='data/images/sample_applications_sq.jpg'))
    if cache_key in file_cache:
        media = [InputMediaDocument(media=file_id) for file_id in file_cache[cache_key]]
        await message.answer_media_group(media)
    else:
        media = [InputMediaDocument(media=FSInputFile(f'data/files/statement/заявление {i}.docx')) for i in range(1, 5)]
        messages = await message.answer_media_group(media)
        file_ids = []
        for msg in messages:
            if msg.document:
                file_ids.append(msg.document.file_id)
        file_cache[cache_key] = file_ids

@router.message(F.text == '🏠Клуб молодых семей БГПУ «Очаг»')
async def menu_club_ochag(message: Message):
    await message.answer(text="Выберите уровень поддержки:", reply_markup=kb.club_keyboard)

@router.message(F.text == 'ℹ️О клубе')
async def club_info(message: Message):
    cache_key = 'info_pdf'
    if cache_key in file_cache:
        await message.answer_document(document=file_cache[cache_key])
    else:
        msg = await message.answer_document(document=FSInputFile(path='data/files/Ochag/info.pdf'))
        file_cache[cache_key] = msg.document.file_id


@router.message(F.text == '👫Мероприятия и встречи')
async def club_events(message: Message):
    if 'club_events_pdf' in file_cache:
        await message.answer_document(document=file_cache['club_events_pdf'])
    else:
        msg = await message.answer_document(document=FSInputFile(path='data/files/Ochag/events.pdf'))
        file_cache['club_events_pdf'] = msg.document.file_id

@router.message(F.text == '📞Контакты')
async def club_contacts(message: Message):
    if 'club_contacts_pdf' in file_cache:
        await message.answer_document(document=file_cache['club_contacts_pdf'])
    else:
        msg = await message.answer_document(document=FSInputFile(path='data/files/Ochag/contacts.pdf'))

        file_cache['club_contacts_pdf'] = msg.document.file_id

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
async def write_question(message: Message, state: FSMContext):
    await state.update_data(user=message.text)
    data = await state.get_data()
    db.add_question(user_id=message.from_user.id, user=data['user'], text=data['text'])
    await message.answer('Спасибо за Ваш вопрос! Мы постараемся ответить на него как можно скорее🤗')
    db.get_all_admins()
    for admin in [username[0] for username in db.data]:
        await message.bot.send_message(text=f"⚠️Кто-то задал новый вопрос", chat_id=admin)
    await state.clear()

@router.message(F.text == '⬅️В главное меню')
async def set_message_list(message: Message):
    await message.answer(text="Служба заботы🤗", reply_markup=kb.main_keyboard)

@router.message(F.text.lower() == 'admin')
async def admin_menu(message: Message):
    db.get_all_admins()
    user_name = message.from_user.username
    if user_name in [username[1] for username in db.data]:
        id_user = message.from_user.id
        db.edit_admin(username=user_name, id_user=id_user)
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
    db.add_admin(username=username['login'])
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
    await message.reply("Извините, я не понимаю это сообщение.", reply_markup=kb.main_keyboard)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from app.database.request import get_application, add_user, get_user, get_whitelist, get_admin
import app.keyboards as kb


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user = await add_user(user_id=message.from_user.id, firstname=message.from_user.first_name, username=message.from_user.username)
    if user is None:
        await message.answer('Произошла ошибка, напишите @nzhasulan')
    
    await message.answer_sticker('CAACAgIAAxkBAAKFQGWaZCD2Tyt8Ry1wfSXMTLqptogUAAI_AAMkcWIaL6pT6Rh9O2c0BA')
    
    if await get_admin(user_id=message.from_user.id):
        await message.answer('Привет, Админ!', reply_markup=kb.main_admin)
    else:
        await message.answer('Привет, Пидор!', reply_markup=kb.main)
        

@router.message(F.text == 'Профиль')
async def profile_selected(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id=user_id)

    await message.answer(f'<b>Профиль пользователя</b>\n\n<i>Имя пользователя: {user.name} ({user.tg_id})</i>\nДата регистраций: {user.date}\nКоличество конвертаций: {user.count_convert}')


@router.message(F.text == 'Конвертировать')
async def create_convert(message: Message):
    if await get_whitelist(user_id=message.from_user.id) is None:
        await message.answer('У вас нет доступа.\n\nКупить доступ – @alexblockone 💎')
        return
    else:
        await message.answer('Выберите вариант конвертаций:', reply_markup=await kb.create_convert())
    

# @router.callback_query(F.data.startswith('application_'))
# async def applications_selected(callback: CallbackQuery):
#     application_id = int(callback.data.split('_')[1])
#     application = await get_application(application_id=application_id)
#     user = await get_user(user_id=application.user_id)
    
#     await callback.message.answer(f'<b>Заявка номер #{application_id}</b>\n\n<i>Имя пользователя: {user.name} ({application.user_id})</i>\nТип конвертации: {application.convert_type}\nДата: {application.date}'
#                                   , reply_markup=kb.application_selected)
#     await callback.answer('')
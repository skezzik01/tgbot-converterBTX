from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.database.request import get_application
from app.config import ADMINS_ID

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    if message.from_user.id in ADMINS_ID:
        await message.answer('Hello, admin!', reply_markup=kb.main_admin)
    await message.answer('Hello, world!', reply_markup=kb.main)
    

@router.message(F.text == 'Подать заявку')
async def create_applications(message: Message):
    await message.answer('Выберите вариант конвертаций:', reply_markup=await kb.create_applications())

@router.message(F.text == 'Заявки')
async def applications(message: Message):
    await message.answer('Выберите заявку:', reply_markup=await kb.applications())
    
    
@router.callback_query(F.data.startswith('application_'))
async def applications_selected(callback: CallbackQuery):
    application_id = int(callback.data.split('_')[1])
    application = await get_application(application_id=application_id)
    
    await callback.message.answer(f'<b>Заявка номер #{application_id}</b>\n\nИмя пользователя: ({application.user_id})\nТип конвертации: {application.convert_type}\nДата: {application.date}')
    await callback.answer('')
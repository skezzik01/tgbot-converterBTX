from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Filter

from app.database.request import get_admins, get_users_ids, delete_user, add_user_whitelist, delete_user_whitelist
import app.keyboards as kb


router = Router()


class Newsletter(StatesGroup):
    message = State()
    confirmation = State()
    
    
class Whitelist(StatesGroup):
    add_userid = State()
    add_confirmation = State()
    del_userid = State()
    del_confirmation = State()


class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [admin for admin in await get_admins()]


@router.message(AdminProtect(), F.text == 'Админ-панель')
async def admin_panel(message: Message):
    await message.answer('Выберите действие:', reply_markup=await kb.admin_panel())
    
    
@router.callback_query(AdminProtect(), F.data == 'notifyEveryone')
async def notifyEveryone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Newsletter.message)
    await callback.message.answer(f'Внимание! Вы хотите сделать рассылку всем пользователям бота! Введите сообщение ниже. Будьте осторожны, сообщение разошлётся моментально.')


@router.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    
    await message.answer('Подождите... начинается рассылка. При большом количестве пользователей это может занять время.')
    
    for user_id in await get_users_ids():
        try:
            await message.send_copy(chat_id=user_id)
        except:
            try:
                await delete_user(user_id)
            except:
                continue
    
    await state.clear()
    await message.answer('Рассылка завершена!')


@router.callback_query(AdminProtect(), F.data == 'whitelist')
async def whitelist(callback: CallbackQuery):
    await callback.message.edit_text('Выберите действие:', reply_markup=await kb.whitelist())
    

@router.callback_query(AdminProtect(), F.data == 'add_whitelist')
async def add_whitelist(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Whitelist.add_userid)
    await callback.message.answer(f'Введите ид пользователя:')
    

@router.message(AdminProtect(), Whitelist.add_userid)
async def add_whitelist_message(message: Message, state: FSMContext):
    await state.update_data(userid=message.text)
    await state.set_state(Whitelist.add_confirmation)
    await message.answer('Подтвердите действие:', reply_markup=kb.confirm_whitelist)
    

@router.message(AdminProtect(), Whitelist.add_confirmation)
async def add_whitelist_confirmation(message: Message, state: FSMContext):
    if message.text == 'Подтвердить':
        try:
            await message.answer('Подождите...')
            user_id = await state.get_data()
            await add_user_whitelist(user_id=user_id)
            await state.clear()
            await message.answer('Добавление в <i>Whitelist</i> прошло успешно!', reply_markup=kb.main_admin)
        except:
            await message.answer('[Error #001] Отпишите @nzhasulan')
    else:
        await state.clear()
        await message.answer('Добавление в <i>Whitelist</i> отменено!', reply_markup=kb.main_admin)
        

@router.callback_query(AdminProtect(), F.data == 'delete_whitelist')
async def delete_whitelist(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Whitelist.del_userid)
    await callback.message.answer(f'Введите ид пользователя:')
    

@router.message(AdminProtect(), Whitelist.del_userid)
async def del_whitelist_message(message: Message, state: FSMContext):
    await state.update_data(userid=message.text)
    await state.set_state(Whitelist.del_confirmation)
    await message.answer('Подтвердите действие:', reply_markup=kb.confirm_whitelist)
    

@router.message(AdminProtect(), Whitelist.del_confirmation)
async def del_whitelist_confirmation(message: Message, state: FSMContext):
    if message.text == 'Подтвердить':
        try:
            await message.answer('Подождите...')
            user_id = await state.get_data()
            await delete_user_whitelist(user_id=user_id)
            await state.clear()
            await message.answer('Удаление из <i>Whitelist</i> прошло успешно!', reply_markup=kb.main_admin)  
        except:
            await message.answer('[Error #002] Отпишите @nzhasulan')      
    else:
        await state.clear()
        await message.answer('Удаление из <i>Whitelist</i> отменено!', reply_markup=kb.main_admin)
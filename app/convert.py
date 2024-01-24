import os
import shutil
import PVRTexLibPy as pvrpy

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()


class Convert(StatesGroup):
    type = State()
    files = State()
    

@router.callback_query(F.data == 'convert_type_btxtopng')
async def convert_type_btxtopng(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type='btxtopng')
    await state.set_state(Convert.files)
    await callback.message.answer('Отправьте файлы для конвертации:', reply_markup=kb.cancel_convert)
    

@router.message(F.text == 'Отмена', Convert.files)
async def cancel_convert(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Операция отменена.')
    

@router.message(Convert.files)
async def convert_files(message: Message, state: FSMContext):
    pass


async def convert_btxtopng():
    pass
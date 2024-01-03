from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.request import get_applications


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Подать заявку")],
], resize_keyboard=True, input_field_placeholder="Выберите действие")


main_admin= ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Подать заявку")],
    [KeyboardButton(text="Заявки")],
    [KeyboardButton(text="Админ-панель")]
], resize_keyboard=True, input_field_placeholder="Выберите действие")


async def applications():
    applications_kb = InlineKeyboardBuilder()
    applications = await get_applications()
    for application in applications:
        applications_kb.add(InlineKeyboardButton(text=f"Заявка #{application.id}", callback_data=f'application_{application.id}'))
    return applications_kb.adjust(2).as_markup()


async def create_applications():
    application_kb = InlineKeyboardBuilder()
    application_kb.add(InlineKeyboardButton(text=".btx -› .png", callback_data=f'convert_type_1'))
    application_kb.add(InlineKeyboardButton(text=".png -› .btx", callback_data=f'convert_type_2'))
    return application_kb.adjust(2).as_markup()
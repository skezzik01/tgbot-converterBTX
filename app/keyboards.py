from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Конвертировать")],
], resize_keyboard=True, input_field_placeholder="Выберите действие")


main_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Конвертировать")],
    [KeyboardButton(text="Админ-панель")]
], resize_keyboard=True, input_field_placeholder="Выберите действие")


confirm_whitelist = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Подтвердить"), KeyboardButton(text="Отмена")],
], resize_keyboard=True, input_field_placeholder="Выберите действие")


cancel_convert = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отмена")],
], resize_keyboard=True, input_field_placeholder="Выберите действие")


async def create_convert():
    convert_kb = InlineKeyboardBuilder()
    convert_kb.add(InlineKeyboardButton(text=".btx -› .png", callback_data=f'convert_type_btxtopng'))
    convert_kb.add(InlineKeyboardButton(text=".png -› .btx", callback_data=f'convert_type_pngtobtx'))
    return convert_kb.adjust(2).as_markup()


async def admin_panel():
    admin_panel_kb = InlineKeyboardBuilder()
    admin_panel_kb.add(InlineKeyboardButton(text="WhiteList", callback_data='whitelist'))
    admin_panel_kb.add(InlineKeyboardButton(text="Очистить файлы пользователей", callback_data='cleaning_files'))
    admin_panel_kb.add(InlineKeyboardButton(text="Оповещение всем пользователям", callback_data='notifyEveryone'))
    return admin_panel_kb.adjust(1).as_markup()


async def whitelist():
    whitelist_kb = InlineKeyboardBuilder()
    whitelist_kb.add(InlineKeyboardButton(text="Добавить в WhiteList", callback_data='add_whitelist'))
    whitelist_kb.add(InlineKeyboardButton(text="Удалить из WhiteList", callback_data='delete_whitelist'))
    return whitelist_kb.adjust(1).as_markup()
    
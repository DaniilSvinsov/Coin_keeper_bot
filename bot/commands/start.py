from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


async def start(message: types.Message) -> None:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.add(
        KeyboardButton(text='Добавить доход'), KeyboardButton(text='Добавить расход')
    )
    menu_builder.row(
        KeyboardButton(text='Получить выписку о движении денежных средств')
    )
    await message.answer('Выберите действие', reply_markup=menu_builder.as_markup(resize_keyboard=True))

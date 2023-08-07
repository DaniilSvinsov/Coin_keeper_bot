import types
from aiogram.filters import *
from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram import types
from aiogram.filters import state
from aiogram import Bot, Dispatcher
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

bot = Bot(token='6528204794:AAHvIrpdEP_HJ5ZwG-saBE7dayhHUIO0Qno')


async def sum_maker(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    return await bot.send_message(chat_id, f'Вы написали: {text}')


async def add_sum(message: types.Message):
    d = ReplyKeyboardBuilder()
    d.add(
        KeyboardButton(text='Зарплата'), KeyboardButton(text='Стипендия')
    )
    d.row(
        KeyboardButton(text='Шабашка'), KeyboardButton(text='Другое')
    )
    await message.answer('Выберите категорию получения заработка', reply_markup=d.as_markup(resize_keyboard=True))


async def choice_add_method(message: types.Message):
    print(message.text)
    return await message.answer('Выберите категорию дохода или добавтьте свою')

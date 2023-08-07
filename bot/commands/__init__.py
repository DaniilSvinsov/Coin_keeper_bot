from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from bot.commands.start import start
from bot.commands.help import help_command
from bot.commands.add_income import add_sum, choice_add_method
from bot.commands.settings import settings_command
from bot.commands.callback_data_states import TestCallbackData
from aiogram import F

__all__ = ['bot_commands', 'register_user_commands']


def register_user_commands(router: Router) -> None:
    router.message.register(start, CommandStart())
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(add_sum, F.text == 'Добавить доход')
    router.message.register(settings_command, Command(commands=['settings']))
    #router.callback_query.register(call_add_func, F.data == 'help')

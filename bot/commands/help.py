from aiogram import types
from aiogram.filters import CommandObject
from bot.commands.bot_commands import bot_commands


async def help_command(message: types.Message, command: CommandObject):
    if command.args:
        for c in bot_commands:
            if c[0] == command.args:
                return await message.answer(f"{c[0]} - {c[1]}\n\n{c[2]}")
            else:
                return await message.answer("Команда не найдена")

    return 'Помощь потом придумаю'

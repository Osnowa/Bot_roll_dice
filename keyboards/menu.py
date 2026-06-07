from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Получить помощь"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        BotCommand(command="/game", description= 'Начать игру')
    ]
    await bot.set_my_commands(main_menu_commands)
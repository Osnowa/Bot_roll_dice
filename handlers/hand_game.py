from aiogram import Router

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from service.serv_user_db import UserService
from database.repository_db import UserRepository
import logging


logger = logging.getLogger(__name__)
router = Router()

class FSMGame(StatesGroup):
    '''Состояния для игры в кости'''
    waiting_for_roll = State() # ожидание броска кубика

    

@router.message(CommandStart(), StateFilter(default_state))
async def start_game(message: Message, state: FSMContext, session: AsyncSession):
    user_rep = UserRepository(session) # передаем сессию в класс с методами работой функции
    user_serv = UserService(user_rep) # передаем методы работа в сервис (помошника в упрощении логики)

    created, user = await user_serv.register(message.from_user.id, message.from_user.username)

    if created:
        await message.answer(f"Рад приветствовать Вас снова, {user.username}")
    else:
        await message.answer(f"Рад приветстовать Вас впервые !")
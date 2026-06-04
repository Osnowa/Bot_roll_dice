from aiogram import Router

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)
router = Router()

class FSMGame(StatesGroup):
    '''Состояния для игры в кости'''
    waiting_for_roll = State() # ожидание броска кубика

    

@router.message(CommandStart(), StateFilter(default_state))
async def start_game(message: Message, state: FSMContext, session: AsyncSession):
    pass
from aiogram import Router

from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from service.serv_user_db import UserService
from service.game_service import Roll_dice
from database.repository_db import UserRepository
from keyboards.keyb_game import get_game_keyboard, roll_dice_keyboard, play_again_keyboard
from db_redis.redis_serv import redis_db
import logging


logger = logging.getLogger(__name__)
router = Router()

class FSMGame(StatesGroup):
    '''Состояния для игры в кости'''
    in_game = State() # ожидание броска кубика

    

@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message, state: FSMContext, session: AsyncSession):
    user_rep = UserRepository(session) # передаем сессию в класс с методами работой функции
    user_serv = UserService(user_rep) # передаем методы работа в сервис (помошника в упрощении логики)

    created, user = await user_serv.register(message.from_user.id, message.from_user.username)

    if created:
        await message.answer(f"Рад приветствовать Вас снова, {user.username}\n"
                             f"Для начала игры 🎮 введите команду /game")
    else:
        await message.answer(f"Рад приветстовать Вас впервые !\n"
                             f"Для начала игры 🎮 введите команду /game")


@router.message(CommandStart(), ~StateFilter(default_state))
async def start_bot(message: Message, state: FSMContext):
    '''Команда для начала игры, если игрок уже в игре'''
    await message.answer(f"Вы уже начали игру, что бы отменить её введите команду /cancel")


@router.message(Command(commands = 'cancel'), StateFilter(default_state))
async def cancel_game(message: Message, state: FSMContext):
    '''Команда для команды cancel вне игры'''
    await message.answer(f"Вы не начали игру, что бы её отменить. Для начала игры введите команду /game")


@router.message(Command(commands = 'cancel'), ~StateFilter(default_state))
async def cancel_game(message: Message, state: FSMContext):
    '''Команда для отмены игры'''
    await message.answer(f"Вы отменили игру.\n Для начала новой введите /game")
    await state.clear()


@router.callback_query(lambda c: c.data == 'play_again', StateFilter(default_state))
@router.message(Command(commands = 'game'), StateFilter(default_state))
async def start_game(event: Message | CallbackQuery, state: FSMContext):
    '''Команда для начала игры'''
    if isinstance(event, Message):
        await event.answer(f"Игры началась! 🎲\n"
                         f"Как вы думаете, Вы выбросите больше опонента ?",
                         reply_markup = get_game_keyboard())
    else:
        await event.message.edit_text(f"Игры началась! 🎲\n"
                         f"Как вы думаете, Вы выбросите больше опонента ?",
                         reply_markup = get_game_keyboard())
    # Перевод игрока в состояние игры
    await state.set_state(FSMGame.in_game)


@router.message(Command(commands = 'game'), ~StateFilter(default_state))
async def start_game(message: Message, state: FSMContext):
    '''Команда для начала новой игры, если игрок уже в игре'''
    await message.answer(f"Вы уже начали игру! 🎲\n"
                         f"Если хотите начать новую игру, отмените текущую командой /cancel")
    

@router.callback_query(lambda c: c.data in ['roll_higher', 'roll_lower', 'roll_equal'], StateFilter(FSMGame.in_game))
async def roll_higher(callback: CallbackQuery, state: FSMContext):
    '''Обработка выбора'''
    roll_1, roll_2 = Roll_dice.roll() # бросок кубика опонента
    choice_game = callback.data # выбор игрока
    # сохранение выбора игрока
    await redis_db.hset(f"game_choise:{callback.from_user.id}",
                          mapping={"choise":f"{choice_game}"}
                        ) # сохраняем выбор игрока в Redis 
    await redis_db.expire(f"game_choise:{callback.from_user.id}", 600) # устанавливаем время жизни ключа 10 минут
    
    # сохранение броска оппонента
    await redis_db.hset(f"opponent_choise:{callback.from_user.id}",
                         mapping={"roll":roll_1 + roll_2}
                        )
    await redis_db.expire(f"opponent_choise:{callback.from_user.id}", 600) # устанавливаем время жизни ключа 10 минут

    await callback.message.edit_text(f"Вы думаете, что выбросите {'больше' if choice_game == 'roll_higher' else 'меньше' if choice_game == 'roll_lower' else 'как у'} опонента!\n"
                          "Ваш опонент бросает кубик...\n"
                          f"Опонент выбросил {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n"
                          f"Ваш черед !",
                          reply_markup = roll_dice_keyboard())


@router.callback_query(lambda c: c.data == 'roll_dice', StateFilter(FSMGame.in_game))
async def roll_dice(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    '''Обработка кнопки бросить кубик и получение результата'''
    roll_1, roll_2 = Roll_dice.roll()
    user_rep = UserRepository(session) # передаем сессию в класс с методами работой функции

    # сохранение броска игрока
    await redis_db.hset(f"game_choise:{callback.from_user.id}",
                         mapping={"roll":roll_1 + roll_2}
                        )
    await redis_db.expire(f"game_choise:{callback.from_user.id}", 120) # устанавливаем время жизни ключа 2 минуты

    roll_oponenta = await redis_db.hget(f"opponent_choise:{callback.from_user.id}", "roll")
    roll_igroka = await redis_db.hget(f"game_choise:{callback.from_user.id}", "roll")
    choise_igroka = await redis_db.hget(f"game_choise:{callback.from_user.id}", "choise")
    
    if (int(roll_igroka) > int(roll_oponenta) and choise_igroka == 'roll_higher') or (int(roll_igroka) < int(roll_oponenta) and choise_igroka == 'roll_lower') or (int(roll_igroka) == int(roll_oponenta) and choise_igroka == 'roll_equal'):
        # логика для базы данных
        await user_rep.update_game_static(callback.from_user.id, 'win')

        await callback.message.edit_text(f"Вы выбросили {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n"
                                    f"Вы победили !"
                                    f"Хоите сыграть еще ?",
                                    reply_markup = play_again_keyboard())
    else:
        # логика для базы данных
        await user_rep.update_game_static(callback.from_user.id, 'lose')

        await callback.message.edit_text(f"Вы выбросили {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n"
                                    f"К сожалению Вы проиграли ( :с \n "
                                    f"Хоите сыграть еще ?",
                                    reply_markup = play_again_keyboard())
    
    await state.clear() # очищаем состояние
    await redis_db.delete(f"game_choise:{callback.from_user.id}") # удаляем ключ для игрока
    await redis_db.delete(f"opponent_choise:{callback.from_user.id}") # удаляем ключ для оппонента


@router.callback_query(lambda c: c.data == 'stop_game', StateFilter(default_state))
async def stop_game(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Спасибо за игру !\n" \
                                  "Для начала новой введите /game")
    await state.clear()
    await redis_db.delete(f"game_choise:{callback.from_user.id}") # удаляем ключ для игрока
    await redis_db.delete(f"opponent_choise:{callback.from_user.id}") # удаляем ключ для оппонента
    



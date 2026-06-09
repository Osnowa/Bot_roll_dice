from aiogram import Router
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database.repository_db import UserRepository
from service.serv_user_db import UserService
from keyboards.keyb_game import start_keyb, get_game_keyboard
from handlers.fsm_hand import FSMGame
import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart(), StateFilter(default_state))
async def start_bot(message: Message, session: AsyncSession):
    user_rep = UserRepository(session) # передаем сессию в класс с методами работой функции
    user_serv = UserService(user_rep) # передаем методы работа в сервис (помошника в упрощении логики)

    # получаем состояние игрока (bool, User, очки)
    created, user, score_user = await user_serv.register(message.from_user.id, message.from_user.username)

    if created:
        logger.info(f"Пользователь {message.from_user.username} найден в базе данных")
        await message.answer(f"Рад приветствовать Вас снова, {user.username}\n"
                             f"Ваши очки: {score_user}\n"
                             f"Для начала игры 🎮 введите команду /game\n"
                             f"Или воспользуйтесь клавиатурой ⌨️",
                             reply_markup=start_keyb())
    else:
        logger.info(f"Пользователь {message.from_user.username} зарегистрирован в базе данных")
        await message.answer(f"Рад приветстовать Вас впервые !\n"
                             f"Ваши очки: {score_user}\n"
                             f"Для начала игры 🎮 введите команду /game"
                             f"Или воспользуйтесь клавиатурой ⌨️",
                             reply_markup=start_keyb())


@router.message(CommandStart(), ~StateFilter(default_state))
async def start_bot(message: Message):
    '''Команда для начала игры, если игрок уже в игре'''
    await message.answer(f"Вы уже начали игру, что бы отменить её введите команду /cancel")

@router.callback_query(lambda c: c.data == 'rules')
@router.message(Command(commands = 'help'))
async def command_help(event: Message | CallbackQuery):
    '''Для команды помощь'''
    if isinstance(event, Message):
        await event.answer(f"Правила игры очень простые.\n"
                         f"В начале Вам выдается 1000 очков.\n"
                         f"Вы можете выбрать, будет ли на Ваших костях очков больше, меньше или столько же, как у оппонента.\n"
                         f"Если Вы угадаете больше или меньше, Ваши очки удваиваются.\n"
                         f"Если угадаете точно, Ваши очки утраиваются.\n"
                         f"При обнулении очков, я пока не придумал =) "
                         )

    elif isinstance(event, CallbackQuery):
        await event.message.edit_text(f"Правила игры очень простые.\n"
                         f"В начале Вам выдается 1000 очков.\n"
                         f"Вы можете выбрать, будет ли на Ваших костях очков больше, меньше или столько же, как у оппонента.\n"
                         f"Если Вы угадаете больше или меньше, Ваши очки удваиваются.\n"
                         f"Если угадаете точно, Ваши очки утраиваются.\n"
                         f"При обнулении очков, я пока не придумал =) ",
                         reply_markup = event.message.reply_markup
                         )
    

@router.callback_query(lambda c: c.data == 'statistic')
@router.message(Command(commands = 'statistic'), StateFilter(default_state))
async def command_statistic(event: Message| CallbackQuery, session: AsyncSession):
    '''Команда для команды статистика вне игры'''
    user_rep = UserRepository(session)
    us_st = await user_rep.get_static(event.from_user.id) 

    if isinstance(event, Message):
        await event.answer(f"Ваша статистика:\n"
                         f"Ваши очки {us_st.u_score.score}\n"
                         f"Всего игр: {us_st.all_game}\n"
                         f"Выигрышных игр: {us_st.win_game}\n"
                         f"Проигрышных игр: {us_st.lose_game}",
                         )
    
    elif isinstance(event, CallbackQuery):
        await event.message.edit_text(f"Ваша статистика:\n"
                         f"Ваши очки {us_st.u_score.score}\n"
                         f"Всего игр: {us_st.all_game}\n"
                         f"Выигрышных игр: {us_st.win_game}\n"
                         f"Проигрышных игр: {us_st.lose_game}",
                         reply_markup = event.message.reply_markup # отправляем ту же самую клавиатуру
                         )

@router.message(Command(commands = 'statistic'), ~StateFilter(default_state))
async def command_statistic(message: Message):
    '''Команда для команды статистика вне игры'''    
    await message.answer(f"Вы еще в игре, статистика пока не доступна.")


@router.message(Command(commands = 'cancel'), StateFilter(default_state))
async def cancel_game(message: Message):
    '''Команда для команды cancel вне игры'''
    await message.answer(f"Вы не начали игру, что бы её отменить. Для начала игры введите команду /game")


@router.message(Command(commands = 'cancel'), ~StateFilter(default_state))
async def cancel_game(message: Message, state: FSMContext):
    '''Команда для отмены игры'''
    await message.answer(f"Вы отменили игру.\n Для начала новой введите /game")
    await state.clear()


@router.message(Command(commands = 'game'), ~StateFilter(default_state))
async def start_game(message: Message):
    '''Команда для начала новой игры, если игрок уже в игре'''
    await message.answer(f"Вы уже начали игру! 🎲\n"
                         f"Если хотите начать новую игру, отмените текущую командой /cancel")
    

@router.callback_query(lambda c: c.data in ['play_again', 'game'], StateFilter(default_state))
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



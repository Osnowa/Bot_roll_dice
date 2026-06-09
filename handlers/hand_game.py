from aiogram import Router

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from service.serv_user_db import UserService
from service.game_service import Roll_dice
from service.game_service_result import get_game_result
from database.repository_db import UserRepository
from keyboards.keyb_game import roll_dice_keyboard, play_again_keyboard, start_keyb, start_game_three_a_row, get_game_keyboard
from db_redis.redis_serv import redis_db
from handlers.fsm_hand import FSMGame
import logging



logger = logging.getLogger(__name__)
router = Router()



@router.callback_query(lambda c: c.data in ['roll_higher', 'roll_lower', 'roll_equal'], StateFilter(FSMGame.in_game, FSMGame.in_game_three_a_row))
async def handle_player_choice(callback: CallbackQuery):
    '''Обработка выбора'''
    roll_1, roll_2 = Roll_dice.roll() # бросок кубика опонента
    choice_game = callback.data # выбор игрока
    
    # сохранение выбора игрока
    await redis_db.hset(f"game_choice:{callback.from_user.id}",
                          mapping={"choice":f"{choice_game}"}
                        ) 
    await redis_db.expire(f"game_choice:{callback.from_user.id}", 600) # устанавливаем время жизни ключа 10 минут
    
    # сохранение броска оппонента
    await redis_db.hset(f"opponent_choice:{callback.from_user.id}",
                         mapping={"roll":roll_1 + roll_2}
                        )
    await redis_db.expire(f"opponent_choice:{callback.from_user.id}", 600) # устанавливаем время жизни ключа 10 минут

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
    user_serv = UserService(user_rep)
    us =  await user_rep.get_user(callback.from_user.id) # получаем пользователя

    # сохранение броска игрока
    await redis_db.hset(f"game_choice:{callback.from_user.id}",
                         mapping={"roll":roll_1 + roll_2}
                        )
    await redis_db.expire(f"game_choice:{callback.from_user.id}", 120) # устанавливаем время жизни ключа 2 минуты

    roll_oponenta = await redis_db.hget(f"opponent_choice:{callback.from_user.id}", "roll")
    roll_igroka = await redis_db.hget(f"game_choice:{callback.from_user.id}", "roll")
    choice_igroka = await redis_db.hget(f"game_choice:{callback.from_user.id}", "choice")
    
    result = get_game_result(int(roll_igroka), int(roll_oponenta), choice_igroka)
        # логика для базы данных
    if result == 'win':
        await user_serv.process_game_result(callback.from_user.id, 'win',  us.id)

        await callback.message.edit_text(f"Вы выбросили {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n\n"
                                    f"<b>Вы победили ! </b>🏆\n\n"
                                    f"Хоите сыграть еще ? 😏",
                                    reply_markup = play_again_keyboard())
    elif result == 'lose':
        # логика для базы данных
        await user_serv.process_game_result(callback.from_user.id, 'lose', us.id)

        await callback.message.edit_text(f"Вы выбросили {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n\n"
                                    f"<b>К сожалению Вы проиграли 😔 </b>\n\n "
                                    f"Хоите сыграть еще ? 😏",
                                    reply_markup = play_again_keyboard())
    elif result == 'draw':
        # логика для базы данных
        await user_serv.process_game_result(callback.from_user.id, 'draw', us.id)

        await callback.message.edit_text(f"Вы выбросили {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n\n"
                                    f"<b>Вы смогли угадать опонента ! </b>\n\n "
                                    f"Хоите сыграть еще ? 😏",
                                    reply_markup = play_again_keyboard())

    
    await state.clear() # очищаем состояние
    await redis_db.delete(f"game_choice:{callback.from_user.id}") # удаляем ключ для игрока
    await redis_db.delete(f"opponent_choice:{callback.from_user.id}") # удаляем ключ для оппонента


@router.callback_query(lambda c: c.data == 'stop_game', StateFilter(default_state))
async def stop_game(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Спасибо за игру !\n" 
                                     "Для начала новой введите /game\n"
                                     "Или воспользуйтесь клавиатурой ⌨️ ниже",
                                     reply_markup = start_keyb())
    await state.clear()
    await redis_db.delete(f"game_choice:{callback.from_user.id}") # удаляем ключ для игрока
    await redis_db.delete(f"opponent_choice:{callback.from_user.id}") # удаляем ключ для оппонента
    

@router.callback_query(lambda c: c.data == 'three_in_a_row', StateFilter(default_state))
async def three_in_a_row(callback: CallbackQuery, state: FSMContext):
    '''Обработка кнопки старт игры 3 подряд'''    
    await callback.message.edit_text(f"Добро подаловать в режим игры 3 подряд !\n"
                                     "Если не сможете 3 раза подряд выиграть у опонента, то Вам начисляется 1000 очков\n"
                                     "За проигрыш очки не снимаются\n"
                                     f"Вы готовы ?",
                                     reply_markup = start_game_three_a_row()
                                     ) # добавить клавиатуру на согласие игры 

@router.callback_query(lambda c: c.data == 'stop_three_a_row', StateFilter(default_state))    
async def stop_three_a_row(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Ну что же, тогда в другой раз !",
                                   reply_markup = start_keyb()
                                   )
    
@router.callback_query(lambda c: c.data == 'play_three_a_row', StateFilter(default_state))    
async def play_three_a_row(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMGame.in_game_three_a_row) # переход в состояние игры 3 подряд

    # ставим ключ по кол-во попыток
    await redis_db.hset(f"game_choice:{callback.from_user.id}",
                         mapping={"attempt": 0}
                        )

    await callback.message.edit_text(f"Игры до 3️⃣ побед началась!  🎲\n"
                         f"Как вы думаете, Вы выбросите больше опонента ?",
                         reply_markup = get_game_keyboard())
    

@router.callback_query(lambda c: c.data == 'roll_dice', StateFilter(FSMGame.in_game_three_a_row))
async def roll_dice(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    '''Обработка кнопки бросить кубик и получение результата для режима 3 подряд'''
    roll_1, roll_2 = Roll_dice.roll()
    user_rep = UserRepository(session) # передаем сессию в класс с методами работой функции
    user_serv = UserService(user_rep)
    us =  await user_rep.get_user(callback.from_user.id) # получаем пользователя

    # сохранение броска игрока
    await redis_db.hset(f"game_choice:{callback.from_user.id}",
                         mapping={"roll":roll_1 + roll_2}
                        )
    await redis_db.expire(f"game_choice:{callback.from_user.id}", 120) # устанавливаем время жизни ключа 2 минуты

    roll_oponenta = await redis_db.hget(f"opponent_choice:{callback.from_user.id}", "roll")
    roll_igroka = await redis_db.hget(f"game_choice:{callback.from_user.id}", "roll")
    choice_igroka = await redis_db.hget(f"game_choice:{callback.from_user.id}", "choice")
    attemp_num = await redis_db.hget(f"game_choice:{callback.from_user.id}", "attempt") # получаем кол-во попыток
    
    # получаем рзультат
    result = get_game_result(int(roll_igroka), int(roll_oponenta), choice_igroka)

    if result == 'win' or result == 'draw':

        await redis_db.hset(f"game_choice:{callback.from_user.id}",
                             mapping={"attempt": int(attemp_num) + 1}
                            )
        
        if int(attemp_num) == 3:
            # зачисляем очки победителю
            await user_serv.process_game_result(callback.from_user.id, 'win_three_in_a_row',  us.id)
            await callback.message.edit_text(f"Вы выбросили {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n\n"
                                            f"<b>Вы победили в супер игре ! </b>🏆\n\n")
            
            
            await state.clear() # очищаем состояние
            await redis_db.delete(f"game_choice:{callback.from_user.id}") # удаляем ключ для игрока
            await redis_db.delete(f"opponent_choice:{callback.from_user.id}") # удаляем ключ для оппонента

        elif int(attemp_num) < 3:
            await callback.message.edit_text(f"Вы выбросили {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n\n"
                                        f"<b>Вы одержали победу в {int(attemp_num) + 1} раунде ! </b>🏆\n\n"
                                        f"Продолжаем ! 🎲 \n"
                                        "Как вы думаете, Вы выбросите больше опонента ?",
                                        reply_markup = get_game_keyboard())
   
    elif result == 'lose':
        # логика для базы данных
        await user_serv.process_game_result(callback.from_user.id, 'lose', us.id)

        await callback.message.edit_text(f"Вы выбросили {roll_1} и {roll_2} (сумма: {roll_1 + roll_2})\n\n"
                                    f"<b>К сожалению Вы проиграли 😔 </b>\n\n ",
                                    reply_markup = start_keyb()
                                    )
        
        await state.clear() # очищаем состояние
        await redis_db.delete(f"game_choice:{callback.from_user.id}") # удаляем ключ для игрока
        await redis_db.delete(f"opponent_choice:{callback.from_user.id}") # удаляем ключ для оппонента

    
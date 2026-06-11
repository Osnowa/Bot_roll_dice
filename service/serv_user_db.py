from database.repository_db import UserRepository
from config import Config_game

class UserService:
    '''Сервис для работы с пользователем'''
    def __init__(self, user_repo: UserRepository):
        # получаем все методы репозитория user, которые работают с сессией
        self.user_repo = user_repo

    async def register(self, tg_id: int, user_name: str):
        '''Регистрируем пользователя'''
        user =  await self.user_repo.get_user(tg_id)
        if user:
            return True, user, user.u_score.score
        
        # если пользователя в базе данных нет
        await self.user_repo.add_user(tg_id, username=user_name) # добавляем пользователя

        user = await self.user_repo.get_user(tg_id)  # получаем пользователя
        u_id = user.id # получаем id пользователя
        await self.user_repo.add_score(u_id) # добавляем запись в таблицу с очками
        score_us = await self.user_repo.get_score(u_id) # получаем очки
        return False, None, score_us.score

    async def process_game_result(self, tg_id: int, result: str, u_id: int):
        cof_res = Config_game()
        if result == 'win':
            await self.user_repo.update_game_st_win(tg_id)
            await self.user_repo.update_score(u_id, cof_res.score_win)
        elif result == 'lose':
            await self.user_repo.update_game_st_lose(tg_id)
            await self.user_repo.update_score(u_id, -cof_res.score_win)
        elif result == 'draw':
            await self.user_repo.update_game_st_draw(tg_id)
            await self.user_repo.update_score(u_id, cof_res.score_win_draw)
        if result == 'win_three_in_a_row':
            await self.user_repo.update_game_st_win(tg_id)
            await self.user_repo.update_score(u_id, cof_res.score_win_three_in_a_row)
            

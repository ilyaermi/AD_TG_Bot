import aiohttp
from typing import Coroutine
from TelegramBot.classess import OrderInfo

class Http:
    async def request(self, url, data=None, method='POST'):
        for i in range(3):
            try:
                async with aiohttp.request(method,
                                           f'http://localhost:8000/{url}', json=data) as resp:
                    if resp.status != 200:
                        raise
                    return await resp.json()
            except:
                pass

    def execute_db(self, list_args: list) -> Coroutine:
        return self.request('execute_db',
                                  data={'list_args': list_args}, method='POST')

class HttpUsers(Http):

    async def add_admin(self, user_id):
        check_admin = await self.execute_db(['SELECT * FROM User WHERE user_id=?', [user_id]])
        if len(check_admin) == 0:
            await self.execute_db(['INSERT INTO User VALUES(?,?)', [user_id, True]])
        else:
            await self.execute_db(['UPDATE User SET admin=? WHERE user_id=?', [True, user_id]])

class HttpOrders(Http):

    async def get_orders(self, user_id:int) -> list[OrderInfo]:
        orders = await self.execute_db(['SELECT * FROM Orders WHERE user_id=?', [user_id]])
        return [OrderInfo(*i[1:]) for i in orders]

http_users = HttpUsers()
http_orders = HttpOrders()
import aiohttp
from typing import Coroutine
from TelegramBot.classess import OrderInfo
import config as cfg


class Http:
    async def request(self, url, data=None, method='POST'):
        for i in range(3):
            try:
                async with aiohttp.request(method,
                                           f'http://localhost:{cfg.port}/{url}', json=data) as resp:
                    if resp.status != 200:
                        raise
                    return await resp.json()
            except Exception as e:
                print(e)
                print(data)
                pass

    def execute_db(self, list_args: list) -> Coroutine:
        return self.request('execute_db',
                            data={'list_args': list_args}, method='POST')


class HttpUsers(Http):

    async def add_admin(self, user_id):
        check_admin = await self.execute_db(['SELECT * FROM User WHERE user_id=?', [user_id]])
        print(check_admin)
        if len(check_admin) == 0:
            await self.execute_db(['INSERT INTO User VALUES(?,?,?)', [user_id, True, True]])
        else:
            await self.execute_db(['UPDATE User SET admin=? WHERE user_id=?', [True, user_id]])

    async def get_admins(self) -> list[int, str]:
        ans = await self.execute_db(['SELECT user_id FROM User WHERE admin',])
        return [i[0] for i in ans]


class HttpOrders(Http):

    async def get_orders(self, user_id: int) -> list[OrderInfo]:
        if user_id in cfg.admin_list:
            orders = await self.execute_db(['SELECT * FROM Orders'])
        else:
            orders = await self.execute_db(['SELECT * FROM Orders WHERE user_id=?', [user_id]])

        return [OrderInfo(*i) for i in orders]

    async def new_order(self, data: OrderInfo):
        await self.execute_db(['INSERT INTO Orders VALUES(?,?,?,?,?,?,?,?,?,?, ?)', list(data.__dict__.values())])

    async def update_order(self, order: OrderInfo):
        data = list(order.__dict__.values())[2:]
        data.append(order.uid_order)
        await self.execute_db(['UPDATE Orders SET region=?, type_com=?, section=?, rate=?, billing=?, pay=?, active=?, tx_hash=?, user_url=? WHERE uid_order=?', data])

http_users = HttpUsers()
http_orders = HttpOrders()

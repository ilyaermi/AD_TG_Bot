from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from ..keyboards import Keyboards
from ..main import dp, bot
import config as cfg
import re
from ..states import MyOrders, UserMenu
from ..check_pay import check_bep20_txs_status, check_trc20_txs_status
from time import time
from asyncio import sleep
from api.http_api import http_orders
kbd = Keyboards()


@dp.callback_query_handler(text='my_orders', state=UserMenu.menu)
async def my_orders(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выберите пункт:', reply_markup=kbd.my_orders())
    await MyOrders.main_menu.set()


@dp.callback_query_handler(text='active_orders', state=MyOrders.main_menu)
async def my_orders(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    orders = await http_orders.get_orders(user_id)
    orders = [i for i in orders if i.active]
    await state.update_data(orders=orders, page=0)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Активные заказы:', reply_markup=kbd.menu_order(orders=orders, page=0))
    await MyOrders.next()


@dp.callback_query_handler(text='history_orders', state=MyOrders.main_menu)
async def my_orders(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    orders = await http_orders.get_orders(user_id)
    await state.update_data(orders=orders, page=0)
    orders = [i for i in orders if not i.active]
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='История заказов:', reply_markup=kbd.menu_order(orders=orders, page=0))
    await MyOrders.next()

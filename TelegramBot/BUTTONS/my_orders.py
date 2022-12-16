from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from ..keyboards import Keyboards
from ..main import dp, bot
import config as cfg
import re
from ..states import MyOrders, UserMenu
from ..check_pay import check_bep20_txs_status, check_trc20_txs_status
from ..classess import OrderInfo
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
    active_orders = []
    for order in orders:
        if order.active:
            active_orders.append(order)
    await state.update_data(orders=orders, page=0)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Активные заказы:', reply_markup=kbd.menu_order(orders=active_orders, page=0))
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


@dp.callback_query_handler(Text(startswith='select_order_'), state=MyOrders.select_order)
async def my_orders(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    select_order = cq.data.split('select_order_')[1]
    orders: list[OrderInfo] = (await state.get_data())['orders']
    page = (await state.get_data())['page']
    order = [i for i in orders if i.uid_order == select_order][0]
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text=f'Регион - {order.region}\n'
                                f'Тип рекламы - {order.type_com}\n'
                                f'Раздел рекламы - {order.section}\n'
                                f'Тариф рекламы - {order.rate}\n', reply_markup=kbd.menu_order(orders=orders, page=0))


@dp.callback_query_handler(Text(startswith='remove_order_'), state=MyOrders.select_order)
async def my_orders(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    select_order = cq.data.split('remove_order_')[1]
    orders: list[OrderInfo] = (await state.get_data())['orders']
    page = (await state.get_data())['page']
    order = [i for i in orders if i.uid_order == select_order][0]
    orders.remove(order)
    await state.update_data(orders=orders)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text=f'Заказ удалён.', reply_markup=kbd.menu_order(orders=orders, page=page))


@dp.callback_query_handler(Text(startswith='replace_page_'), state=MyOrders.select_order)
async def my_orders(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    page = int(cq.data.split('replace_page_')[1])
    orders = (await state.get_data())['orders']
    await state.update_data(page=page)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='История заказов:', reply_markup=kbd.menu_order(orders=orders, page=page))
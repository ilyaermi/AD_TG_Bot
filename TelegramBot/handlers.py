import sqlite3
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from .states import OrderCommercial, MyOrders, Support
import config as cfg
from .keyboards import Keyboards
from .main import bot, dp
from .states import UserMenu
from api.http_api import http_users

kbd = Keyboards()


async def on_startup(dp):
    """ try to add admins and create table to add MAIN admin from cfg.admin_list"""
    for id in cfg.admin_list:
        await http_users.add_admin(id)
        await bot.send_message(
            chat_id=id,
            text='<b>Bot launched.</b>'
        )


@dp.message_handler(commands=['start', 'menu'])
async def start(message: Message):
    menu_markup = kbd.main_menu()
    await message.answer(
        text='Главное меню:',
        reply_markup=menu_markup
    )
    await UserMenu.menu.set()


@dp.callback_query_handler(text='back_to_menu')
async def fast_start(cq: CallbackQuery):
    """Callback btn press key back_to_menu"""
    menu_markup = kbd.main_menu()
    msg = cq.message
    await bot.edit_message_text(
        chat_id=msg.from_user.id,
        message_id=msg.message_id,
        text='Menu:',
        reply_markup=menu_markup
    )
    await UserMenu.menu.set()
state = [OrderCommercial.region,
         OrderCommercial.type_com,
         OrderCommercial.section,
         OrderCommercial.rate,
         OrderCommercial.billing,
         OrderCommercial.pay,
         MyOrders.main_menu,
         MyOrders.select_order,
         Support.main_menu,
         UserMenu.menu]


@dp.callback_query_handler(text='back_to_menu', state=state)
async def fast_start(cq: CallbackQuery, state: FSMContext):
    """Callback btn press key back_to_menu"""
    menu_markup = kbd.main_menu()
    msg = cq.message
    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        text='Menu:',
        reply_markup=menu_markup
    )
    await UserMenu.menu.set()


@dp.message_handler(commands=['start', 'menu'], state=state)
async def start(message: Message):
    menu_markup = kbd.main_menu()
    await message.answer(
        text='Главное меню:',
        reply_markup=menu_markup
    )
    await UserMenu.menu.set()

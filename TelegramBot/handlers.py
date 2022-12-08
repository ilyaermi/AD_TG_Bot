import sqlite3

from aiogram.types import Message

import config as cfg
from .keyboards import Keyboards
from .main import bot, dp
from .states import UserMenu
from bd import bd
kbd = Keyboards()


async def on_startup(dp):
    """ try to add admins and create table to add MAIN admin from cfg.admin_list"""
    bd.db_users.add_admins(cfg.admin_list)
    for admin in cfg.admin_list:
        await bot.send_message(
            chat_id=admin,
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
async def fast_start(message: Message):
    """Callback btn press key back_to_menu"""
    menu_markup = kbd.main_menu()
    mes_id = message['message']['message_id']
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text='Menu:',
        reply_markup=menu_markup
    )

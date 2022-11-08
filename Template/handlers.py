import sqlite3

from aiogram.types import Message

import config as cfg
from database_connector import db_admin
from keyboards import Keyboards
from main import bot, dp
import BUTTONS

kbd = Keyboards()


async def on_startup(dp):
    """ try to add admins and create table to add MAIN admin from cfg.admin_list"""
    for admin in cfg.admin_list:
        try:
            db_admin.add_admin(user_id=admin)
        except sqlite3.IntegrityError:
            pass
    """ notify admins when bot started """
    for admin in cfg.admin_list:
        await bot.send_message(
            chat_id=admin,
            text='<b>Bot launched.</b>'
        )


@dp.message_handler(commands=['start', 'menu'])
async def start(message: Message):
    """btns start and menu"""
    if str(message.from_user.id) in cfg.admin_list:
        menu_markup = kbd.main_menu()
        await message.answer(
            text='Hello, you are in test bot.',
            reply_markup=menu_markup
        )


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

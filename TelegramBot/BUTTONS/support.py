from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from ..keyboards import Keyboards
from ..main import dp, bot
import config as cfg
import re
from ..states import Support, UserMenu
from ..check_pay import check_bep20_txs_status, check_trc20_txs_status
from time import time
from asyncio import sleep
from api.http_api import http_orders
kbd = Keyboards()


@dp.callback_query_handler(text='collaboration_support', state=UserMenu.menu)
async def my_orders(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выберите пункт:', reply_markup=kbd.support_menu())
    await Support.main_menu.set()

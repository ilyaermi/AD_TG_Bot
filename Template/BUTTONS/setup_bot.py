from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from database_connector import db_bot_switch
from keyboards import Keyboards
from main import dp, bot

kbd = Keyboards()


@dp.callback_query_handler(text='setup_bot')
async def bot_switch(message: Message):
    """main kbd to on or off bot"""
    bot_status = db_bot_switch.bot_status()
    mes_id = message['message']['message_id']
    setup_bot = kbd.btn_to_setup_bot(bot_status)
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=f'Now bot is <b>{"on" if bot_status else "off"}</b>.',
        reply_markup=setup_bot
    )


@dp.callback_query_handler(Text(startswith="setup_bot"))
async def bot_switch(message: Message):
    """handles callback from main kbd"""
    data = message.data.split('setup_bot_')[1]
    mes_id = message['message']['message_id']
    db_bot_switch.change_bot_status(True if data == 'on' else False)
    bot_status = db_bot_switch.bot_status()
    setup_bot = kbd.btn_to_setup_bot(bot_status)
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=f'Now bot is <b>{"on" if bot_status else "off"}</b>.',
        reply_markup=setup_bot
    )

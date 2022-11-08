from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from database_connector import db_users
from keyboards import Keyboards
from main import dp, bot
from states import ChangeUserInvest

kbd = Keyboards()


@dp.callback_query_handler(text='setup_users')
async def setup_users(message: Message):
    """main kbd to settings for users"""
    mes_id = message['message']['message_id']
    setup_users = kbd.btn_setup_users()
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=f'Here you can setup all account by one click or every account separately.',
        reply_markup=setup_users
    )


@dp.callback_query_handler(Text(startswith="setup_user_info_"))
async def get_users_info(message: Message):
    """returns information about user by btn"""
    data = message.data.split('setup_user_info_')[1]
    mes_id = message['message']['message_id']
    setup_users = kbd.btn_setup_users()
    user_data = db_users.get_users_info(data)
    user_frendly_name = user_data[0]
    user_api_key = user_data[1]
    user_api_secret = user_data[2]
    user_invest = user_data[3]
    text = (f'user: <b>{user_frendly_name}</b>\n'
            f'apikey: <span class="tg-spoiler">{user_api_key}</span>\n'
            f'api secret: <span class="tg-spoiler">{user_api_secret}</span>\n'
            f'invest: {user_invest}%\n')
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=text,
        reply_markup=setup_users
    )


@dp.callback_query_handler(Text(startswith="setup_user_change_invest_"))
async def change_users_invest(message: Message, state: FSMContext):
    """get state to change invest procent for user"""
    data = message.data.split('setup_user_change_invest_')[1]
    mes_id = message['message']['message_id']
    setup_users = kbd.btn_setup_users()
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=f'In next message enter new invest % for user: {data}.\nInteger 1 to 100.'
    )

    await ChangeUserInvest.invest_part.set()
    await state.update_data(account_name=data)


@dp.callback_query_handler(Text(startswith="setup_user_delete_user_"))
async def delete_user(message: Message):
    """delete user by btn"""
    data = message.data.split('setup_user_delete_user_')[1]
    mes_id = message['message']['message_id']
    db_users.delete_user(data)
    setup_users = kbd.btn_setup_users()
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=f'User {data} was deleted.',
        reply_markup=setup_users
    )


@dp.message_handler(state=ChangeUserInvest.invest_part)
async def add_admin(message: Message, state: FSMContext):
    """gets message about new user invest procent"""
    try:
        await state.update_data(invest_part=message.text)
        data = await state.get_data()
        db_users.change_invest_for_user(data['account_name'], data['invest_part'])
        setup_users = kbd.btn_setup_users()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'User {data["account_name"]} invest part was changed to {data["invest_part"]}.',
            reply_markup=setup_users
        )
    except Exception as err:
        setup_users = kbd.btn_setup_users()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Error: {err}.',
            reply_markup=setup_users
        )
    await state.finish()

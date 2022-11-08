from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database_connector import db_users
from keyboards import Keyboards
from main import dp, bot
from states import RegisterNewUser

kbd = Keyboards()
btn_cancel = kbd.btn_cancel()
main_menu = kbd.main_menu()


@dp.callback_query_handler(text='new_user')
async def register_new_user(message: Message):
    """Starts State to add new user to database"""
    mes_id = message['message']['message_id']
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=('You are now in stage to add new user. Here will be 4 steps:\n'
              'step 1: Enter user frendly name. (max lenght = 15)\n'
              'step 2: Enter user api key.\n'
              'step 3: Enter user api secret.\n'
              'step 4: Enter user invest procent. (integer 1 to 100)\n'
              'At any step you can press button "Cancel" below and quit.\n\n'
              'Enter frendly name to new user in next message:'),
        reply_markup=btn_cancel
    )
    await RegisterNewUser.frendly_name.set()


@dp.message_handler(state=RegisterNewUser.frendly_name)
async def get_user_frendly_name(message: Message, state: FSMContext):
    """first step to add new user - enter name"""
    await state.update_data(frendly_name=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Enter api key:')
    await RegisterNewUser.next()


@dp.message_handler(state=RegisterNewUser.api_key)
async def get_user_api_key(message: Message, state: FSMContext):
    """second step - enter api key"""
    await state.update_data(api_key=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Enter api secret:'
    )
    await RegisterNewUser.next()


@dp.message_handler(state=RegisterNewUser.api_secret)
async def get_user_api_secret(message: Message, state: FSMContext):
    """thirs step - get secret key"""
    await state.update_data(api_secret=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='And finally enter users invest procent:'
    )
    await RegisterNewUser.next()


@dp.message_handler(state=RegisterNewUser.invest_procent)
async def get_user_api_secret(message: Message, state: FSMContext):
    """final step - get margin and add user to database"""
    await state.update_data(invest_procent=message.text)
    data = await state.get_data()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=f'User registration "{data["frendly_name"]}" was successful.',
        reply_markup=main_menu
    )
    db_users.create_new_user(data)
    await state.finish()


@dp.callback_query_handler(state=[
    RegisterNewUser.frendly_name,
    RegisterNewUser.api_key,
    RegisterNewUser.api_secret], text=['cancel'])
async def cancel_add_new_user(message: Message, state: FSMContext):
    """handles cancel btn"""
    mes_id = message['message']['message_id']
    await state.finish()
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text='Operation canceled.\n\nMenu:',
        reply_markup=main_menu
    )

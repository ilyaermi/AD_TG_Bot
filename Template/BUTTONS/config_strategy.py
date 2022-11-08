from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from keyboards import Keyboards
from main import dp, bot
from database_connector import db_settings
from states import StrategyConfig

kbd = Keyboards()
btn_cancel = kbd.btn_cancel()


@dp.callback_query_handler(text='config_strategy')
async def config_strategy(message: Message):
    """Handles btn 'config strategy' click."""
    mes_id = message['message']['message_id']
    config_strategy_kbd = kbd.btn_config_strategy()
    config = db_settings.get_strategy()
    if len(config) == 0:
        text = 'Now you dont have strategy, press btn to setup it.'
    else:
        text = 'Current strategy:\n\n'
        for el in config:
            text += f'take #{el[0]}: qty reduce = {float(el[2])*100}%{"" if el[1] == 0 else ", moving stop loss"}\n'
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=text,
        reply_markup=config_strategy_kbd
    )


@dp.callback_query_handler(Text(startswith="config_setup_"))
async def register_new_user(message: Message):
    """handles singly btn click"""
    data = message.data.split('config_setup_')[1]
    mes_id = message['message']['message_id']
    manual_text = ('Okay, here will be 3 steps:\n'
                   '1 step: enter amount of takes-profit.\n'
                   '2 step: enter which take-profit should work to move stop-loss it should be lower as number of 1 step.\n'
                   '3 step: enter N numbers, equal to the number of take profits from a new line,'
                   'which will be equal to 100 in total.\n\n'
                   'Example:\n'
                   'In first step i enter <u><b>3</b></u>\n'
                   'In second step i enter <u><b>2</b></u>\n'
                   'In third step i enter numbers <u><b>in one message using new lines</b></u>:\n'
                   '<u><b>40\n'
                   '40\n'
                   '20</b></u>\n\n'
                   'so my strategy would be:\n'
                   '3 takes, after 2nd take will work '
                   '- stop will moved to breakeven and '
                   '1st take will close 40% my position, 2nd:40%, 3d:20%.\n\n'
                   'In next message enter amount of take-profits:')
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text=manual_text,
        reply_markup=btn_cancel
    )
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=open('./hint.png', 'rb')
    )
    await StrategyConfig.takes.set()


@dp.message_handler(state=StrategyConfig.takes)
async def get_strategy_takes(message: Message, state: FSMContext):
    """thirs step - get secret key"""
    try:
        some_int = int(message.text)
        if 0 < some_int < 20:
            await state.update_data(takes=message.text)
            await bot.send_message(
                chat_id=message.from_user.id,
                text='Enter which takes should move stop-loss to breakeven. Countdown from entry point:'
            )
            await StrategyConfig.next()
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=('<b>Please, enter integer more than 0 and lower than 20</b>\n\n'
                      'In next message enter qty of take-profits:'),
                reply_markup=btn_cancel
            )
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=('<b>Please, enter integer.</b>\n\n'
                  'In next message enter qty of take-profits:'),
            reply_markup=btn_cancel
        )


@dp.message_handler(state=StrategyConfig.breakeven)
async def get_strategy_breakeven(message: Message, state: FSMContext):
    """thirs step - get secret key"""
    try:
        some_int = int(message.text)
        data = await state.get_data()
        if some_int <= int(data['takes']):
            await state.update_data(breakeven=message.text)
            await bot.send_message(
                chat_id=message.from_user.id,
                text=(f'Enter <b>{data["takes"]}</b> numbers, each in new line of qty every take-profit.'
                      'Countdown from entry point, total sum must be equal 100:')
            )
            await StrategyConfig.next()
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f'Number must be lower or equals qty of takes ({data["takes"]}).',
                reply_markup=btn_cancel
            )
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=('<b>Please, enter integer.</b>\n\n'
                  'Enter which takes should move stop-loss to breakeven. Countdown from entry point:'),
            reply_markup=btn_cancel
        )


@dp.message_handler(state=StrategyConfig.qty)
async def get_strategy_qty(message: Message, state: FSMContext):
    """thirs step - get secret key"""
    try:
        config_strategy_kbd = kbd.btn_config_strategy()
        await state.update_data(qty=message.text)
        data = await state.get_data()
        data_dict, data_list = data_treatment(data)
        total = 0
        for i in range(len(data_list)):
            total += int(data_dict[i]['qty'])
        if total == 100:
            text = f'New strategy config:\n\n'
            for i in range(len(data_list)):
                text = text + f'take #{i+1}:qty reduce: {data_list[i][2] * 100}%{", moves stop" if data_list[i][1] else ""}\n'
            await bot.send_message(
                chat_id=message.from_user.id,
                text=text,
                reply_markup=config_strategy_kbd
            )
            await state.finish()
            db_settings.update_table(data_list)
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f'<b>Sum must be equals 100!</b>\nNow it\'s {total}.\nEnter new {data["takes"]} numbers, each in new line.',
                reply_markup=btn_cancel
            )
    except IndexError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Please enter numbers equals takes.',
            reply_markup=btn_cancel
        )
    except Exception as err:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'some error: {err}, try again.',
            reply_markup=btn_cancel
        )


def data_treatment(data: dict):
    final_data_dict = []
    final_data_list = []

    for i in range(int(data['takes'])):
        final_data_dict.append({'take': i + 1, 'breakeven': False, 'qty': None})
        final_data_list.append([i + 1, False, None])

    final_data_dict[int(data['breakeven']) - 1]['breakeven'] = True
    final_data_list[int(data['breakeven']) - 1][1] = True

    for i in range(len(final_data_dict)):
        final_data_dict[i]['qty'] = data['qty'].split('\n')[i]
        final_data_list[i][2] = float(data['qty'].split('\n')[i]) / 100

    return final_data_dict, final_data_list


@dp.callback_query_handler(state=[
    StrategyConfig.breakeven,
    StrategyConfig.takes,
    StrategyConfig.qty], text=['cancel'])
async def cancel_add_new_user(message: Message, state: FSMContext):
    """handles cancel btn"""
    mes_id = message['message']['message_id']
    main_menu = kbd.main_menu()
    await state.finish()
    await bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=mes_id,
        text='Operation canceled.\n\nMenu:',
        reply_markup=main_menu
    )

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from ..keyboards import Keyboards
from ..main import dp, bot
import config as cfg
from ..classess import OrderInfo
import re
from api.http_api import http_orders
from ..states import OrderCommercial, UserMenu
from ..check_pay import check_bep20_txs_status, check_trc20_txs_status
from time import time
from asyncio import sleep
kbd = Keyboards()


@dp.callback_query_handler(text='order_commercial', state=UserMenu.menu)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выберите предпочтительный регион рекламы:', reply_markup=kbd.regions())
    await OrderCommercial.region.set()


@dp.callback_query_handler(Text(startswith='select_region_'), state=OrderCommercial.region)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    region = cq.data.split('select_region_')[1]
    await state.update_data(order=OrderInfo(region=region, user_id=user_id))
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выберете раздел,чтобы мы подобрали для Вас наиболее заинтересованную аудиторию:', reply_markup=kbd.type_coms())
    await OrderCommercial.next()


@dp.callback_query_handler(Text(startswith='select_type_com_'), state=OrderCommercial.type_com)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    order = (await state.get_data())['order']
    order.type_com = cq.data.split('select_type_com_')[1]
    await state.update_data(order=order)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Пожалуйста помогите нам определить тематику вашего канала под рекламу:', reply_markup=kbd.sections())
    await OrderCommercial.next()


@dp.callback_query_handler(Text(startswith='select_section_'), state=OrderCommercial.section)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    order = (await state.get_data())['order']
    order.section = cq.data.split('select_section_')[1]
    await state.update_data(order=order)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Пожалуйста,выберете наиболее подходящий для вас тариф. Нажмите на тариф и узнайте подробней:', reply_markup=kbd.rates())
    await OrderCommercial.next()


@dp.callback_query_handler(Text(startswith='select_rate_'), state=OrderCommercial.rate)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    order = (await state.get_data())['order']
    order.rate = cq.data.split('select_rate_')[1]
    await state.update_data(order=order)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Оплата:', reply_markup=kbd.billing())
    await OrderCommercial.next()


@dp.callback_query_handler(Text(startswith='select_billing_'), state=OrderCommercial.billing)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    order = (await state.get_data())['order']
    order.billing = cq.data.split('select_billing_')[1]
    await state.update_data(order=order, _msg=msg)
    wallet = cfg.payAdress_bep20 if order.billing == 'BEP20' else cfg.payAdress_trc20
    bank = 150 if order.rate == 'Standart' else 350 if order.rate == 'Premium' else 500 if order.rate == "Individual" else 1
    await state.update_data(bank=bank)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text=f'Сумма: {bank}$\nКошелек для оплаты:\n<code>{wallet}</code>\nВведите txid транзакции:', reply_markup=kbd.single_menu_btn())
    await OrderCommercial.next()


async def mailing_admins(order:OrderInfo, msg:Message):
    for admin in cfg.admin_list:
        await bot.send_message(admin, text=f'Новый заказ!\n{order}\n\nЮзер: @{msg.from_user.username}', reply_markup=kbd.kbd_with_btn_url(order.user_url))


@dp.message_handler(state=OrderCommercial.pay)
async def order_commercial(msg: Message, state: FSMContext):
    user_id = msg.chat.id
    _user_msg = msg
    data = await state.get_data()
    _msg: Message = data['_msg']
    order = (await state.get_data())['order']
    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
    _tx = msg.text
    ans = re.findall('^', _tx)
    if ans:
        order.tx_hash = _tx
        order.user_url = msg.from_user.url
        msg = await bot.edit_message_text(chat_id=user_id, message_id=_msg.message_id, text='Проверяю...')
        time_start_check = time()
        while time() - time_start_check < 1800:
            if order.billing == 'BEP20':
                if await check_bep20_txs_status(_tx, data['bank']):
                    await bot.send_message(chat_id=user_id, text='Платёж получен!', reply_markup=kbd.single_menu_btn())
                    order.pay = True
                    order.active = True
                    await http_orders.new_order(order)
                    await mailing_admins(order, _user_msg)
                    break
            else:
                if await check_trc20_txs_status(_tx, data['bank']):
                    await bot.send_message(chat_id=user_id, text='Платёж получен!', reply_markup=kbd.single_menu_btn())
                    order.pay = True
                    order.active = True
                    await http_orders.new_order(order)
                    await mailing_admins(order, _user_msg)
                    break
            await sleep(30)
        if time() - time_start_check >= 1800:
            msg = await bot.edit_message_text(chat_id=user_id, message_id=_msg.message_id, text='Платёж не получен.')
            await state.finish()
    else:
        await bot.edit_message_text(chat_id=user_id, message_id=_msg.message_id, text='Неверный формат, попробуй ещё раз.')
        return ''

    await state.finish()

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from ..keyboards import Keyboards
from ..main import dp, bot
from ..states import OrderCommercial, UserMenu

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
    await state.update_data(region=region)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выберите тип рекламы:', reply_markup=kbd.type_coms())
    await OrderCommercial.next()


@dp.callback_query_handler(Text(startswith='select_type_com_'), state=OrderCommercial.type_com)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    type_com = cq.data.split('select_type_com_')[1]
    await state.update_data(type_com=type_com)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выберите раздел рекламы:', reply_markup=kbd.sections())
    await OrderCommercial.next()


@dp.callback_query_handler(Text(startswith='select_section_'), state=OrderCommercial.section)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    section = cq.data.split('select_section_')[1]
    await state.update_data(section=section)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выберите тариф рекламы:', reply_markup=kbd.rates())
    await OrderCommercial.next()


@dp.callback_query_handler(Text(startswith='select_rate_'), state=OrderCommercial.rate)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    rate = cq.data.split('select_rate_')[1]
    await state.update_data(rate=rate)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Оплата:', reply_markup=kbd.billing())
    await OrderCommercial.next()


@dp.callback_query_handler(Text(startswith='select_billing_'), state=OrderCommercial.billing)
async def order_commercial(cq: CallbackQuery, state: FSMContext):
    msg = cq.message
    user_id = msg.chat.id
    billing = cq.data.split('select_billing_')[1]
    await state.update_data(billing=billing)
    await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Кошелек для оплаты:\nВведите txid транзакции', reply_markup='')
    await OrderCommercial.next()

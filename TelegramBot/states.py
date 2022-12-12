from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderCommercial(StatesGroup):
    """State for register new user."""
    region = State()
    type_com = State()
    section = State()
    rate = State()
    billing = State()
    pay = State()


class MyOrders(StatesGroup):
    """State for register new user."""
    main_menu = State()
    select_order=State()


class Support(StatesGroup):
    """State for register new user."""
    main_menu = State()

class UserMenu(StatesGroup):
    menu = State()

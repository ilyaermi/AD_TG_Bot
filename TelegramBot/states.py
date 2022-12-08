from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderCommercial(StatesGroup):
    """State for register new user."""
    region = State()
    type_com = State()
    section = State()
    rate = State()
    billing = State()


class UserMenu(StatesGroup):
    menu = State()

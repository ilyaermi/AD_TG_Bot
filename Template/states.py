from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterNewUser(StatesGroup):
    """State for register new user."""
    frendly_name = State()
    api_key = State()
    api_secret = State()
    invest_procent = State()


class RegisterNewAdmin(StatesGroup):
    """State for register new admin."""
    admin_id = State()


class DeleteAdmin(StatesGroup):
    """State for delete admin."""
    admin_id = State()


class ChangeUserInvest(StatesGroup):
    """State change invest part for user."""
    account_name = State()
    invest_part = State()


class StrategyConfig(StatesGroup):
    """State for config new strategy."""
    takes = State()
    breakeven = State()
    qty = State()


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database_connector import db_users


class Keyboards:

    def __init__(self):
        self.btn_back_to_menu = InlineKeyboardButton(
            text='↩️Back to menu',
            callback_data='back_to_menu'
        )

    def single_menu_btn(self):
        """Keyboard back to menu btn."""
        menu_btn = InlineKeyboardMarkup(row_width=2)
        menu_btn.insert(self.btn_back_to_menu)

        return menu_btn

    def main_menu(self):
        """returns start markup"""
        main_menu = InlineKeyboardMarkup(row_width=2)

        btn_add_new_user = InlineKeyboardButton(
            text='Add new user',
            callback_data='new_user'
        )
        btn_setup_users = InlineKeyboardButton(
            text='Setup users',
            callback_data='setup_users'
        )
        btn_config = InlineKeyboardButton(
            text='Config strategy',
            callback_data='config_strategy'
        )
        btn_setup_bots = InlineKeyboardButton(
            text='Setup bot',
            callback_data='setup_bot'
        )
        btn_add_admin = InlineKeyboardButton(
            text='Admin manage',
            callback_data='add_admin'
        )

        btn_list = [btn_add_new_user, btn_setup_users, btn_config,
                    btn_setup_bots, btn_add_admin]

        for btn in btn_list:
            main_menu.insert(btn)

        return main_menu

    def btn_to_setup_bot(self, bot_status):
        """Keyboard on or off bot."""
        btn_to_setup_bot = InlineKeyboardMarkup(row_width=1)

        btn_on = InlineKeyboardButton(
            text='✅ Bot turn ON',
            callback_data='setup_bot_on'
        )

        btn_off = InlineKeyboardButton(
            text='⛔️Bot turn OFF',
            callback_data='setup_bot_off'
        )

        if bot_status:
            btn_to_setup_bot.insert(btn_off)
        else:
            btn_to_setup_bot.insert(btn_on)
        btn_to_setup_bot.insert(self.btn_back_to_menu)

        return btn_to_setup_bot

    def btn_setup_users(self):
        """Keyboard settings for user."""
        users_list = db_users.get_list_of_users()
        btn_to_setup_bot = InlineKeyboardMarkup(row_width=3)
        for user in users_list:
            btn_info = InlineKeyboardButton(
                text=f'ℹ️{user}',
                callback_data=f'setup_user_info_{user}'
            )
            btn_change_invest = InlineKeyboardButton(
                text=f'⚙️invest',
                callback_data=f'setup_user_change_invest_{user}'
            )
            btn_delete = InlineKeyboardButton(
                text=f'❌delete ',
                callback_data=f'setup_user_delete_user_{user}'
            )
            btn_to_setup_bot.insert(btn_info)
            btn_to_setup_bot.insert(btn_change_invest)
            btn_to_setup_bot.insert(btn_delete)
        btn_to_setup_bot.insert(self.btn_back_to_menu)
        return btn_to_setup_bot

    def btn_config_strategy(self):
        """Keyboard to config strategy."""
        btn_config_strategy = InlineKeyboardMarkup(row_width=1)

        btn_nubmer_of_takes = InlineKeyboardButton(
            text='Setup strategy',
            callback_data='config_setup_strategy'
        )

        btn_config_strategy.insert(btn_nubmer_of_takes)
        btn_config_strategy.insert(self.btn_back_to_menu)

        return btn_config_strategy

    def btn_cancel(self):
        """Keyboard to cancel current move.."""
        kbd_cancel = InlineKeyboardMarkup(row_width=1)
        btn_cancel = InlineKeyboardButton(
            text='✖ Cancel',
            callback_data='cancel'
        )

        kbd_cancel.insert(btn_cancel)

        return kbd_cancel

    def admin_settings(self):
        """Keyboard to settings for admins."""
        kbd_admin = InlineKeyboardMarkup(row_width=1)

        btn_add_admin = InlineKeyboardButton(
            text='Add admin',
            callback_data='admin_settings_add'
        )
        btn_admins_list = InlineKeyboardButton(
            text='Admins list',
            callback_data='admin_settings_list'
        )
        btn_delete_admin = InlineKeyboardButton(
            text='Delete admin',
            callback_data='admin_settings_delete'
        )

        for btn in [btn_add_admin, btn_admins_list,
                    btn_delete_admin, self.btn_back_to_menu]:
            kbd_admin.insert(btn)

        return kbd_admin

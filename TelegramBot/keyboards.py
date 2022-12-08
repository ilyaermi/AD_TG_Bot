from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
        main_menu = InlineKeyboardMarkup(row_width=1)

        btn_order = InlineKeyboardButton(
            text='Заказать рекламу',
            callback_data='order_commercial'
        )
        btn_my_orders = InlineKeyboardButton(
            text='My orders',
            callback_data='my_orders'
        )
        btn_collaboration = InlineKeyboardButton(
            text=r'Сотрудничество\поддержка',
            callback_data='collaboration_support'
        )

        btn_list = [btn_order, btn_my_orders, btn_collaboration, ]

        for btn in btn_list:
            main_menu.insert(btn)

        return main_menu

    def regions(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.insert(InlineKeyboardButton(
            text='Россия', callback_data='select_region_Россия'))
        markup.insert(InlineKeyboardButton(text='Украина',
                      callback_data='select_region_Украина'))
        markup.insert(InlineKeyboardButton(text='Беларусь',
                      callback_data='select_region_Беларусь'))
        markup.insert(InlineKeyboardButton(text='Всё СНГ',
                      callback_data='select_region_Всё СНГ'))
        markup.insert(self.btn_back_to_menu)
        return markup

    def type_coms(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.insert(InlineKeyboardButton(
            text='Розыгрыш', callback_data='select_type_com_Розыгрыш'))
        markup.insert(InlineKeyboardButton(
            text='Проект', callback_data='select_type_com_Проект'))
        markup.insert(InlineKeyboardButton(
            text='Канал', callback_data='select_type_com_Канал'))
        markup.insert(InlineKeyboardButton(
            text='Бот', callback_data='select_type_com_Бот'))
        markup.insert(self.btn_back_to_menu)
        return markup

    def sections(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.insert(InlineKeyboardButton(
            text='Криптовалюты', callback_data='select_section_Криптовалюты'))
        markup.insert(InlineKeyboardButton(
            text='NFT', callback_data='select_section_NFT'))
        markup.insert(InlineKeyboardButton(
            text=r'Проекты\Абуз', callback_data=r'select_section_Проекты\Абуз'))
        markup.insert(InlineKeyboardButton(
            text='Новостной паблик', callback_data='select_section_Новостной паблик'))
        markup.insert(InlineKeyboardButton(
            text='Трейдинг', callback_data='select_section_Трейдинг'))
        markup.insert(InlineKeyboardButton(
            text='Майнинг', callback_data='select_section_Майнинг'))
        markup.insert(InlineKeyboardButton(
            text='Арбитраж', callback_data='select_section_Арбитраж'))
        markup.insert(InlineKeyboardButton(
            text='Ноды', callback_data='select_section_Ноды'))
        markup.insert(InlineKeyboardButton(
            text='Life', callback_data='select_section_Life'))
        markup.insert(InlineKeyboardButton(
            text='Смешанные', callback_data='select_section_Смешанные'))
        markup.insert(self.btn_back_to_menu)
        return markup

    def rates(self):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.insert(InlineKeyboardButton(
            text='Standart', callback_data='select_rate_Standart'))
        markup.insert(InlineKeyboardButton(
            text='Premium', callback_data='select_rate_Premium'))
        markup.insert(InlineKeyboardButton(
            text='VIP', callback_data='select_rate_VIP'))
        markup.insert(InlineKeyboardButton(
            text='Individual', callback_data='select_rate_Individual'))
        markup.insert(self.btn_back_to_menu)
        return markup

    def billing(self):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.row(InlineKeyboardButton(
            text='Связаться с поддержкой', callback_data='contact_suppport'))
        markup.insert(InlineKeyboardButton(
            text='BEP20', callback_data='select_billing_BEP20'))
        markup.insert(InlineKeyboardButton(
            text='TRC20', callback_data='select_billing_TRC20'))
        markup.row(self.btn_back_to_menu)
        return markup
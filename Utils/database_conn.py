import sqlite3 as sl
import config as cfg
from typing import Union
import os


class DatabaseConnector:
    """connector to database w/ users"""

    def __init__(self,):
        self.db = sl.connect(cfg.db_path, check_same_thread=False)
        self.cursor = self.db.cursor()

    def create_tables(self):
        """Creates table if not exists."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                                user_id int,
                                admin BOOLEAN,
                                verify BOOLEAN
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                                uid_order TEXT,
                                user_id int,
                                region TEXT,
                                type_com TEXT,
                                section TEXT,
                                rate TEXT,
                                billing TEXT,
                                pay BOOLEAN,
                                active BOOLEAN
                                )''')
        self.db.commit()

    def execute_db(self, list_args: Union[list[str], list[str, list]]):
        ans = self.cursor.execute(*list_args).fetchall()
        self.db.commit()
        return ans


db = DatabaseConnector()
db.create_tables()
# db_bot_switch = BotSwitch(f'{homeDir}/DBs/bot_switch.db')
# db_settings.update_table(
#     {'name': 'name3', 'tp': '3', 'tp_conditions': '2', 'tp_qty': '30', 'sl': '3', 'move_stop': 'Yes',
#      'move_stop_condition': '1', 'move_stop_price': '3'})

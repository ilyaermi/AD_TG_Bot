import sqlite3
import os
from datetime import datetime
from typing import Union
from dataclasses import dataclass
import uuid6
# INTEGER PRIMARY KEY AUTOINCREMENT
import config as cf


@dataclass
class DbUsers:
    connect: sqlite3.Connection
    cur: sqlite3.Cursor

    async def get_user_by_tg_id(self, user_id: int) -> tuple:
        values = self.cur.execute(
            "SELECT * FROM user WHERE user_id=?", [user_id]).fetchone()
        try:
            return values
        except:
            self.cur.execute(
                'INSERT INTO user VALUES(?,?)', [user_id, False])
            self.connect.commit()
            return (user_id, False)

    async def add_admins(self, list_users: list[int]) -> None:
        for user_id in list_users:
            ans = self.cur.execute(
                "SELECT * FROM user WHERE user_id=?", [user_id]).fetchall()
            if len(ans) != 0:
                self.cur.execute(
                    "UPDATE user SET admin = ? WHERE user_id=?", [True, user_id]).fetchall()
            else:
                self.cur.execute(
                    'INSERT INTO user VALUES(?,?)', [user_id, True])
        self.connect.commit()


@dataclass
class DbOrders:
    connect: sqlite3.Connection
    cur: sqlite3.Cursor

    async def get_orders(self, user_id: int) -> tuple[tuple]:
        ans = self.cur.execute(
            'SELECT * FROM order WHERE user_id=?', [user_id])
        return ans


class FullBd:
    def __init__(self) -> None:
        self.connect = sqlite3.connect(cf.db_path)
        self.cur = sqlite3.Cursor(self.connect)
        self.create_full_bd()
        self.db_users = DbUsers(self.connect, self.cur)
        self.db_orders = DbOrders(self.connect, self.cur)

    def create_table_users(self,) -> None:
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS user (
                                                user_id int,
                                                admin BOOLEAN)
                                                ''')

    def create_table_orders(self,) -> None:
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS order (
                                                user_id int
                                                region varchar(40),
                                                type_com varchar(40),
                                                section varchar(40),
                                                rate varchar(40))
                                                ''')

    def create_full_bd(self,) -> None:
        self.create_table_users()
        self.connect.commit()


bd = FullBd()
bd.create_full_bd()

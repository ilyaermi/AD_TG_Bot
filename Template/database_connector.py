import sqlite3 as sl


class UsersDatabaseConnector:
    """connector to database w/ users"""
    def __init__(self, db_file):
        self.db = sl.connect(db_file)
        self.cursor = self.db.cursor()

    def create_table(self):
        """Creates table if not exists."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                                account_name TEXT,
                                api_key TEXT,
                                api_secret TEXT,
                                invest_procent TEXT
                                )''')
        self.db.commit()

    def create_new_user(self, data):
        """Creates new user."""
        try:
            self.cursor.execute(f'''INSERT INTO accounts VALUES 
                        ('{data['frendly_name']}', '{data['api_key']}', '{data['api_secret']}', '{data['invest_procent']}')''')
            self.db.commit()
        except Exception as err:
            print(err)

    def get_list_of_users(self):
        """Returns list of users."""
        self.cursor.execute('''SELECT * FROM accounts''')
        data = self.cursor.fetchall()
        accounts_list = []
        for el in data:
            accounts_list.append(el[0])
        return accounts_list

    def get_users_all_data(self):
        """Returns all users data."""
        self.cursor.execute('''SELECT * FROM accounts''')
        data = self.cursor.fetchall()

        return data

    def delete_user(self, account_name):
        """Delete user by name."""
        self.cursor.execute(f"DELETE FROM accounts WHERE account_name = '{account_name}'")
        self.db.commit()

    def get_users_info(self, account_name):
        """Returns user info by name."""
        self.cursor.execute(f'''SELECT * FROM accounts WHERE account_name = "{account_name}"''')
        data = self.cursor.fetchone()

        return data

    def change_invest_for_user(self, account_name, invest_procent):
        """Change invest procent for user by name."""
        self.cursor.execute(
            f'''UPDATE accounts set invest_procent = "{invest_procent}" WHERE account_name = "{account_name}" ''')
        self.db.commit()


class BotConfiguration:
    """Connector to configuration."""
    def __init__(self, db_file):
        self.db = sl.connect(db_file)
        self.cursor = self.db.cursor()

    def create_table(self):
        """ creates table if not exists """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bot_config (
                                take INTEGER DEFAULT 2,
                                breakeven BOOLEAN DEFAULT FALSE, 
                                qty_reduce REAL DEFAULT 0.33
                                )''')
        self.db.commit()
        # qty_reduce_per_order REAL

    def get_strategy(self):
        """Returns current strategy"""
        self.cursor.execute("""SELECT * FROM bot_config""")
        res = self.cursor.fetchall()

        return res

    def update_table(self, data: list):
        """Change strategy by list"""
        self.cursor.execute('''DELETE FROM bot_config''')
        for el in data:
            self.cursor.execute(f'''INSERT INTO bot_config VALUES ({int(el[0])}, {bool(el[1])}, {float(el[2])})''')
        self.db.commit()


class AdminDatabaseConnector:
    """Connector to admins database."""
    def __init__(self, db_file):
        self.db = sl.connect(db_file)
        self.cursor = self.db.cursor()

    def create_table(self):
        """Creates table if not exists."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                                user_id TEXT PRIMARY KEY
                                )''')
        self.db.commit()

    def get_admins_list(self):
        """Returns admins list."""
        self.cursor.execute('''SELECT * FROM admins''')
        data = self.cursor.fetchall()
        return data

    def add_admin(self, user_id):
        """Add new admin."""
        self.cursor.execute(f'''INSERT INTO admins VALUES ('{user_id}')''')
        self.db.commit()

    def delete_admin(self, user_id):
        """Delete admin by id."""
        self.cursor.execute(f"DELETE FROM admins WHERE user_id = '{user_id}'")
        self.db.commit()


class BotSwitch:
    """Here will be one var, where will be info about bot ON, or bot OFF"""

    def __init__(self, db_file):
        self.db = sl.connect(db_file)
        self.cursor = self.db.cursor()

    def create_table(self):
        """ creates table if not exists """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bot (status BOOLEAN)''')
        self.db.commit()

    def bot_status(self):
        """Return bot status, default None, so we need to make it False befor
        return."""
        try:
            self.cursor.execute('''SELECT status FROM bot''')
            data = self.cursor.fetchone()[0]
            if data is None:
                self.insert_bot(value=False)
                self.bot_status()
            else:
                return data
        except TypeError:
            self.insert_bot(value=False)
            self.bot_status()

    def insert_bot(self, value: bool):
        """Insert new line."""
        self.cursor.execute(f'''INSERT INTO bot VALUES ( {value})''')
        self.db.commit()

    def change_bot_status(self, value: bool):
        """Change bot status."""
        self.cursor.execute(f'''UPDATE bot set status = {value}''')
        self.db.commit()


db_users = UsersDatabaseConnector('../DBs/users.db')
db_settings = BotConfiguration('../DBs/settings.db')
db_admin = AdminDatabaseConnector('../DBs/admins.db')
db_bot_switch = BotSwitch('../DBs/bot_switch.db')
for db in [db_users, db_settings, db_admin, db_bot_switch]:  # Create tables for all connectors if not exist.
    db.create_table()

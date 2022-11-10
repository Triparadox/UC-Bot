# Importing modules
import sqlite3
import os
import random
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        # Initialize database connection
        self.connection = sqlite3.connect(os.path.dirname(os.getcwd()) +
                                          '\\Database\\ucgroup_data.db')
        self.db_cursor = self.connection.cursor()

    def increment_xp(self, account_id, xp_amount):
        # Increment user XP by certain amount
        print(account_id)
        self.db_cursor.execute("""SELECT ACCOUNT_XP, LAST_UPDATE FROM 
        ACCOUNT_LEVEL WHERE 
        ACCOUNT_ID = ?
        """, (account_id, ))
        query_result = self.db_cursor.fetchone()

        if query_result:
            # ACCOUNT_LEVEL data exists, check LAST_UPDATE
            current_xp, last_update = query_result
            current_time = datetime.strptime(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            last_update_time = datetime.strptime(last_update, '%Y-%m-%d '
                                                              '%H:%M:%S')
            elapsed_time = current_time - last_update_time
            if elapsed_time.total_seconds() >= 10:
                # Calculate new ACCOUNT_XP amount
                new_xp_amount = current_xp + xp_amount
                # Push update to ACCOUNT_XP
                self.db_cursor.execute("""UPDATE ACCOUNT_LEVEL SET 
                ACCOUNT_XP = 
                            ?, LAST_UPDATE = ? WHERE ACCOUNT_ID = ?
                            """, (new_xp_amount, str(current_time),
                                  account_id))
                self.connection.commit()
            else:
                # XP is not granted to avoid frequent spam
                pass
        else:
            # ACCOUNT_LEVEL data does not exist, create ACCOUNT_LEVEL data
            current_time = datetime.strptime(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            self.db_cursor.execute("""INSERT INTO ACCOUNT_LEVEL VALUES(?, ?, ?)
            """, (account_id, xp_amount, str(current_time)))
            self.connection.commit()

    def check_level(self, account_id):
        # Find user data
        self.db_cursor.execute("""SELECT ACCOUNT_XP FROM ACCOUNT_LEVEL WHERE 
        ACCOUNT_ID = ?""", (account_id, ))
        xp_amount, = self.db_cursor.fetchone()

        # Calculate the user's level and progress to next level
        base_xp_requirement = 100
        level = 1
        while xp_amount > 0:
            xp_amount = xp_amount - base_xp_requirement
            if xp_amount < 0:
                xp_amount += base_xp_requirement
                break
            base_xp_requirement = int(base_xp_requirement * 1.25)
            level = level + 1

        return (level, xp_amount, base_xp_requirement)

    def daily_bonus(self, account_id):
        # Find user data
        self.db_cursor.execute("""SELECT ACCOUNT_BALANCE, 
        DAILY_BONUS_LAST_CLAIMED FROM ACCOUNT_ECONOMY WHERE ACCOUNT_ID = 
        ?""", (account_id, ))
        query_result = self.db_cursor.fetchone()

        if query_result:
            # ACCOUNT_ECONOMY data exists, check last claimed time
            account_balance, last_update = query_result
            current_time = datetime.strptime(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            last_update_time = datetime.strptime(last_update, '%Y-%m-%d '
                                                              '%H:%M:%S')
            elapsed_time = current_time - last_update_time
            if elapsed_time.total_seconds() >= 86400:
                # Grant daily bonus
                bonus_amount = random.randint(1, 10)
                account_balance = account_balance + bonus_amount
                current_time = datetime.strptime(datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                # Push update to ACCOUNT_BALANCE
                self.db_cursor.execute("""UPDATE ACCOUNT_ECONOMY SET 
                ACCOUNT_BALANCE = ? , DAILY_BONUS_LAST_CLAIMED = ? WHERE 
                ACCOUNT_ID = ?""", (account_balance, current_time, account_id))
                self.connection.commit()
                return 1, bonus_amount
            else:
                # Daily bonus is granted once every 24 hours only
                return 0, 0
        else:
            # ACCOUNT_ECONOMY data does not exist, create ACCOUNT_ECONOMY data
            bonus_amount = random.randint(1, 10)
            current_time = datetime.strptime(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
            self.db_cursor.execute("""INSERT INTO ACCOUNT_ECONOMY VALUES(?, 
            ?, ?)
            """, (account_id, bonus_amount, current_time))
            self.connection.commit()
            return 1, bonus_amount

    def get_balance(self, account_id):
        # Find user data
        self.db_cursor.execute("""SELECT ACCOUNT_BALANCE FROM 
        ACCOUNT_ECONOMY WHERE ACCOUNT_ID = ?""", (account_id, ))
        account_balance, = self.db_cursor.fetchone()

        return account_balance,

DATABASE_MANAGER = None


def get_database_manager():
    global DATABASE_MANAGER
    if DATABASE_MANAGER:
        return DATABASE_MANAGER
    else:
        DATABASE_MANAGER = DatabaseManager()
        return DATABASE_MANAGER
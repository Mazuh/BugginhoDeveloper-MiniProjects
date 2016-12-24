""" Lib to manage an ATM (Automatic Teller Machine).
Important classes: User, Persistence.
"""

from decimal import Decimal
import hashlib
import sqlite3
import os

from datetime import datetime

class User(object):
    """ Bank user. Can log in and do stuff or just act as a passive object.
    Another class must be used to persist these instances in local storage. """

    ACTIONS = { # for later registration in history attribute
        'TRANSFERING' : 'transfered', # money transfering between two users
        'WITHDRAWING' : 'withdrawed', # withdraw own money
        'RECEIVING' : 'received an amount of', # receiving money from anyone/anywhere
    }

    __agency = ''
    __account = ''
    __password = '' # md5
    __balance = 0
    __history = []

    __is_logged_in = False # must not be persisted



    def __init__(self, agency, account, password, balance=None, history=None):
        """ Constructor. Limited actions while it's not logged in.

        Args:
            agency   (str): Agency identification code.
            account  (str): Account identification code.
            password (str): Password MD5 hash, put None if it's unknown.
            balance  (num): Balance in R$, put None if it's unknown.
            history (list): A list of tuples representing balance transaction records,
                            put None if it's unknown or empty.
                            List format: [(register string, True if it's a saved register), ...]
        """
        self.__agency = agency
        self.__account = account
        self.__password = password

        if balance is not None:
            self.__balance = balance

        if history is not None:
            self.__history = history



    def log_in(self, password_str):
        """ Access this existent bank account, authenticating by this password string.

        Args:
            password_str (str): A password in natural language.

        Returns:
            bool: True if it was successfully authenticated, False otherwise.

        """
        self.__is_logged_in = self.__password == self.str_to_hash(password_str)
        return self.__is_logged_in



    def log_out(self):
        """ Exit this bank account, ie, removes active rights to do some stuff. """
        self.__is_logged_in = False



    def deposit(self, amount, another_user=None):
        """ Deposit cash in this account or in another user's account.
        If something goes wrong, a fatal error will be triggered.

        Args:
            amount        (num): amount of cash in R$ to deposit.
            another_user (User): if it's depositing in another user account then
                                 put its instance here, otherwise leave it as None.

        Returns:
            bool: True if operations has been a success ('unreturned' error otherwise).

        """
        if another_user:
            another_user.deposit(amount)
            self.register_operation(self.ACTIONS['RECEIVING'], amount)
            self.register_operation(self.ACTIONS['TRANSFERING'], amount, another_user)
        else:
            self.__balance = float(Decimal(str(self.__balance + amount)))
            self.register_operation(self.ACTIONS['RECEIVING'], amount)

        return True # False is never reached



    def transfer_to(self, amount, another_user):
        """ Transfer an amount of cash from this user to another one.
        This instance must have enough balance to do so.
        This is a private method, that requires previous authentication.

        Args:
            amount       (num): Cash in R$ to discount from this instance user
                                and to increase in another user account.
            another_use (User): Another use to receive this transfering amount of cash.

        Returns:
            bool: True if cash has been transfered from this instance to another, False otherwise.

        """
        if self.__balance >= amount and self.__is_logged_in:
            self.__balance = float(Decimal(str(self.__balance - amount)))
            another_user.deposit(amount)
            self.register_operation(self.ACTIONS['TRANSFERING'], amount, another_user)
            return True

        return False



    def withdraw_cash(self, qtt_100s, qtt_50s, qtt_20s):
        """ Withdraw cash. Those args should be obtained throught options_to_withdraw function.
        Also, there are two limits: R$1000,00 or the balance (the lower one).
        This is a private method, that requires previous authentication.

        Args:
            qtt_100s (int): quantity of 100-real bills
            qtt_50s  (int): quantity of 50-real bills
            qtt_20s  (int): quantity of 20-real bills

        Returns:
            bool: True if the cash has been withdraw, False otherwise.

        """
        amount = PaperMoneyCounter().cash(qtt_100s, qtt_50s, qtt_20s)
        if (self.__is_logged_in) and (amount <= self.__balance) and (amount <= 1000):
            self.__balance = float(Decimal(str(self.__balance - amount)))
            self.register_operation(self.ACTIONS['WITHDRAWING'], amount)
            return True

        return False



    def options_to_withdraw(self, amount):
        """ Check options to withdraw an amount of cash. Can't be more than R$1000,00 and
        should be 'printed' in 20, 50 and/or 100-real bills.

        Args:
            amount (num): Desired amount of cash to withdraw.

        Returns:
            None: If the requirements to withdraw weren't accomplished.
            list: If the requeriments to withdraw were accomplished, a list in format
                  [[a, b, c], ...], where each sublist is an option to withdraw cash,
                  and reading as a: quantity of 100s, b: quantity of 50s,
                  c: quantity of 20-real bills available and a,b,c are int.

        """
        counter = PaperMoneyCounter() # aux class
        options = [] # options to withdraw
        remaining_cash = 0 # aux var

        if (amount % 20 == 0 or amount % 50 == 0) and (amount <= 1000): # is it allowed to withdraw?
            # prioritizing 100-real bills
            qtt_100s = counter.how_many_100s(amount)
            remaining_cash = counter.remaining_cash_without_100s(amount)

            qtt_50s = counter.how_many_50s(remaining_cash)
            remaining_cash = counter.remaining_cash_without_50s(remaining_cash)

            qtt_20s = counter.how_many_20s(remaining_cash)
            remaining_cash = counter.remaining_cash_without_20s(remaining_cash)

            if counter.cash(qtt_100s, qtt_50s, qtt_20s) == amount:
                options.append([int(qtt_100s), int(qtt_50s), int(qtt_20s)])

            # prioritizing 50-real bills
            qtt_100s = 0

            qtt_50s = counter.how_many_50s(amount)
            remaining_cash = counter.remaining_cash_without_50s(amount)

            qtt_20s = counter.how_many_20s(remaining_cash)
            remaining_cash = counter.remaining_cash_without_20s(remaining_cash)

            if counter.cash(qtt_100s, qtt_50s, qtt_20s) == amount:
                if not(options[0] == [qtt_100s, qtt_50s, qtt_20s]):
                    options.append([int(qtt_100s), int(qtt_50s), int(qtt_20s)])

            # prioritizing 20-real bills
            qtt_100s = 0

            qtt_50s = 0

            qtt_20s = counter.how_many_20s(amount)

            if counter.cash(qtt_100s, qtt_50s, qtt_20s) == amount:
                if not(options[0] == [qtt_100s, qtt_50s, qtt_20s]):
                    if not(options[1] == [qtt_100s, qtt_50s, qtt_20s]):
                        options.append([int(qtt_100s), int(qtt_50s), int(qtt_20s)])

            return options

        return None # it wasn't allowed to withdraw



    def register_operation(self, action, amount, user_to=None):
        """ Register an operation, that this user is executing, in its own history list.

        Args:
            action   (str): An adequate value from ACTIONS dictionary attribute.
            amount   (num): Amount of money being moved in this operation.
            user_to (User): Another user as a target, eg: transfering money from this
                            user to this argumented user.

        Returns:
            str: Builded operation string added to this user history,
                 in format 'd/m/a - [account]/[agency] [action] R$[amount]'
                 or 'd/m/a - [account1]/[agency1] [action] R$[amount] to [account2]/[agency2]'.

        """
        now = datetime.now()

        register = str(now.day) + "/" + str(now.month) + "/" + str(now.year) + ' - '
        register += self.__account + '/' + self.__agency
        register += ' ' + action + ' R$' + str(amount)

        if user_to:
            register += ' to ' + user_to.get_account() + '/' + user_to.get_agency()

        self.__history.append((register, False))
        return register



    def append_register(self, register):
        """ Append an already saved register to this user's history.

        Args:
            register (tuple): an item to append in history attribute that, following
                              construct format, was already been saved.

        Returns:
            bool: True if has been appended, False otherwise.

        """
        register_str, is_saved = register # pylint: disable=I0011,W0612

        if is_saved:
            self.__history.append(register)
            return True

        return False



    def str_to_hash(self, param):
        """ Generate a hash of a string param using md5 algorithm

        Args:
            param (str): The content string for hashing.

        Returns:
            str: A hash, generated by a md5 algorithm, using the parameter.

        """
        param = param.encode('utf-8')
        my_hash = hashlib.md5(param)
        return my_hash.hexdigest()



    def hash_password(self):
        """ Hashes the password of this instance
        (but... it's supposed to be already hashed!). """
        self.__password = self.str_to_hash(self.__password)



    def is_logged_in(self):
        """ Check if user has been authenticated.

        Returns:
            bool: True if is logged in, False otherwise.
        """
        return self.__is_logged_in



    def get_balance(self):
        """ Consult balance in R$.

        Returns:
            num: This user's balance, None for unauthorized operation.
        """
        if self.is_logged_in:
            return self.__balance
        else:
            return None



    def get_agency(self):
        """ Get agency id.

        Returns:
            str: User's agency.
        """
        return self.__agency



    def get_account(self):
        """ Get account id.

        Returns:
            str: User's account.
        """
        return self.__account



    def get_history(self):
        """ Get history of user's transactions.

        Returns:
            list: Just a copy of User's history in constructed format.
        """
        return self.__history[:]

# ..............................................................


class PaperMoneyCounter(object):
    """ Can do some counts about paper money. Aux class. """

    def cash(self, qtt_100s, qtt_50s, qtt_20s):
        """ Return how much money there is by assembling 100s, 50s and 20-real bills quantities.
        """
        return (qtt_100s * 100) + (qtt_50s * 50) + (qtt_20s * 20)



    def how_many_100s(self, amount):
        """ Return how many 100-real bill can be printed from this amount of cash.
        """
        return amount // 100



    def remaining_cash_without_100s(self, amount):
        """ Return how much cash remains after using a maximum quantity of 100-real bills.
        """
        return amount % 100



    def how_many_50s(self, amount):
        """ Return how many 50-real bill can be printed from this amount of cash.
        """
        return amount // 50



    def remaining_cash_without_50s(self, amount):
        """ Return how much cash remains after using a maximum quantity of 50-real bills.
        """
        return amount % 50



    def how_many_20s(self, amount):
        """ Return how many 20-real bill can be printed from this amount of cash.
        """
        return amount // 20



    def remaining_cash_without_20s(self, amount):
        """ Return how much cash remains after using a maximum quantity of 20-real bills.
        """
        return amount % 20


# ..............................................................


class Persistence(object):
    """ Data manager for ATM bank accounts. """

    __DB = 'users.db'

    __users = {}


    def __init__(self):
        """ Create an instance of Persistence, and also try to execute
        an initial script for db installation. """
        if not self.is_installed():
            self.install()
        else:
            self.load_users()



    def install(self):
        """ Initialize database, create tables and add few rows. """
        conn = sqlite3.connect(self.__DB)
        cursor = conn.cursor()

        # creating tables...

        cursor.execute('''
        CREATE TABLE users (
            id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            agency   TEXT NOT NULL,
            account  TEXT NOT NULL,
            password TEXT NOT NULL,
            balance  REAL NOT NULL
        );
        ''')

        cursor.execute('''
        CREATE TABLE history (
            id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            register TEXT NOT NULL,
            owner    INTEGER NOT NULL
        );
        ''')

        # inserting a few users by default (there's no 'sign up' requirement for this app)...

        hasher = User('', '', '')
        users_data = [
            ('A1', '00000-0', hasher.str_to_hash('pass0'), 1500),
            ('A1', '11111-1', hasher.str_to_hash('pass1'), 400),
            ('A2', '22222-2', hasher.str_to_hash('pass2'), 260),
            ('A3', '33333-3', hasher.str_to_hash('pass3'), 380),
            ('A2', '44444-4', hasher.str_to_hash('pass4'), 240),
        ]

        cursor.executemany('''
        INSERT INTO users (agency, account, password, balance)
        VALUES (?, ?, ?, ?);
        ''', users_data)

        conn.commit()
        conn.close()

        self.load_users()



    def is_installed(self):
        """ Returns: True if database file already exists, False otherwise.
        Doesn't guarantee that this file really is a database, ie, a valid file. """
        return os.path.isfile(self.__DB)



    def update_users(self):
        """ Update all current users balance and history in database using list attribute.
        There's basically no security against SQL injection, due to there's no espected
        input string (the existents here are auto builded by this script using numeric inputs) """
        conn = sqlite3.connect(self.__DB)
        cursor = conn.cursor()

        users_data = []
        unsaved_histories_data = []
        for key, user in self.__users.items(): # here, key it's actually users id
            users_data.append((user.get_balance(), key))
            for register in user.get_history():
                register_str, is_saved = register
                if not is_saved:
                    unsaved_histories_data.append((register_str, key))

        cursor.executemany('''
        UPDATE users
        SET balance=?
        WHERE id=?;
        ''', users_data)

        cursor.executemany('''
        INSERT INTO history (register, owner)
        VALUES (?, ?);
        ''', unsaved_histories_data)

        conn.commit()
        conn.close()

        self.load_users() # REALOADING!!! Pew, pew, pew, pew, pew...



    def load_users(self):
        """ Load all database rows and put their data in list attribute. """
        self.__users = {}

        conn = sqlite3.connect(self.__DB)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM users;
        ''')

        for row in cursor.fetchall():
            self.__users[row[0]] = User(row[1], row[2], row[3], row[4])

        cursor.execute('''
        SELECT * FROM history;
        ''')

        for row in cursor.fetchall():
            self.__users[row[2]].append_register((row[1], True))

        conn.close()



    def find_user(self, agency=None, account=None):
        """ Search for a registered user with these BOTH matching agency and account attributes.
        Don't worry about SQL injection, this searching is executed withing already loaded users,
        so there's no use of SQL here.

        Args:
            agency (str): Agency name of wanted user (recomended: use upper case only).
            account (str): Account name of wanted user (recommended: use upper case only).

        Returns:
            User: Found user, or None if there's no matching user.

        """
        if agency is None or account is None:
            return None

        for i in self.__users:
            user = self.__users[i]
            if user.get_agency() == agency and user.get_account() == account:
                return self.__users[i]

        return None

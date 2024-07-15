import os
from datetime import datetime
from random import randint

import bcrypt
import psycopg2
import pwinput as pin

# SQL CODE:

# CREATE TABLE IF NOT EXISTS UserDetails (
#     acc_no SERIAL PRIMARY KEY,
#     name VARCHAR(100),
#     age INT,
#     address TEXT,
#     balance DECIMAL(10, 2),
#     date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     phone_number VARCHAR(15),
#     user_name VARCHAR(50) UNIQUE NOT NULL,
#     password VARCHAR(255) NOT NULL
# );
#


class Account:
    """
    Manages the Account Information of a Client
    """

    def __init__(
        self,
        account_number=None,
        name=None,
        age=None,
        address=None,
        balance=0.0,
        date_created=None,
        phone_number=None,
        user_name=None,
        password=None,
    ):
        self.account_number = account_number
        self.name = name
        self.age = age
        self.address = address
        self.balance = balance
        self.date_created = date_created if date_created else datetime.now()
        self.phone_number = phone_number
        self.user_name = user_name
        self.password = password
        self.postgres_db_password = os.getenv("POSTGRESQL_PASSWORD")

    def open_account(
        self,
        name: str,
        age: int,
        address: str,
        phone_number: str,
        user_name: str,
        password: str,
    ) -> str:
        self.name = name
        self.age = age
        self.address = address
        self.balance = 0  # Default balance is 0 at sign up
        self.date_created = datetime.now()  # Date & Time Client's account was open
        self.phone_number = phone_number  # Client's Phone Number
        self.user_name = user_name  # Client's Username
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        )  # Hashed Password

        # Database Settings
        postgres_db_password = os.getenv("POSTGRESQL_PASSWORD")

        conn = None
        cur = None
        try:
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                host="localhost",
                dbname="Banking",
                user="postgres",
                password=postgres_db_password,
                port=5432,
            )
            cur = conn.cursor()

            # SQL query to insert a new record into the UserDetails table
            insert_script = """
            INSERT INTO UserDetails (name, age, address, balance, date_created, phone_number, user_name, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_values = (
                self.name,
                self.age,
                self.address,
                self.balance,
                self.date_created,
                self.phone_number,
                self.user_name,
                self.password.decode("utf-8"),
            )

            # Execute the SQL query
            cur.execute(insert_script, insert_values)
            conn.commit()

            print("Account opened successfully!")
            return f"Account opened successfully with Account Number: {self.account_number}"

        except Exception as error:
            print(f"Error: {error}")
            return f"Failed to open account: {error}"

        finally:
            # Close the cursor and connection
            if cur:
                cur.close()
            if conn:
                conn.close()

    def sign_in(self, user_name, password) -> bool:

        # Database Settings
        postgres_db_password = os.getenv("POSTGRESQL_PASSWORD")

        conn = None
        cur = None
        try:
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                host="localhost",
                dbname="Banking",
                user="postgres",
                password=postgres_db_password,
                port=5432,
            )
            cur = conn.cursor()

            # SQL query to retrieve password hash
            select_script = """
                SELECT password
                FROM UserDetails
                WHERE user_name = %s;
            """

            cur.execute(select_script, (user_name,))
            stored_password = cur.fetchone()

            if stored_password and bcrypt.checkpw(
                password.encode("utf-8"), stored_password[0].encode("utf-8")
            ):
                print("Signed In")
                return True
            else:
                print("Unable to Sign In")
                return False

        except Exception as error:
            print(f"Error: {error}")
            return False

        finally:
            # Close the cursor and connection
            if cur:
                cur.close()
            if conn:
                conn.close()

    def deposit(self, user_name: str, password: str, amount: float) -> str:
        user_is_authenticated = self.sign_in(user_name, password)

        if user_is_authenticated:

            conn = None
            cur = None
            updated_balance = None

            try:
                conn = psycopg2.connect(
                    host="localhost",
                    dbname="Banking",
                    user="postgres",
                    password=self.postgres_db_password,
                    port=5432,
                )

                cur = conn.cursor()
                selet_balance_script = """
                    SELECT balance
                    FROM userdetails
                    WHERE user_name = %s;
                    """
                insert_values = (user_name,)
                cur.execute(selet_balance_script, insert_values)
                current_balance = float(cur.fetchone()[0])

                update_script = """
                    UPDATE userdetails
                    SET balance = %s
                    WHERE user_name = %s;
                    """
                updated_balance = amount + current_balance
                insert_values = (updated_balance, user_name)

                cur.execute(update_script, insert_values)

                conn.commit()

            except Exception as error:
                print(f"Error: {error}")

            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
                return f"{amount} was added to user account!\nYour current balance is {updated_balance}"

        return "Wrong credentials were provided hence your balance can't be updated!"

    def withdraw(self, amount: float) -> str:
        pass


# name: str = input("Enter your name: ")
# age: int = int(input("Enter your age: "))
# address = input("Address: ")
# phone_number = input("Enter phone number: ")
# user_name = input("Enter your username: ")
# password = pin.pwinput("Enter your password: ", "🍌")

# mannys_account = Account()
# mannys_account.open_account(name, age, address, phone_number, user_name, password)


user_name = input("Enter your username: ")
password = pin.pwinput("Enter your password: ", ".")
balance = float(input("Enter amount: "))

mannys_account = Account()

print(mannys_account.deposit(user_name, password, balance))

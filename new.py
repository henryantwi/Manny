import os
from datetime import datetime
from random import randint
import bcrypt
import psycopg2

class Account:
    """
    Manages the Account Information of a Client 
    """
    
    def __init__(self, account_number=None, name=None, age=None, address=None, balance=0.0, date_created=None, phone_number=None, user_name=None, password=None):
        self.account_number = account_number
        self.name = name
        self.age = age
        self.address = address
        self.balance = balance
        self.date_created = date_created if date_created else datetime.now()
        self.phone_number = phone_number
        self.user_name = user_name
        self.password = password

    def open_account(self, name: str, age: int, address: str, phone_number: str, user_name: str, password: str) -> str:
        self.name = name
        self.age = age
        self.address = address
        self.balance = 0  # Default balance is 0 at sign up
        self.date_created = datetime.now()  # Date & Time Client's account was open
        self.phone_number = phone_number  # Client's Phone Number
        self.user_name = user_name  # Client's Username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hashed Password

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
                self.password.decode('utf-8'),
            )
            
            my_list = (1, 2, 3)

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

    def authenticate(self, user_name: str, password: str) -> bool:
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

            if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0].encode('utf-8')):
                return True
            else:
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

    def deposit(self, user_name: str, amount: float) -> str:
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

            # SQL query to update the balance
            update_script = """
            UPDATE UserDetails
            SET balance = balance + %s
            WHERE user_name = %s;
            """
            cur.execute(update_script, (amount, user_name))
            conn.commit()

            print("Deposit successful!")
            return "Deposit successful!"

        except Exception as error:
            print(f"Error: {error}")
            return f"Failed to deposit: {error}"

        finally:
            # Close the cursor and connection
            if cur:
                cur.close()
            if conn:
                conn.close()

    def withdraw(self, user_name: str, amount: float) -> str:
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

            # Check current balance
            select_script = """
            SELECT balance
            FROM UserDetails
            WHERE user_name = %s;
            """
            cur.execute(select_script, (user_name,))
            current_balance = cur.fetchone()[0]

            if current_balance < amount:
                print("Insufficient funds!")
                return "Insufficient funds!"

            # SQL query to update the balance
            update_script = """
            UPDATE UserDetails
            SET balance = balance - %s
            WHERE user_name = %s;
            """
            cur.execute(update_script, (amount, user_name))
            conn.commit()

            print("Withdrawal successful!")
            return "Withdrawal successful!"

        except Exception as error:
            print(f"Error: {error}")
            return f"Failed to withdraw: {error}"

        finally:
            # Close the cursor and connection
            if cur:
                cur.close()
            if conn:
                conn.close()

    def check_balance(self, user_name: str) -> float:
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

            # SQL query to retrieve the balance
            select_script = """
            SELECT balance
            FROM UserDetails
            WHERE user_name = %s;
            """
            cur.execute(select_script, (user_name,))
            balance = cur.fetchone()[0]

            print(f"Current balance: {balance}")
            return balance

        except Exception as error:
            print(f"Error: {error}")
            return 0.0

        finally:
            # Close the cursor and connection
            if cur:
                cur.close()
            if conn:
                conn.close()

# Example usage
name = input("Enter your name: ")
age = int(input("Enter your age: "))
address = input("Enter your address: ")
phone_number = input("Enter your phone number: ")
user_name = input("Enter your username: ")
password = input("Enter your password: ")

account = Account()
account.open_account(name, age, address, phone_number, user_name, password)

# Deposit
account.deposit(user_name, 1000.0)

# Withdraw
account.withdraw(user_name, 500.0)

# Check Balance
account.check_balance(user_name)

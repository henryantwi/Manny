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

    def home_page(self) -> None:
        print("Welcome to the Banking System")
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            name = input("Enter your name: ") 
            age = int(input("Enter your age: "))
            address = input("Enter your address: ")
            phone_number = input("Enter your phone number: ")
            user_name = input("Enter your username: ")
            password = pin.pwinput("Enter your password: ", "🍌")
              
            self.sign_up(name, age, address, phone_number, user_name, password)
            self.home_page()
            
        elif choice == 2:
            user_name = input("Enter your username: ")
            password = pin.pwinput("Enter your password: ", "🔑")
            
            self.sign_in(user_name, password)
            
        elif choice == 3:
            print("Goodbye!")
            exit()
        
        else:
            print("Invalid Choice!")
            exit()

    def sign_up(
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

    def sign_in(self, user_name, password) -> None:
        self.user_name = user_name
        self.password = password

        # Database Settings
        postgres_db_password = os.getenv("POSTGRESQL_PASSWORD")
        self.user_name = user_name

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
                SELECT password, acc_no 
                FROM UserDetails
                WHERE user_name = %s;
            """

            cur.execute(select_script, (user_name,))
            stored_password = cur.fetchall()[0]
            hmm = cur.fetchone()
            print(hmm)
            
            self.account_number = stored_password[1]
            print(stored_password)

            if stored_password and bcrypt.checkpw(
                password.encode("utf-8"), stored_password[0].encode("utf-8")
            ):
                print("Signed In!")
                print(f"Welcome {user_name}")
                print(f"Your Account Number is: 00000130010{self.account_number}")
                
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Exit")
                
                choice = int(input("Enter your choice: "))
                
                if choice == 1:
                    amount = float(input("Enter amount: "))
                    self.deposit(amount)
                    
                elif choice == 2:
                    amount = float(input("Enter amount: ")) 
                    self.withdraw(amount)
                    
                elif choice == 3:
                    self.check_balance()
                    
                elif choice == 4:
                    print("Goodbye!")
                    exit()
                else:
                    print("Invalid Choice!")
                    exit()
                
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

    def deposit(self, amount: float) -> str:
        user_is_authenticated = self.sign_in(self.user_name, self.password)

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
                insert_values = (self.user_name,)
                cur.execute(selet_balance_script, insert_values)
                current_balance = float(cur.fetchone()[0])

                update_script = """
                    UPDATE userdetails
                    SET balance = %s
                    WHERE user_name = %s;
                    """
                updated_balance = amount + current_balance
                insert_values = (updated_balance, self.user_name)

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

    def check_balance(self) -> str:
        conn = psycopg2.connect(
            host="localhost",
            dbname="Banking",
            user="postgres",
            password=self.postgres_db_password,
            port=5432,
        )
    
        cur = conn.cursor()
    
        select_balance_script = """
            SELECT balance FROM userdetails WHERE user_name = %s;
            """
    
        cur.execute(select_balance_script, (self.user_name,))
    
        current_balance = cur.fetchone()[0]
    
        cur.close()
        conn.close()
    
        return f"Your current balance is: {current_balance}"
    

mannys_account = Account()
mannys_account.home_page()

import os
from datetime import datetime
import pwinput as pin

import bcrypt
from random import randint

import psycopg2


class Account:
    """
    Account Class
    """

    def __init__(self) -> None:
        self.date_created = None
        self.phone_number = None
        self.address = None
        self.username = None
        self.client_password = None
        self.sex = None
        self.age = None
        self.name = None
        self.balance: float = 0.00
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                dbname="Banking",
                user="postgres",
                password=os.getenv("POSTGRESQL_PASSWORD"),
                port=5432,
            )
        except Exception:
            print("There was a problem connecting to the database...")
            exit()

    def create_client(self):
        try:
            self.name: str = input("\nEnter fullname: ")
            self.age: str = input("Enter Age: ")
            self.address: str = input("Enter Address: ")
            self.phone_number: str = input("Enter phone number: ")
            self.date_created = datetime.now()
            password: str = pin.pwinput("Enter your password: ", "🔑")
            confirm_password: str = pin.pwinput("Confirm your password: ", "🔑")
            if password == confirm_password:
                self.client_password = bcrypt.hashpw(confirm_password.encode("utf-8"), bcrypt.gensalt())
            else:
                print("Wrong Password!\nTry Again")
                self.create_client()
            self.username: str = f"@bk_{self.name.split(" ")[0].lower()}{randint(10, 100)}"

            cur = self.conn.cursor()

            insert_script = """
                INSERT INTO clients(name, age, address, balance, date_created, phone_number, user_name, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            placeholders = (
                self.name,
                self.age,
                self.address,
                self.balance,
                self.date_created,
                self.phone_number,
                self.username,
                self.client_password.decode("utf-8"),
            )

            cur.execute(insert_script, placeholders)
            self.conn.commit()

            cur = self.conn.cursor()
            cur.execute(f"SELECT acc_no FROM clients WHERE user_name = '{self.username}';")

            print("Account Details\n-------------\n")
            print(f"Client Name: {self.name}\nUsername: {self.username}\nAccount_Number: {cur.fetchone()[0]}\nBalance: {self.balance}")

            return True

        except Exception as e:
            print(e)
            return False

import os
from datetime import datetime
from random import randint

import psycopg2


class Account:
    def __init__(self, name: str, age: int, address: str):
        self.__id = randint(1, 99)
        self.name = name
        self.age = age
        self.address = address
        self.balance = 0
        self.sex = "F"
        self.account_number = str(randint(100000, 999999))
        self.date_create = datetime.now()

    def sign_up(self):
        password = os.getenv("POSTGRESQL_PASSWORD")

        conn = psycopg2.connect(
            host="localhost",
            dbname="Banking",
            user="postgres",
            password=password,
            port=5432,
        )

        cur = conn.cursor()

        
        insert_script = 'INSERT INTO BankingFive ("ID", "NAME", "Age", "SEX", "Balance", "Address") ' 
        values = "VALUES ({}, '{}', {}, '{}', {}, '{}')".format(self.__id, self.name, self.age, self.sex, self.balance, self.address) 
        
        full_script = insert_script + values
    
        print(full_script)

        cur.execute(full_script)
        
        conn.commit()
        cur.close()
        conn.close()


name: str = input("Enter your name: ")
age: int = int(input("Enter your age: "))
address = input("Address: ")

mannys_account = Account(name, age, address)


mannys_account.sign_up()

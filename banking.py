from sql_queries import Account


class Banking(Account):
    """
    Banking System
    """

    def __init__(self):
        super().__init__()
        ...

    def sign_up(self):
        if self.create_client():
            print("Account creation success\nSign in with your credentials")
            self.sign_in()
        else:
            print("Account creation unsuccessful!")
        return self.home()

    def sign_in(self):
        if self.authenticate_client():
            print("\n1. Transfer Money")
            print("2. Make Withdrawal ")
            print("3. Check Account Balance")
            print("4. Deactivate Account")
            print("5. Exit")
            try:
                choice = int(input("Enter choice: "))

                if choice == 1:
                    self.make_transfer()
                elif choice == 2:
                    self.make_withdraw()
                elif choice == 3:
                    self.check_balance()
                elif choice == 4:
                    self.deactivate()
                elif choice == 5:
                    exit()
                else:
                    print("Invalid Input")
                    return self.sign_in()

            except ValueError:
                print("Invalid Input! Try Again")
                self.sign_in()
        self.sign_in()

    def make_deposit(self):
        ...

    def make_withdraw(self):
        ...

    def make_transfer(self):
        ...

    def check_balance(self):
        ...

    def view_account_details(self):
        ...

    def home(self):
        pass

    def deactivate(self):
        pass


if __name__ == "__main__":
    umat_bank = Banking()
    umat_bank.sign_in()

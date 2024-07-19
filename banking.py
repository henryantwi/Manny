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
            print("Account creation success")

    def sign_in(self):
        ...

    def make_deposit(self):
        ...

    def make_withdraw(self):
        ...

    def make_transfer(self):
        ...

    def view_account_details(self):
        ...


if __name__ == "__main__":
    umat_bank = Banking()
    umat_bank.sign_up()

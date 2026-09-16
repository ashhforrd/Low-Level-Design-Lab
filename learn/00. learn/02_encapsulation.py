class BankAccount:
    def __init__(
            self,
            owner: str,
            initial_balance: int = 0,
    ):
        self.owner = owner
        self.balance_value = 0
        self.balance = initial_balance

    @property
    def balance(self) -> int:
        return self.balance_value

    @balance.setter
    def balance(self, value: int) -> None:
        if value < 0:
            raise ValueError("Saldo tidak boleh negatif")

        self.balance_value = value

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Deposit harus lebih dari nol")

        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Penarikan harus lebih dari nol")

        if amount > self.balance:
            raise ValueError("Saldo tidak mencukupi")

        self.balance -= amount

    def show_summary(self) -> str:
        return f"{self.owner}: Rp{self.balance}"


if __name__ == "__main__":
    account = BankAccount("Budi", 100_000)

    account.deposit(50_000)
    account.withdraw(25_000)

    print(account.show_summary())

    account.balance = -1_000_000
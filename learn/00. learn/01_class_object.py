class BankAccount:
    def __init__(self, owner: str, balance: int = 0):
        self.owner = owner
        self.balance = balance

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
        return "f{self.owner}: Rp{self.balance}"

if __name__ == "__main__":
    budi_account = BankAccount("Budi", 100_000)
    sari_account = BankAccount("Sari")

    budi_account.deposit(50_000)
    budi_account.withdraw(25_000)

    sari_account.deposit(20_000)

    print(budi_account.show_summary())
    print(sari_account.show_summary())
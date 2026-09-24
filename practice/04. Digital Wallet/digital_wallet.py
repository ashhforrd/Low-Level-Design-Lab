class WalletAccount:
    def __init__(self, user_id: str, wallet_id: str) -> None:
        self.user_id = user_id
        self.wallet_id = wallet_id
        self.balance = 0

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero")

        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than zero")

        if self.balance < amount:
            raise ValueError("Insufficient balance")

        self.balance -= amount


class WalletSystem:
    def __init__(self) -> None:
        self.wallets: dict[str, WalletAccount] = {}

    def create_wallet(self, user_id: str, wallet_id: str) -> WalletAccount:
        if wallet_id in self.wallets:
            raise ValueError(f"Wallet with ID {wallet_id} already exist")

        user_has_wallet = any(wallet.user_id == user_id for wallet in self.wallets.values())

        if user_has_wallet:
            raise ValueError(
                f"User with ID {user_id} already has a wallet"
            )
        
        new_wallet = WalletAccount(user_id, wallet_id)
        self.wallets[wallet_id] = new_wallet

        return new_wallet

    def deposit(self, wallet_id: str, amount: int) -> None:
        wallet = self.wallets.get(wallet_id)

        if wallet is None:
            raise ValueError("Wallet doesn't exist")

        wallet.deposit(amount)

    def transfer(self, source_wallet_id: str, destination_wallet_id: str, amount: int) -> None:
        if source_wallet_id == destination_wallet_id:
            raise ValueError("Cannot transfer to the same wallet")
        
        source = self.wallets.get(source_wallet_id)
        destination = self.wallets.get(destination_wallet_id)

        if source is None:
            raise ValueError("Source wallet doesn't exist")
        if destination is None:
            raise ValueError("Destination wallet doesn't exist")

        source.withdraw(amount)
        destination.deposit(amount)

    def get_balance(self, wallet_id: str) -> int:
        wallet = self.wallets.get(wallet_id)

        if wallet is None:
            raise ValueError(f"Wallet with ID {wallet_id} doesn't exist")

        return wallet.balance


def main() -> None:
    system = WalletSystem()

    system.create_wallet("USER-1", "WALLET-1")
    system.create_wallet("USER-2", "WALLET-2")

    system.deposit("WALLET-1", 100_000)

    print(system.get_balance("WALLET-1"))
    print(system.get_balance("WALLET-2"))

    system.transfer(
        source_wallet_id="WALLET-1",
        destination_wallet_id="WALLET-2",
        amount=30_000,
    )

    print(system.get_balance("WALLET-1"))
    print(system.get_balance("WALLET-2"))

    try:
        system.transfer(
            source_wallet_id="WALLET-1",
            destination_wallet_id="WALLET-2",
            amount=100_000,
        )
    except ValueError as error:
        print(error)

    print(system.get_balance("WALLET-1"))
    print(system.get_balance("WALLET-2"))


if __name__ == "__main__":
    main()
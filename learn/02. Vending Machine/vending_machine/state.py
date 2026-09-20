from abc import ABC, abstractmethod


class VendingState(ABC):
    @abstractmethod
    def select_product(self, machine, product_id: str) -> None:
        pass

    @abstractmethod
    def insert_money(self, machine, amount: int) -> None:
        pass

    @abstractmethod
    def purchase(self, machine):
        pass

    @abstractmethod
    def cancel(self, machine):
        pass


class IdleState(VendingState):
    def select_product(self, machine, product_id):
        product = machine.products.get(product_id)

        if product is None:
            raise ValueError("Product Unavailable")

        if machine.stock.get(product_id, 0) <= 0:
            raise ValueError("Product is out of stock")

        machine.selected_product = product
        machine.state = SelectedState()

    def insert_money(self, machine, amount: int):
        raise ValueError("Select a product before inserting money")

    def purchase(self, machine):
        raise ValueError("Select a product before purchasing")

    def cancel(self, machine):
        raise ValueError("There is no transaction to cancel")


class SelectedState(VendingState):
    def select_product(self, machine, product_id):
        raise ValueError("Cannot select another product, cancel the current transaction first")

    def insert_money(self, machine, amount):
        accepted_denominations = { 1_000, 2_000, 5_000, 10_000, 20_000 }

        if amount not in accepted_denominations:
            raise ValueError(f"Unssopperted denomination: Rp{amount}")

        machine.inserted_amount += amount

        if machine.inserted_amount >= machine.selected_product.price:
            machine.state = ReadyState()

    def purchase(self, machine):
        missing_amount = machine.selected_product.price - machine.inserted_amount

        raise ValueError(f"Insuffisient amount, insert Rp{missing_amount} more")
    
    def cancel(self, machine):
        refund = machine.inserted_amount

        machine.selected_product = None
        machine.inserted_amount = 0
        machine.state = IdleState()

        return refund


class ReadyState(VendingState):
    def select_product(self, machine, product_id):
        raise ValueError("Cannot select another product, cancel the current transaction first")

    def insert_money(self, machine, amount):
        raise ValueError("Amount of money is sufficient")

    def purchase(self, machine):
        product = machine.selected_product

        machine.stock[product.product_id] -= 1
        machine.revenue += product.price

        change = machine.inserted_amount - product.price

        machine.selected_product = None
        machine.inserted_amount = 0
        machine.state = IdleState()

        return product, change

    def cancel(self, machine):
        refund = machine.inserted_amount
        
        machine.selected_product = None
        machine.inserted_amount = 0
        machine.state = IdleState()

        return refund

from typing import Optional

from .product import Product
from .state import IdleState

class VendingMachine:
    def __init__(self):
        self.products: dict[str, Product] = {}
        self.stock: dict[str, int] = {}

        self.selected_product: Optional[Product] = None
        self.inserted_amount = 0
        self.revenue = 0

        self.state = IdleState()

    def add_product(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Product quantity must be greater than zero")

        if product.product_id in self.products:
            raise ValueError(f"Product {product.product_id} already exists, use restock instead")
        
        self.products[product.product_id] = product
        self.stock[product.product_id] = quantity

    def restock(self, product_id, quantity):
        if product_id not in self.products:
            raise ValueError(f"Product {product_id} does not exist")

        if quantity <= 0:
            raise ValueError("Restock quantity must be greater than zero")

        self.stock[product_id] += quantity

    def select_product(self, product_id: str):
        self.state.select_product(self, product_id)

    def insert_money(self, amount: int):
        self.state.insert_money(self, amount)

    def purchase(self) -> tuple[Product, int]:
        return self.state.purchase(self)

    def cancel(self) -> int:
        return self.state.cancel(self)
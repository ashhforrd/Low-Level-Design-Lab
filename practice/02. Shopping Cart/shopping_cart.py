class Product:
    def __init__(self, product_id: str, price: int) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")

        self.product_id = product_id
        self.price = price


class CartItem:
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        self.product = product
        self.quantity = quantity


class Cart:
    def __init__(self) -> None:
        self.items: dict[str, CartItem] = {}

    def add_product(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        item = self.items.get(product.product_id)

        if item is not None:
            item.quantity += quantity
        else:
            self.items[product.product_id] = CartItem(product, quantity)

    def remove_product(self, product_id: str) -> None:
        if product_id not in self.items:
            raise ValueError("Product does not exist in the cart")

        self.items.pop(product_id)

    def calculate_total(self) -> int:
        total = 0

        for item in self.items.values():
            total += (item.product.price * item.quantity)

        return total


def main() -> None:
    coffee = Product("COFFEE", 15_000)
    sandwich = Product("SANDWICH", 25_000)

    cart = Cart()

    cart.add_product(coffee, 2)
    cart.add_product(coffee, 1)
    cart.add_product(sandwich, 1)

    print(cart.items["COFFEE"].quantity)
    print(cart.calculate_total())

    cart.remove_product("COFFEE")

    print(cart.calculate_total())

    cart.remove_product("SANDWICH")

    print(cart.calculate_total())


if __name__ == "__main__":
    main()
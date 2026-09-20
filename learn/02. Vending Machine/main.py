from vending_machine.machine import VendingMachine
from vending_machine.product import Product


machine = VendingMachine()

water = Product(
    product_id="WATER",
    name="Air Mineral",
    price=8_000,
)

machine.add_product(water, quantity=3)

print(type(machine.state).__name__)

machine.select_product("WATER")
print(type(machine.state).__name__)

machine.insert_money(5_000)
print(type(machine.state).__name__)

machine.insert_money(5_000)
print(type(machine.state).__name__)

product, change = machine.purchase()

print(product.name)
print(change)
print(machine.stock["WATER"])
print(machine.revenue)
print(type(machine.state).__name__)
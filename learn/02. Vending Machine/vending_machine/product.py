class Product:
    def __init__(self, product_id: str, name: str, price: int) -> None:
        if product_id.strip() == "" or name.strip() == "":
            raise ValueError("ID or Name cannot be empty")
        
        if price <= 0:
            raise ValueError("Price must be higher than zero")
        
        self.product_id = product_id.strip()
        self.name = name.strip()
        self.price = price
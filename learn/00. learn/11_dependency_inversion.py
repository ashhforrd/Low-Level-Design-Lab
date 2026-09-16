from abc import ABC, abstractmethod


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order_id: str) -> None:
        pass


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.order_ids = []

    def save(self, order_id: str) -> None:
        self.order_ids.append(order_id)
        print(f"Saved {order_id} in memory")


class DatabaseOrderRepository(OrderRepository):
    def save(self, order_id: str) -> None:
        print(f"Saved {order_id} to database")


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, order_id: str) -> None:
        print(f"Creating order {order_id}")
        self.repository.save(order_id)


if __name__ == "__main__":
    memory_repository = InMemoryOrderRepository()
    database_repository = DatabaseOrderRepository()

    test_service = OrderService(memory_repository)
    production_service = OrderService(database_repository)

    test_service.create_order("ORDER-TEST-1")
    production_service.create_order("ORDER-PROD-1")
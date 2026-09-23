from enum import Enum, auto
from typing import Optional


class TicketStatus(Enum):
    WAITING = auto()
    SERVED = auto()
    CANCELLED = auto()


class QueueTicket:
    def __init__(self, ticket_number: int, customer_id: str) -> None:
        self.ticket_number = ticket_number
        self.customer_id = customer_id
        self.status = TicketStatus.WAITING

    def serve(self) -> None:
        if self.status != TicketStatus.WAITING:
            raise ValueError("Only WAITING ticket can be served")
        
        self.status = TicketStatus.SERVED

    def cancel(self) -> None:
        if self.status != TicketStatus.WAITING:
            raise ValueError("Only WAITING ticket can be cancelled")
         
        self.status = TicketStatus.CANCELLED


class Queue:
    def __init__(self) -> None:
        self.tickets: dict[int, QueueTicket] = {}
        self.next_ticket_number = 1

    def take_ticket(self, customer_id: str) -> QueueTicket:
        for ticket in self.tickets.values():
            if ticket.customer_id == customer_id and ticket.status == TicketStatus.WAITING:
                raise ValueError("Customer already has a WAITING ticket")

        queue_ticket = QueueTicket(self.next_ticket_number, customer_id)
        self.tickets[self.next_ticket_number] = queue_ticket

        self.next_ticket_number += 1

        return queue_ticket

    def call_next(self) -> Optional[QueueTicket]:
        waiting_tickets = [
            ticket 
            for ticket in self.tickets.values()
            if ticket.status == TicketStatus.WAITING
        ]

        if not waiting_tickets:
            return None

        next_ticket = min(
            waiting_tickets,
            key=lambda ticket: ticket.ticket_number,
        )

        next_ticket.serve()
        return next_ticket

    def cancel_ticket(self, ticket_number: int) -> None:
        ticket = self.tickets.get(ticket_number)

        if ticket is None:
            raise ValueError("Ticket does not exists")
        
        ticket.cancel()


def main() -> None:
    queue = Queue()

    first = queue.take_ticket("CUSTOMER-1")
    second = queue.take_ticket("CUSTOMER-2")
    third = queue.take_ticket("CUSTOMER-3")

    print(first.ticket_number)
    print(second.ticket_number)
    print(third.ticket_number)

    queue.cancel_ticket(second.ticket_number)

    called = queue.call_next()
    print(called.ticket_number, called.status)

    called = queue.call_next()
    print(called.ticket_number, called.status)

    called = queue.call_next()
    print(called)

    new_ticket = queue.take_ticket("CUSTOMER-1")
    print(new_ticket.ticket_number)


if __name__ == "__main__":
    main()
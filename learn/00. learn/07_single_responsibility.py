class Invoice:
    def __init__(self, subtotal: int, tax_percentage: int):
        self.subtotal = subtotal
        self.tax_percentage = tax_percentage

    def calculate_total(self) -> int:
        tax = self.subtotal * self.tax_percentage // 100
        return self.subtotal + tax


class InvoiceRepository:
    def save(self, invoice: Invoice) -> None:
        total = invoice.calculate_total()
        print(f"Saving invoice with total Rp{total}")


class InvoiceEmailServices:
    def send(self, invoice: Invoice, email_address: str) -> None:
        total = invoice.calculate_total()
        print(
            f"Sending invoice Rp{total} "
            f"to {email_address}"
        )


if __name__ == "__main__":
    invoice = Invoice(
        subtotal=100_000,
        tax_percentage=11,
    )

    repository = InvoiceRepository()
    email_service = InvoiceEmailServices()

    repository.save(invoice)
    email_service.send(
        invoice,
        "budi@example.com"
    )
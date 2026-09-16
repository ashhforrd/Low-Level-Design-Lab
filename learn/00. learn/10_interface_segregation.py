from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print_document(self, contract: str) -> None:
        pass


class Scanner(ABC):
    @abstractmethod
    def scan_document(self) -> str:
        pass


class BasicPrinter(Printer):
    def print_document(self, content: str) -> None:
        print(f"Printing: {content}")


class OfficeMachine(Printer, Scanner):
    def print_document(self, content: str) -> None:
        print(f"Office printing: {content}")

    def scan_document(self) -> str:
        return "Scanned document"


def print_report(printer: Printer) -> None:
    printer.print_document("Monthly report")


if __name__ == "__main__":
    basic_printer = BasicPrinter()
    office_machine = OfficeMachine()

    print_report(basic_printer)
    print_report(office_machine)

    print(office_machine.scan_document())
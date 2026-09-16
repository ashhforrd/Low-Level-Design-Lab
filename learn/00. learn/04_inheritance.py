class Employee:
    def __init__(self, name: str):
        self.name = name

    def work(self) -> str:
        return f"{self.name} sedang bekerja"


class Developer(Employee):
    def __init__(
            self,
            name: str,
            programming_language: str,
    ):
        super().__init__(name)
        self.programming_language = programming_language

    def work(self) -> str:
        return (
            f"{self.name} sedang menulis"
            f"kode {self.programming_language}"
        )


class Manager(Employee):
    def __init__(
            self,
            name: str,
            team_size: int
    ):
        super().__init__(name)
        self.team_size = team_size

    def work(self) -> str:
        return (
            f"{self.name} sedang mengelola "
            f"{self.team_size} anggota time"
        )


def run_workday(employees: list[Employee]) -> None:
    for employee in employees:
        print(employee.work())


if __name__ == "__main__":
    employees = [
        Employee("Andi"),
        Developer("Budi", "Python"),
        Manager("Sari", 5),
    ]

    run_workday(employees)

from abc import ABC, abstractmethod


class Expense:
    def __init__(self, total_amount: int, participant_ids: list[str]) -> None:
        if total_amount <= 0:
            raise ValueError("Total amount must be greater than zero")

        if len(participant_ids) < 2:
            raise ValueError("Expense requires at least two participants")

        if len(set(participant_ids)) != len(participant_ids):
            raise ValueError("Participants cannot contain duplicates")

        self.total_amount = total_amount
        self.participant_ids = tuple(participant_ids)


class SplitStrategy(ABC):
    @abstractmethod
    def split(self, expense: Expense) -> dict[str, int]:
        pass


class EqualSplitStrategy(SplitStrategy):
    def split(self, expense: Expense) -> dict[str, int]:
        participant_count = len(expense.participant_ids)

        if expense.total_amount < participant_count:
            raise ValueError(
                "Total amount is too small for a positive equal split"
            )
        
        base_amount = expense.total_amount // len(expense.participant_ids)
        remainder = expense.total_amount % len(expense.participant_ids)

        allocations: dict[str, int] = {}

        for index, participant_id in enumerate(expense.participant_ids):
            extra_amount = 1 if index < remainder else 0

            allocations[participant_id] = base_amount + extra_amount

        return allocations


class ExactSplitStrategy(SplitStrategy):
    def __init__(
        self,
        allocations: dict[str, int],
    ) -> None:
        self.allocations = allocations.copy()

    def split(
        self,
        expense: Expense,
    ) -> dict[str, int]:
        expected_participants = set(
            expense.participant_ids
        )
        provided_participants = set(
            self.allocations.keys()
        )

        if provided_participants != expected_participants:
            raise ValueError(
                "Allocations must match expense participants"
            )

        has_invalid_amount = any(
            amount <= 0
            for amount in self.allocations.values()
        )

        if has_invalid_amount:
            raise ValueError(
                "Every allocation must be greater than zero"
            )

        allocated_total = sum(
            self.allocations.values()
        )

        if allocated_total != expense.total_amount:
            raise ValueError(
                "Allocation total must equal expense total"
            )

        return self.allocations.copy()


class ExpenseSplitter:
    def split(
        self,
        expense: Expense,
        strategy: SplitStrategy,
    ) -> dict[str, int]:
        allocations = strategy.split(expense)

        if set(allocations.keys()) != set(
            expense.participant_ids
        ):
            raise RuntimeError(
                "Strategy returned invalid participants"
            )

        if any(
            amount <= 0
            for amount in allocations.values()
        ):
            raise RuntimeError(
                "Strategy returned invalid amounts"
            )

        if sum(allocations.values()) != expense.total_amount:
            raise RuntimeError(
                "Strategy returned an invalid total"
            )

        return allocations


def main() -> None:
    expense = Expense(
        total_amount=100,
        participant_ids=[
            "USER-1",
            "USER-2",
            "USER-3",
        ],
    )

    splitter = ExpenseSplitter()

    equal_result = splitter.split(
        expense,
        EqualSplitStrategy(),
    )

    print("Equal split:", equal_result)

    exact_result = splitter.split(
        expense,
        ExactSplitStrategy(
            {
                "USER-1": 50,
                "USER-2": 30,
                "USER-3": 20,
            }
        ),
    )

    print("Exact split:", exact_result)

    try:
        splitter.split(
            expense,
            ExactSplitStrategy(
                {
                    "USER-1": 50,
                    "USER-2": 30,
                    "USER-3": 10,
                }
            ),
        )
    except ValueError as error:
        print("Invalid exact split:", error)


if __name__ == "__main__":
    main()
from abc import ABC, abstractmethod
from typing import Optional


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class TextEditor:
    def __init__(self) -> None:
        self.content = ""

    def insert(self, position: int, text: str) -> None:
        if position > 0 or position > len(self.content):
            raise ValueError("Insert position is out of range")

        self.content = (
            self.content[:position] 
            + text
            + self.content[position:]
        )

    def delete(self, position: int, lenght: int) -> str:
        if position < 0 or position > len(self.content):
            raise ValueError("Invalid delete operation")

        end_position = position + lenght

        if end_position > len(self.content):
            raise ValueError("Delete range is out of bounds")

        deleted_text = self.content[position:end_position]

        self.content = (
            self.content[:position] 
            + self.content[end_position:]
        )

        return deleted_text


class InsertTextCommand(Command):
    def __init__(
            self,
            editor: TextEditor,
            position: int,
            text: str,
    ) -> None:
        if text == "":
            raise ValueError("Inserted text cannot be empty")

        self.editor = editor
        self.position = position
        self.text = text

    def execute(self) -> None:
        self.editor.insert(self.position, self.text)

    def undo(self) -> None:
        deleted_text = self.editor.delete(
            self.position,
            len(self.text)
        )

        if deleted_text != self.text:
            raise RuntimeError(
                "Editor state is inconsistent with command history"
            )


class DeleteTextCommand(Command):
    def __init__(
            self,
            editor: TextEditor,
            position: int,
            length: int,
    ) -> None:
        self.editor = editor
        self.position = position
        self.length = length
        self.deleted_text: Optional[str] = None

    def execute(self) -> None:
        self.deleted_text = self.editor.delete(
            self.position,
            self.length
        )

    def undo(self) -> None:
        if self.deleted_text is None:
            raise RuntimeError(
                "Cannot undo a command that has not been executed"
            )

        self.editor.insert(
            self.position,
            self.deleted_text,
        )


class CommandManager:
    def __init__(self) -> None:
        self.history: list[Command] = []
        self.redo_history: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self.history.append(command)

        # Command baru membuat jalur redo lama tidak lagi valid.
        self.redo_history.clear()

    def undo(self) -> bool:
        if not self.history:
            return False

        command = self.history[-1]
        command.undo()

        self.history.pop()
        self.redo_history.append(command)

        return True

    def redo(self) -> bool:
        if not self.redo_history:
            return False

        command = self.redo_history[-1]
        command.execute()

        self.redo_history.pop()
        self.history.append(command)

        return True


def main() -> None:
    editor = TextEditor()
    manager = CommandManager()

    manager.execute(
        InsertTextCommand(editor, 0, "Hello")
    )
    print("Insert Hello:", editor.content)

    manager.execute(
        InsertTextCommand(editor, 5, " World")
    )
    print("Insert World:", editor.content)

    manager.undo()
    print("Undo insert:", editor.content)

    manager.redo()
    print("Redo insert:", editor.content)

    manager.execute(
        DeleteTextCommand(editor, 5, 6)
    )
    print("Delete World:", editor.content)

    manager.undo()
    print("Undo delete:", editor.content)

    manager.redo()
    print("Redo delete:", editor.content)

    manager.undo()
    print("Undo delete again:", editor.content)

    manager.execute(
        InsertTextCommand(editor, 11, "!")
    )
    print("Execute new command:", editor.content)

    redo_succeeded = manager.redo()
    print("Redo after new command:", redo_succeeded)
    print("Final content:", editor.content)


if __name__ == "__main__":
    main()
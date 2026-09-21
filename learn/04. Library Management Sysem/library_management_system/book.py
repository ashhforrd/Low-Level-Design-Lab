class Book:
    def __init__(self, isbn: str, title: str, author: str) -> None:
        normalized_isbn = isbn.strip()
        normalized_title = title.strip()
        normalized_author = author.strip()

        if normalized_isbn == "":
            raise ValueError("ISBN cannot be empty")

        if normalized_title == "":
            raise ValueError("Title cannot be empty")

        if normalized_author == "":
            raise ValueError("Author cannot be empty")

        self.isbn = normalized_isbn
        self.title = normalized_title
        self.author = normalized_author
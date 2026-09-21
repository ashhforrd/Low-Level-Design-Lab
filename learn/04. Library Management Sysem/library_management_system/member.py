class Member:
    def __init__(self, member_id: str, name: str) -> None:
        normalized_member_id = member_id.strip()
        normalized_name = name.strip()

        if normalized_member_id == "":
            raise ValueError("Member ID cannot be empty")

        if normalized_name == "":
            raise ValueError("Name cannot be empty")

        self.member_id = normalized_member_id
        self.name = normalized_name
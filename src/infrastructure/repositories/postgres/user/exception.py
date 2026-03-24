class UserIsExist(Exception):
    def __init__(self, field: str, value: str):
        super().__init__(f"User with {field} {value} already exists.")


class UserNotFound(Exception):
    def __init__(self):
        super().__init__("User not found.")

class EmailIsNotUnique(Exception):
    def __init__(self, field: str):
        super().__init__(f"User with {field} already exists.")

class NameIsNotUnique(Exception):
    def __init__(self, field: str):
        super().__init__(f"User with {field} already exists.")



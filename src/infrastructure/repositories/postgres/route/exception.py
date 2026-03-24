class RouteNameIsNotUnique(Exception):
    def __init__(self, field: str):
        super().__init__(f"Route with {field} already exists.")


class UserNotAuthorize(Exception):
    def __init__(self):
        super().__init__("User not authorize.")

class EmailIsNotUnique(Exception):
    def __init__(self, field: str):
        super().__init__(f"Email with {field} already exists.")

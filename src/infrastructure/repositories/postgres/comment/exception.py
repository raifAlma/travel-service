
class UserNotAuthorize(Exception):
    def __init__(self):
        super().__init__('User not authorize.')

class RouteNotFound(Exception):
    def __init__(self):
        super().__init__('Route not found.')
class LikeAlreadyExists(Exception):
    def __init__(self):
        super().__init__(f'Like already exists.')

class RouteNotFound(Exception):
    def __init__(self):
        super().__init__('Route not found.')
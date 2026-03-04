class WaypointNameIsNotUnique(Exception):
    def __init__(self, field: str):
        super().__init__(f'Waypoint with {field} already exists.')

class RouteNotFound(Exception):
    def __init__(self):
        super().__init__('Route not found.')


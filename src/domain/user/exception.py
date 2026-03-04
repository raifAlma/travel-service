class ItemNotFoundError(Exception):
    """Бизнес-ошибка: Item не найден."""

    def __init__(self, item_id: int) -> None:
        super().__init__(f"Item with id={item_id} not found")
        self.item_id = item_id

    def __str__(self, user_id: int) -> None:
        super().__str__(f"Item with id={user_id} was created")
        self.user_id = user_id
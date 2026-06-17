class InvalidAPIUsage(Exception):
    """Исключение, представляющее ошибки в работе с API."""

    status_code = 400

    def __init__(self, message, status_code=400):
        """Переопределенный магический метод конструктора."""
        super().__init__()

        self.message = message
        self.status_code = status_code
    
    def to_dict(self):
        """Преобразует исключение с словарь для сериализации."""
        return dict(message=self.message)

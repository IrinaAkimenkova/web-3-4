class User:
    """Класс пользователя
    :param id: идентификатор
    :type id: int
    :param email: эдектронная почта
    :type email: str
    :param password: пароль
    :type password: str"""
    def __init__(self, id: int, email: str, password: str):
        self.id = id
        self.email = email
        self.password = password

class Task:
    def __init__(self, id: int, title: str, description: str, user_id: int, state: bool):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
        self.state = state
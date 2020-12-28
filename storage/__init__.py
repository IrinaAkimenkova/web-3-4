import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from entities import User, Task

# Подключаемся к БД
db_path = '/'.join([str(Path(__file__).parent), '..', 'db', 'database.sqlite'])
db = sqlite3.connect(db_path, check_same_thread=False)


class Storage:
    @staticmethod
    def add_user(user: User):
        """обавление пользователя
        :param user:    новый пользователь
        :type user:     User"""
        db.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                   (user.email, generate_password_hash(user.password)))
        db.commit()

    @staticmethod
    def get_user_by_email_and_password(email: str, passwordHash: str) -> User:
        """Найти пользователя по email и паролю
        :param email:       электронная почта
        :type email:        str
        :param passwordHash:    хэш пароля
        :type passwordHash:     str
        :return: пользователь
        :rtype: User
        """
        user_data = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user_data and check_password_hash(user_data[2], passwordHash):
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def get_user_by_id(id: int) -> User:
        """Найти пользователя по id
        :param id:  идентификатор пользователя
        :type id:   int
        :return:    пользователь
        :rtype:     User"""
        user_data = db.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
        if user_data:
            return User(id=user_data[0], email=user_data[1], password=user_data[2])
        else:
            return None

    @staticmethod
    def get_tasks(user_id: int) -> list:
        request = db.execute('SELECT * FROM tasks WHERE id_user = ?', (user_id,));
        tasks = request.fetchall();
        tasksList = [];
        for task in tasks:
            tasksList.append(Task(task[0], task[1], task[2], task[3], task[4]));
        return tasksList;

    @staticmethod
    def add_task(task: Task):
        db.execute('INSERT INTO tasks (title, description, id_user, is_done) VALUES (?, ?, ?, ?)',
            (task.title, task.description, task.user_id, task.state));
        db.commit();

    @staticmethod
    def delete_task(taskId: int):
        db.execute('DELETE FROM tasks WHERE id = ?', (taskId,));
        db.commit();

    @staticmethod
    def get_task(taskId: int) -> Task:
        request = db.execute('SELECT * FROM tasks WHERE id = ?', (taskId,));
        task = request.fetchone();
        return Task(task[0], task[1], task[2], task[3], task[4]);

    @staticmethod
    def set_state(taskId : int):
        db.execute('UPDATE tasks SET is_done = CASE WHEN is_done = 0 THEN 1 ELSE 0 END WHERE id = ?', (taskId,));
        db.commit();

    @staticmethod
    def update_desc(taskId: int, new_desc: str):
        db.execute('UPDATE tasks SET description = ? WHERE id = ?', (new_desc, taskId));
        db.commit();

    @staticmethod
    def task_exists(taskId: int):
        count = db.execute('SELECT COUNT(*) FROM tasks WHERE id = ?', (taskId,)).fetchone()
        if count[0] > 0:
            return True
        else:
            return False

    @staticmethod
    def is_permitted(id_user: int, taskId: int):
        task_owner_id = db.execute('SELECT id_user FROM tasks WHERE id = ?', (taskId,)).fetchone()
        if task_owner_id[0] == id_user:
            return True
        else:
            return False

    @staticmethod
    def filter(state: str, id_user: int):
        is_done_l = 0
        is_done_r = 1

        if state == 'done':
            is_done_l = 1
        if state == 'in_progress':
            is_done_r = 0

        request = db.execute('SELECT * FROM tasks WHERE (is_done = ? OR is_done = ?) AND id_user = ? ORDER BY id ASC', (is_done_l, is_done_r, id_user));
        tasks = request.fetchall();
        tasksList = [];
        for task in tasks:
            tasksList.append({
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'user_id': task[3],
                'state': task[4]
            });
        return tasksList;
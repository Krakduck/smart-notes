import sqlite3
import os


class NoteDatabase:
    def __init__(self, db_name="Note_tracker.db"):
        self.db_path = os.path.abspath(os.path.join(os.getcwd(), db_name))
        self.create_table()
        print(self.db_path)

    def create_table(self):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users ( 
                                  name TEXT NOT NULL,
                                  text TEXT NOT NULL
                                  )''')
            connection.commit()
            connection.close()
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")

    def add(self, name, text):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO users (name, text) VALUES (?, ?)',
                (name, text)
            )
            connection.commit()
            connection.close()
            return True
        except Exception as e:
            print(f"Ошибка добавления: {e}")
            return False

    def get(self, name):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # 1. Посмотрим вообще ВСЕ записи, которые есть
            cursor.execute('SELECT * FROM users')
            print(f"Все данные в базе: {cursor.fetchall()}")
            cursor.execute(
                'SELECT * FROM users WHERE name = ?',
                (name.strip().upper(),)
            )
            result = cursor.fetchall()
            connection.close()
            return result
        except Exception as e:
            print(f"Ошибка поиска: {e}")
            return None

    def get_all(self):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT name, text FROM users")
            data = cursor.fetchall()
            connection.close()
            return data
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return []

    def update_user_param(self, name, column_name, new_value):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # Безопасное обновление через f-строку только для имени колонки
            query = f"UPDATE users SET {column_name} = ? WHERE name = ?"
            cursor.execute(query, (new_value, name))
            connection.commit()
            connection.close()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении {column_name}: {e}")
            return False

    def delete(self, name):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('DELETE FROM users WHERE name = ?', (name,))
            connection.commit()
            connection.close()
            print(f"Данные по {name} успешно удалены.")
            return True
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
            return False
import sqlite3
import logging

logging.basicConfig(level=logging.ERROR)


class Data:
    _instance = None

    def __new__(cls, filename):
        if cls._instance is None:
            cls._instance = super(Data, cls).__new__(cls)
            cls._instance.filename = filename
            cls._instance.data = []
            cls._instance.connect()
        return cls._instance

    def connect(self) -> None:
        self.db = sqlite3.connect(self.filename)
        self.cur = self.db.cursor()

    def close(self) -> None:
        if self.db:
            self.db.close()

    def __del__(self):
        self.close()

    def get_all_questions(self) -> None:
        try:
            request = "SELECT * FROM Questions"
            self.data = self.cur.execute(request).fetchall()
        except sqlite3.Error as e:
            logging.error(f"Ошибка получения данных: {e}")

    def get_all_questions_without_answer(self) -> None:
        try:
            request = """
                SELECT * FROM Questions
                WHERE answer IS NULL OR answer = ''
            """
            self.data = self.cur.execute(request).fetchall()
        except sqlite3.Error as e:
            logging.error(f"Ошибка получения данных: {e}")

    def get_question(self, **kwargs) -> None:
        try:
            request = """
                SELECT * FROM Questions
                WHERE id_question = ?"""
            data = (kwargs['id_question'],)
            self.data = self.cur.execute(request, data).fetchall()
        except sqlite3.Error as e:
            logging.error(f"Ошибка получения данных: {e}")

    def add_question(self, **kwargs) -> None:
        try:
            sqlite_insert_query = """
                INSERT INTO Questions (user_id, user, text, answer)
                VALUES (?, ?, ?, ?);
            """
            data = (kwargs['user_id'], kwargs['user'], kwargs['text'], "")
            self.cur.execute(sqlite_insert_query, data)
            self.db.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка добавления: {e}")

    def update_question(self, **kwargs) -> None:
        try:
            sqlite_update_query = """
                UPDATE Questions
                SET answer = ?
                WHERE id_question = ?;
            """
            data = (kwargs['answer'], kwargs['id_question'])
            self.cur.execute(sqlite_update_query, data)
            self.db.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка обновления: {e}")

    def delete_question(self, **kwargs) -> None:
        try:
            sqlite_delete_query = """
                DELETE FROM Questions WHERE id_question = ?;
            """
            data = (kwargs['id_question'],)
            self.cur.execute(sqlite_delete_query, data)
            self.db.commit()
        except sqlite3.Error as e:
            print(e)
            logging.error(f"Ошибка удаления: {e}")

    def get_all_admins(self) -> None:
        try:
            request = "SELECT * FROM Admins"
            self.data = self.cur.execute(request).fetchall()
        except sqlite3.Error as e:
            logging.error(f"Ошибка получения данных: {e}")

    def add_admins(self, **kwargs) -> None:
        try:
            sqlite_insert_query = """
                INSERT INTO Admins (username)
                VALUES (?);
            """
            data = (kwargs['username'],)
            self.cur.execute(sqlite_insert_query, data)
            self.db.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка добавления: {e}")

    def delete_admin(self, **kwargs) -> None:
        try:
            sqlite_delete_query = """
                DELETE FROM Admins WHERE username = ?;
            """
            data = (kwargs['username'],)
            self.cur.execute(sqlite_delete_query, data)
            self.db.commit()
        except sqlite3.Error as e:
            logging.error(f"Ошибка удаления: {e}")
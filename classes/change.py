import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()


class ChangeDB:
    def __init__(self):
        self.config = {
            "host": os.getenv('DB_HOST'),
            "database": os.getenv('DB_NAME'),
            "user": os.getenv('DB_USER'),
            "password": os.getenv('DB_PASSWORD'),
            "port": os.getenv('DB_PORT')
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print('Подключено')
                return True
        except Error as e:
            print(f'Ошибка подключения: {e}')
            return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print('Подключение завершено')

    def use_comand(self, query, params, commit):
        if not(self.connection) or not(self.connection.is_connected()):
            raise Exception("Нет соединения с базой данных")
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query, params)
            if commit:
                self.connection.commit()
                return self.cursor.rowcount
            return self.cursor.fetchall()
        except Error as e:
            if commit:
                self.connection.rollback()
            print(f"[ERROR] Ошибка выполнения запроса: {e}")
            raise e
        finally:
            if self.cursor:
                self.cursor.close()

    def create(self, table, columns, values):
        cols = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        return self.use_comand(query, values, commit=True)

    # condition="id = %s", params=[5]
    def read(self, table, condition=None, params=None):
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        return self.use_comand(query, params, commit=False)

    # updates = {"name": "Петя"}
    def update(self, table, updates, condition, params):
        set_parts = ", ".join([f"{col} = %s" for col in updates.keys()])
        values = list(updates.values()) + list(params)
        query = f"UPDATE {table} SET {set_parts} WHERE {condition}"
        return self.use_comand(query, values, commit=True)

    def delete(self, table, condition, params):
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.use_comand(query, params, commit=True)

    def raw(self, query, params=None, commit=False):
        return self.use_comand(query, params, commit=commit)
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, create_table_sql):
        try:
            self.cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, insert_sql, data):
        try:
            self.cursor.execute(insert_sql, data)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def fetch_data(self, select_sql):
        self.cursor.execute(select_sql)
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()
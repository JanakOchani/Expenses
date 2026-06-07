import psycopg2

class Database:

    def __init__(self):
        print("Database initialized.")

    def get_connection(self):
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="expenses_db",
            user="postgres",
            password="postgres"
        )
        return connection

    def execute_query(self, query):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def fetch_data(self, query):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
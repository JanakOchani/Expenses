import psycopg2

class Database:
    def __init__(self):
        print("Database object created.")

    def execute_query(self, query):
        try:
            print(query)
            connection = psycopg2.connect(
                host="localhost",
                port="5432",
                database="expenses_db",
                user="postgres",
                password="postgres"
            )
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            print("Query executed successfully.")

        except Exception as error:
            print(f"Database error: {error}")
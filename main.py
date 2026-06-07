from fastapi import FastAPI, HTTPException
import psycopg2
from tracker import Tracker
from database import Database

app = FastAPI()

def getDBConnection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="expenses_db",
            user="postgres",
            password="postgres"
        )
        return connection

    except Exception as problem:
        print(f"There was a problem getting connection {problem}")
        return None

@app.post("/expenses")
def add_expense(date: str, amount: float, category: str, description: str):
    try:

        expense = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        print(expense)

        tracker = Tracker()
        result = tracker.addExpense(expense)

        return {
            "message": "Expense added successfully",
            "expense": result
        }
    except Exception as error:
        print("Error adding expense:", error)
        raise HTTPException(status_code=500, detail="Failed to add expense")


@app.get("/expenses")
def get_expenses():
    try:
        connection = getDBConnection()
        cursor = connection.cursor()
        query = """
        SELECT id, date, amount, category, description, added_at
        FROM expenses;
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        tracker = Tracker()
        return tracker.getExpenses(rows)

    except Exception as error:
        print("Error fetching expenses:", error)
        raise HTTPException(status_code=500, detail="Failed to fetch expenses")
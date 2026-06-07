from fastapi import FastAPI, HTTPException
from database import Database
from insights import get_expense_insights
import pandas as pd

expenseTracker = FastAPI()

@expenseTracker.post("/expenses")
def add_expense(expense: dict):

    try:
        database = Database()
        connection = database.get_connection()
        sqlEditor = connection.cursor()
        query = f"""
        INSERT INTO expenses
        (date, amount, category, description)
        VALUES
        (
            '{expense['date']}',
            {expense['amount']},
            '{expense['category']}',
            '{expense['description']}'
        );
        """

        sqlEditor.execute(query)
        connection.commit()
        sqlEditor.close()
        connection.close()

        print("PostgreSQL connection is closed")
        return {"message": "Expense added successfully"}

    except Exception as error:
        print("Error while adding expense:", error)
        raise HTTPException(
            status_code=500,
            detail="Error adding expense"
        )


@expenseTracker.get("/expenses")
def get_expenses():
    try:
        database = Database()
        connection = database.get_connection()
        sqlEditor = connection.cursor()
        query = """
        SELECT
            date,
            amount,
            category,
            description
        FROM expenses;
        """

        sqlEditor.execute(query)
        rows = sqlEditor.fetchall()
        results = []
        for row in rows:
            results.append({
                "date": row[0],
                "amount": row[1],
                "category": row[2],
                "description": row[3]
            })

        df = pd.DataFrame(results)
        df.to_csv("my_expenses.csv", index=False)
        insights = get_expense_insights(df)
        sqlEditor.close()
        connection.close()

        print("PostgreSQL connection is closed")
        return {
            "expenses": results,
            "insights": insights
        }

    except Exception as error:
        print("Error while fetching expenses:", error)
        raise HTTPException(
            status_code=500,
            detail="Error fetching expenses"
        )

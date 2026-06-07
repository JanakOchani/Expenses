from database import Database
from expense import Expense
import pandas as pd

class Tracker:
    def __init__(self):
        print("Tracker initialized.")

    def addExpense(self, expense_data):
        expense = Expense(
            expense_data["date"],
            expense_data["amount"],
            expense_data["category"],
            expense_data["description"]
        )
        db = Database()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            date DATE,
            amount DECIMAL(10,2),
            category VARCHAR(100),
            description TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        db.execute_query(create_table_query)

        insert_query = f"""
        INSERT INTO expenses (date, amount, category, description)
        VALUES ({expense.date}, {expense.amount}, {expense.category}, {expense.description});
        """
        db.execute_query(insert_query)
        return expense.getInfo()

    def buildInsights(self, rows):
        df = pd.DataFrame(
            rows, columns=["id", "date", "amount", "category", "description", "added_at"]
        )
        if df.empty:
            return {
                "total_expenses": 0,
                "total_amount": 0,
                "avg_amount": 0,
                "top_category": None,
                "highest_expense": 0,
                "expenses_by_category": {},
                "amount_list": []
            }
        return {
            "total_expenses": len(df),
            "total_amount": round(df["amount"].sum(), 2),
            "avg_amount": round(df["amount"].mean(), 2),
            "top_category": df["category"].value_counts().idxmax(),
            "highest_expense": round(df["amount"].max(), 2),
            "expenses_by_category": df.groupby("category")["amount"].sum().to_dict(),
            "amount_list": df["amount"].tolist()
        }

    def getExpenses(self, rows):
        df = pd.DataFrame(
            rows,
            columns=["id", "date", "amount", "category", "description", "added_at"]
        )
        insights = self.buildInsights(rows)
        return {
            "expenses": df.to_dict(orient="records"),
            "insights": insights
        }
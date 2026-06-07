
def get_expense_insights(df):
    if df.empty:
        return {
            "total_expenses": 0,
            "total_amount": 0
        }

    insights = {
        "total_expenses": len(df),
        "total_amount": round(df['amount'].sum(), 2),
        "avg_amount": round(df['amount'].mean(), 2),
        "top_category": df['category'].value_counts().idxmax(),
        "highest_expense": round(df['amount'].max(), 2),
        "expenses_by_category":
            df.groupby('category')['amount'].sum().to_dict(),
        "amount_list":
            df['amount'].tolist()
    }

    return insights
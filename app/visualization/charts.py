import plotly.express as px

def monthly_spending_chart(df):
    fig = px.bar(df, x="month", y="amount", title="Monthly Spending")
    return fig.to_json()

def spending_by_category_chart(df):
    fig = px.pie(df, names="category_id", values="amount", title="Spending by Category")
    return fig.to_json()

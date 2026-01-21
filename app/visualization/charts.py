import matplotlib.pyplot as plt

def expense_chart(expenses):
    categories = {}
    for e in expenses:
        categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]

    plt.bar(categories.keys(), categories.values())
    plt.title("Expenses by Category")
    plt.show()

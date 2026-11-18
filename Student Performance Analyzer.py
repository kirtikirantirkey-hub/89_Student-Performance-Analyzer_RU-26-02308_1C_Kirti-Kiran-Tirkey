import pandas as pd
import os
from datetime import datetime

CSV_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"

# Load budget from file if exists
def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            try:
                return float(f.read().strip())
            except:
                return 0
    return 0

def save_budget(budget):
    with open(BUDGET_FILE, "w") as f:
        f.write(str(budget))

# Load expenses using Pandas
def load_expenses():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df
        except:
            return pd.DataFrame(columns=["Date", "Category", "Amount"])
    else:
        return pd.DataFrame(columns=["Date", "Category", "Amount"])

def save_expense(date, category, amount):
    df = load_expenses()
    new_row = pd.DataFrame([{"Date": date, "Category": category, "Amount": amount}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# 1. Set Budget
def set_budget():
    try:
        budget = float(input("Enter monthly budget: "))
        if budget <= 0:
            print("Invalid amount. Amount must be a positive number.")
            return 0
        save_budget(budget)
        print(f"Monthly budget set: {int(budget) if budget.is_integer() else budget}")
        return budget
    except ValueError:
        print("Invalid amount. Amount must be a positive number.")
        return 0

# 2. Add Expense
def add_expense(budget):
    date_str = input("Enter date (YYYY-MM-DD): ")
    # Validate date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    category = input("Enter category (Food/Travel/etc): ")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Amount must be a positive number.")
        return

    if amount <= 0:
        print("Invalid amount. Amount must be a positive number.")
        return

    save_expense(date_str, category, amount)
    print("Expense saved.")

    # Show total and remaining after adding
    df = load_expenses()
    total = df["Amount"].sum()
    remaining = budget - total
    if budget > 0:
        percent = (total / budget) * 100
        print(f"Total spent: {int(total) if total == int(total) else total} | Remaining: {int(remaining) if remaining == int(remaining) else remaining}")
        if percent >= 100:
            print(f"Budget fully used ({percent:.2f}%).")
            print("Budget exceeded!")
        elif percent >= 80:
            print(f"Warning: {percent:.2f}% of the budget used.")

# 3. Category Summary using groupby()
def category_summary():
    df = load_expenses()
    if df.empty:
        print("No expenses found.")
        return
    print("\n--- Category-wise Summary ---")
    summary = df.groupby("Category")["Amount"].sum()
    for cat, amt in summary.items():
        print(f"{cat}: {int(amt) if amt == int(amt) else amt}")

# 4. Report
def report(budget):
    df = load_expenses()
    if df.empty:
        print("No expenses found.")
        return
    print("\n--- Report ---")
    summary = df.groupby("Category")["Amount"].sum()
    for cat, amt in summary.items():
        print(f"{cat}: {int(amt) if amt == int(amt) else amt}")

    total = df["Amount"].sum()
    remaining = budget - total
    print(f"Total spent: {int(total) if total == int(total) else total} | Remaining: {int(remaining) if remaining == int(remaining) else remaining}")

    if budget > 0:
        percent = (total / budget) * 100
        if percent >= 100:
            print(f"Budget fully used ({percent:.2f}%).")
            print("Budget exceeded!")
        elif percent >= 80:
            print(f"Warning: {percent:.2f}% of the budget used.")
        else:
            print(f"Budget used: {percent:.2f}%")

# Main Menu
def main():
    budget = load_budget()
    while True:
        print("\n--- Personal Expense & Budget Manager ---")
        print("1. Set Budget")
        print("2. Add Expense")
        print("3. Category Summary")
        print("4. Report")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            budget = set_budget()
        elif choice == "2":
            if budget == 0:
                print("Please set budget first (Option 1).")
            else:
                add_expense(budget)
        elif choice == "3":
            category_summary()
        elif choice == "4":
            report(budget)
        elif choice == "5":
            print("Thank you! Goodbye.")
            break
        else:
            print("Invalid choice! Try again.")

main()
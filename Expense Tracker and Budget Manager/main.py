import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from tabulate import tabulate
import csv

# Initialize database
conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        category TEXT,
        budget_amount REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS recurring_expenses (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")
conn.commit()

def register_or_login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user_id = cursor.fetchone()

    if user_id:
        print("Login successful.")
        return user_id[0]
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful. You can now log in.")
        return cursor.lastrowid

def log_expense(user_id):
    amount = float(input("Enter expense amount: "))
    category = input("Enter expense category: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO transactions (user_id, amount, category, date) VALUES (?, ?, ?, ?)", (user_id, amount, category, date))
    conn.commit()
    print("Expense logged successfully.")

def set_budget(user_id):
    category = input("Enter category for budget: ")
    budget_amount = float(input("Enter budget amount: "))

    cursor.execute("INSERT OR REPLACE INTO budgets (user_id, category, budget_amount) VALUES (?, ?, ?)", (user_id, category, budget_amount))
    conn.commit()
    print("Budget set successfully.")

def view_spending_trends(user_id):
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY category", (user_id,))
    data = cursor.fetchall()

    if not data:
        print("No spending data available.")
        return

    categories = [entry[0] for entry in data]
    amounts = [entry[1] for entry in data]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts)
    plt.xlabel("Categories")
    plt.ylabel("Total Amount")
    plt.title("Spending Trends")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def view_expense_history(user_id):
    cursor.execute("SELECT amount, category, date FROM transactions WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()

    if not data:
        print("No expense history available.")
        return

    headers = ["Amount", "Category", "Date"]
    table = tabulate(data, headers=headers, tablefmt="grid")
    print("\nExpense History:")
    print(table)

def export_to_csv(user_id):
    cursor.execute("SELECT amount, category, date FROM transactions WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()

    if not data:
        print("No data to export.")
        return

    filename = f"expense_history_{user_id}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Amount", "Category", "Date"])
        writer.writerows(data)
    print(f"Data exported to {filename}.")

def edit_budget(user_id):
    category = input("Enter the category to edit budget for: ")

    cursor.execute("SELECT budget_amount FROM budgets WHERE user_id = ? AND category = ?", (user_id, category))
    existing_budget = cursor.fetchone()

    if not existing_budget:
        print("Budget does not exist for this category.")
        return

    new_budget_amount = float(input(f"Enter new budget amount for {category}: "))

    cursor.execute("UPDATE budgets SET budget_amount = ? WHERE user_id = ? AND category = ?", (new_budget_amount, user_id, category))
    conn.commit()
    print(f"Budget for {category} updated successfully.")

def set_recurring_expense(user_id):
    amount = float(input("Enter recurring expense amount: "))
    category = input("Enter recurring expense category: ")

    cursor.execute("INSERT INTO recurring_expenses (user_id, amount, category) VALUES (?, ?, ?)", (user_id, amount, category))
    conn.commit()
    print("Recurring expense set successfully.")

def generate_expense_report(user_id):
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id = ? AND date BETWEEN ? AND ? GROUP BY category",
                   (user_id, start_date, end_date))
    data = cursor.fetchall()

    if not data:
        print("No data available for the selected time period.")
        return

    headers = ["Category", "Total Amount"]
    table = tabulate(data, headers=headers, tablefmt="grid")
    print("\nExpense Report:")
    print(table)

def main():
    print("Expense Tracker and Budget Manager")

    user_id = register_or_login()

    while True:
        print("\nOptions:")
        print("1. Log Expense")
        print("2. Set Budget")
        print("3. View Spending Trends")
        print("4. View Expense History")
        print("5. Export Data to CSV")
        print("6. Edit Budget")
        print("7. Set Recurring Expense")
        print("8. Generate Expense Report")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            log_expense(user_id)
        elif choice == "2":
            set_budget(user_id)
        elif choice == "3":
            view_spending_trends(user_id)
        elif choice == "4":
            view_expense_history(user_id)
        elif choice == "5":
            export_to_csv(user_id)
        elif choice == "6":
            edit_budget(user_id)
        elif choice == "7":
            set_recurring_expense(user_id)
        elif choice == "8":
            generate_expense_report(user_id)
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

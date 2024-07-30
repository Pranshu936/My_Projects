import json

def save_transactions(transactions, filename='transactions.json'):
    with open(filename, 'w') as file:
        json.dump(transactions, file)
    print("Transactions saved!\n")

def load_transactions(filename='transactions.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error loading transactions. File might be corrupted.")
        return []

def add_income(transactions):
    description = input("Enter income description: ")
    amount = float(input("Enter income amount: "))
    transactions.append({"description": description, "amount": amount, "type": "income"})
    print("Income added!\n")

def add_expense(transactions):
    description = input("Enter expense description: ")
    amount = float(input("Enter expense amount: "))
    transactions.append({"description": description, "amount": amount, "type": "expense"})
    print("Expense added!\n")

def view_balance(transactions):
    balance = 0
    for transaction in transactions:
        if transaction["type"] == "income":
            balance += transaction["amount"]
        elif transaction["type"] == "expense":
            balance -= transaction["amount"]
    print(f"Current balance: ${balance:.2f}\n")

def view_transactions(transactions, filter_type=None):
    print("Transaction History:")
    for i, transaction in enumerate(transactions):
        if filter_type is None or transaction["type"] == filter_type:
            print(f"{i}. {transaction['type'].capitalize()}: ${transaction['amount']:.2f} - {transaction['description']}")
    print()

def delete_transaction(transactions):
    view_transactions(transactions)
    try:
        index = int(input("Enter the index of the transaction to delete: "))
        if 0 <= index < len(transactions):
            transactions.pop(index)
            print("Transaction deleted!\n")
        else:
            print("Invalid index. No transaction deleted.\n")
    except ValueError:
        print("Invalid input. No transaction deleted.\n")

def edit_transaction(transactions):
    view_transactions(transactions)
    try:
        index = int(input("Enter the index of the transaction to edit: "))
        if 0 <= index < len(transactions):
            description = input("Enter new description: ")
            amount = float(input("Enter new amount: "))
            transactions[index]["description"] = description
            transactions[index]["amount"] = amount
            print("Transaction edited!\n")
        else:
            print("Invalid index. No transaction edited.\n")
    except ValueError:
        print("Invalid input. No transaction edited.\n")

def summarize_transactions(transactions):
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expenses
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Balance: ${balance:.2f}\n")

def search_transactions(transactions):
    keyword = input("Enter keyword to search: ")
    print("Search Results:")
    for i, transaction in enumerate(transactions):
        if keyword.lower() in transaction["description"].lower():
            print(f"{i}. {transaction['type'].capitalize()}: ${transaction['amount']:.2f} - {transaction['description']}")
    print()

def main():
    transactions = load_transactions()
    
    while True:
        print("Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View All Transactions")
        print("5. View Income Transactions")
        print("6. View Expense Transactions")
        print("7. Delete Transaction")
        print("8. Edit Transaction")
        print("9. Summarize Transactions")
        print("10. Search Transactions")
        print("11. Save Transactions")
        print("12. Load Transactions")
        print("13. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_income(transactions)
        elif choice == "2":
            add_expense(transactions)
        elif choice == "3":
            view_balance(transactions)
        elif choice == "4":
            view_transactions(transactions)
        elif choice == "5":
            view_transactions(transactions, "income")
        elif choice == "6":
            view_transactions(transactions, "expense")
        elif choice == "7":
            delete_transaction(transactions)
        elif choice == "8":
            edit_transaction(transactions)
        elif choice == "9":
            summarize_transactions(transactions)
        elif choice == "10":
            search_transactions(transactions)
        elif choice == "11":
            save_transactions(transactions)
        elif choice == "12":
            transactions = load_transactions()
        elif choice == "13":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")

if __name__ == "__main__":
    main()

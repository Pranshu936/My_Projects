import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# File paths
USERS_FILE = 'users.json'
DATA_FILE = 'data.json'

# Load data from file
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data to file
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# User Authentication
def register_user(username, password):
    users = load_json(USERS_FILE)
    if username in users:
        return False  # User already exists
    users[username] = password
    save_json(USERS_FILE, users)
    return True

def authenticate_user(username, password):
    users = load_json(USERS_FILE)
    return users.get(username) == password

# Financial Data Management
def load_financial_data():
    return load_json(DATA_FILE)

def save_financial_data(data):
    save_json(DATA_FILE, data)

def add_transaction(transaction_type, amount, category):
    data = load_financial_data()
    if transaction_type == 'income':
        data.setdefault('income', []).append({"amount": amount, "category": category})
    elif transaction_type == 'expense':
        data.setdefault('expenses', []).append({"amount": amount, "category": category})
    save_financial_data(data)

def set_budget(category, amount):
    data = load_financial_data()
    data.setdefault('budget', {})[category] = amount
    save_financial_data(data)

def generate_report():
    data = load_financial_data()
    income_total = sum(item['amount'] for item in data.get('income', []))
    expenses_total = sum(item['amount'] for item in data.get('expenses', []))
    return {
        "income_total": income_total,
        "expenses_total": expenses_total,
        "budget": data.get('budget', {})
    }

# GUI Setup
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Login')
        self.geometry('300x150')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text='Username:').pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text='Password:').pack(pady=5)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self, text='Login', command=self.login).pack(pady=5)
        tk.Button(self, text='Register', command=self.register).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate_user(username, password):
            self.destroy()
            BudgetManagerApp().mainloop()
        else:
            messagebox.showerror('Login Failed', 'Invalid username or password.')

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if register_user(username, password):
            messagebox.showinfo('Success', 'User registered successfully! You can now log in.')
        else:
            messagebox.showerror('Error', 'User already exists.')

class BudgetManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Budget Manager')
        self.geometry('800x600')
        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Section
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Button(self.input_frame, text='Add Income', command=self.add_income).pack(pady=5)
        tk.Button(self.input_frame, text='Add Expense', command=self.add_expense).pack(pady=5)
        tk.Button(self.input_frame, text='Set Budget', command=self.set_budget).pack(pady=5)
        tk.Button(self.input_frame, text='Generate Report', command=self.generate_report).pack(pady=5)
        tk.Button(self.input_frame, text='Compare Income and Expenses', command=self.plot_comparison).pack(pady=5)
        tk.Button(self.input_frame, text='Show Budget Proportions', command=self.plot_budget_proportions).pack(pady=5)

        # Graph Section
        self.graph_frame = tk.Frame(self.main_frame)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def add_income(self):
        amount = simpledialog.askfloat('Input', 'Enter income amount:')
        category = simpledialog.askstring('Input', 'Enter income category:')
        if amount is not None and category:
            add_transaction('income', amount, category)
            messagebox.showinfo('Success', 'Income added successfully!')
        else:
            messagebox.showwarning('Warning', 'Please enter valid amount and category.')

    def add_expense(self):
        amount = simpledialog.askfloat('Input', 'Enter expense amount:')
        category = simpledialog.askstring('Input', 'Enter expense category:')
        if amount is not None and category:
            add_transaction('expense', amount, category)
            messagebox.showinfo('Success', 'Expense added successfully!')
        else:
            messagebox.showwarning('Warning', 'Please enter valid amount and category.')

    def set_budget(self):
        category = simpledialog.askstring('Input', 'Enter budget category:')
        amount = simpledialog.askfloat('Input', 'Enter budget amount:')
        if amount is not None and category:
            set_budget(category, amount)
            messagebox.showinfo('Success', 'Budget set successfully!')
        else:
            messagebox.showwarning('Warning', 'Please enter valid category and amount.')

    def generate_report(self):
        report = generate_report()
        budget_status = "\n".join(f"{cat}: ${amt}" for cat, amt in report['budget'].items())
        messagebox.showinfo("Report", f"Total Income: ${report['income_total']}\nTotal Expenses: ${report['expenses_total']}\nBudget:\n{budget_status}")

    def plot_comparison(self):
        data = load_financial_data()
        income_total = sum(item['amount'] for item in data.get('income', []))
        expenses_total = sum(item['amount'] for item in data.get('expenses', []))
        
        fig, ax = plt.subplots()
        categories = ['Income', 'Expenses']
        values = [income_total, expenses_total]
        
        ax.bar(categories, values, color=['green', 'red'])
        ax.set_ylabel('Amount ($)')
        ax.set_title('Income vs Expenses')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_budget_proportions(self):
        data = load_financial_data()
        budget = data.get('budget', {})
        
        if not budget:
            messagebox.showwarning('No Budget Data', 'No budget data available to plot.')
            return

        fig, ax = plt.subplots()
        categories = list(budget.keys())
        values = list(budget.values())
        
        ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
        ax.set_title('Budget Proportions')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == '__main__':
    LoginWindow().mainloop()

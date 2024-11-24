import mysql.connector
import hashlib
import random
import string
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from cryptography.fernet import Fernet
from datetime import datetime, timedelta


class PasswordManagerGUI:
    def __init__(self, root):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="pranshu@2004", 
            database="password_manager"
        )
        self.cursor = self.conn.cursor()
        self.user_id = None
        self.encryption_key = None

        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("600x400")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        self.login_tab = Frame(self.notebook)
        self.password_tab = Frame(self.notebook)

        self.notebook.add(self.login_tab, text="Login/Register")
        self.notebook.add(self.password_tab, text="Manage Passwords")
        self.password_tab.pack_propagate(False)

        self.create_login_tab()
        self.create_password_tab()

    def create_login_tab(self):
        Label(self.login_tab, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = Entry(self.login_tab)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self.login_tab, text="Master Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = Entry(self.login_tab, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        Button(self.login_tab, text="Register", command=self.register_user).grid(row=2, column=0, padx=10, pady=10)
        Button(self.login_tab, text="Login", command=self.login_user).grid(row=2, column=1, padx=10, pady=10)

    def create_password_tab(self):
        self.password_frame = Frame(self.password_tab)
        self.password_frame.pack(fill=BOTH, expand=True)

        self.password_listbox = Listbox(self.password_frame)
        self.password_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.password_listbox.bind("<Double-1>", self.on_password_selected)

        self.scrollbar = Scrollbar(self.password_frame, command=self.password_listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.password_listbox.config(yscrollcommand=self.scrollbar.set)

        Button(self.password_tab, text="Add Password", command=self.add_password).pack(pady=5)
        Button(self.password_tab, text="Generate Password", command=self.generate_password).pack(pady=5)
        
        self.logout_button = Button(self.password_tab, text="Logout", command=self.logout_user)
        self.logout_button.pack(pady=5)

    def register_user(self):
        username = self.username_entry.get()
        master_password = self.password_entry.get()
        hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
        encryption_key = Fernet.generate_key()

        try:
            self.cursor.execute("""
                INSERT INTO users (username, hashed_password, encryption_key)
                VALUES (%s, %s, %s)
            """, (username, hashed_password, encryption_key.decode()))
            self.conn.commit()
            messagebox.showinfo("Success", f"User {username} registered successfully!")
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Please try a different one.")

    def login_user(self):
        username = self.username_entry.get()
        master_password = self.password_entry.get()
        hashed_password = hashlib.sha256(master_password.encode()).hexdigest()

        self.cursor.execute("""
            SELECT id, encryption_key FROM users WHERE username = %s AND hashed_password = %s
        """, (username, hashed_password))
        result = self.cursor.fetchone()

        if result:
            self.user_id, encryption_key = result
            self.encryption_key = Fernet(encryption_key.encode())
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.list_passwords()
            self.notebook.select(self.password_tab)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def check_password_strength(self, password):
        score = 0
        if len(password) >= 8:
            score += 1
        if any(char.isdigit() for char in password):
            score += 1
        if any(char.isupper() for char in password):
            score += 1
        if any(char.islower() for char in password):
            score += 1
        if any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
            score += 1

        if score <= 2:
            return "Weak"
        elif score == 3:
            return "Moderate"
        else:
            return "Strong"

    def add_password(self):
        if not self.user_id:
            messagebox.showerror("Error", "You need to log in first!")
            return

        website = simpledialog.askstring("Add Password", "Enter website:")
        username = simpledialog.askstring("Add Password", "Enter username:")
        password = simpledialog.askstring("Add Password", "Enter password:", show="*")

        strength = self.check_password_strength(password)
        messagebox.showinfo("Password Strength", f"Password strength: {strength}")

        if strength in ["Weak", "Moderate"]:
            suggested_password = self.generate_password()
            messagebox.showinfo("Suggestion", f"Suggested password: {suggested_password}")
            use_suggested = messagebox.askyesno("Use Suggested Password", "Use the suggested password?")
            if use_suggested:
                password = suggested_password

        expiry_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
        encrypted_password = self.encryption_key.encrypt(password.encode()).decode()

        self.cursor.execute("""
            INSERT INTO passwords (user_id, website, username, encrypted_password, expiry_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.user_id, website, username, encrypted_password, expiry_date))
        self.conn.commit()
        messagebox.showinfo("Success", f"Password for {website} added successfully!")
        self.list_passwords()

    def list_passwords(self):
        if not self.user_id:
            messagebox.showerror("Error", "You need to log in first!")
            return

        self.password_listbox.delete(0, END)
        self.cursor.execute("""
            SELECT website, username, expiry_date FROM passwords WHERE user_id = %s
        """, (self.user_id,))
        results = self.cursor.fetchall()
        for website, username, expiry_date in results:
            self.password_listbox.insert(END, f"{website} - {username} (Expiry: {expiry_date})")

    def on_password_selected(self, event):
        selected_item = self.password_listbox.get(self.password_listbox.curselection())
        website = selected_item.split(" - ")[0]

        self.cursor.execute("""
            SELECT username, encrypted_password, expiry_date
            FROM passwords
            WHERE user_id = %s AND website = %s
        """, (self.user_id, website))
        result = self.cursor.fetchone()

        if result:
            username, encrypted_password, expiry_date = result
            password = self.encryption_key.decrypt(encrypted_password.encode()).decode()
            messagebox.showinfo(
                "Password Details",
                f"Website: {website}\nUsername: {username}\nPassword: {password}\nExpiry Date: {expiry_date}"
            )
        else:
            messagebox.showerror("Error", f"No password found for {website}.")

    def generate_password(self, length=12):
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        messagebox.showinfo("Generated Password", f"Generated password: {password}")
        return password

    def logout_user(self):
        self.user_id = None
        self.encryption_key = None
        messagebox.showinfo("Logout", "You have been logged out successfully!")
        self.notebook.select(self.login_tab) 

def main():
    root = Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

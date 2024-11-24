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
        # Initialize database connection
        self.conn = mysql.connector.connect(
            host="localhost",  # Host for the MySQL database
            user="root",  # MySQL username
            password="pranshu@2004",  # MySQL password
            database="password_manager"  # Database name
        )
        self.cursor = self.conn.cursor()  # Create cursor for executing queries
        self.user_id = None  # Stores the ID of the currently logged-in user
        self.encryption_key = None  # Stores the encryption key for the user

        # Tkinter GUI setup
        self.root = root  # The root window of the Tkinter application
        self.root.title("Password Manager")  # Title of the window
        self.root.geometry("600x400")  # Window size

        # Create tabs using ttk.Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True)

        # Create two tabs: one for login/register, one for managing passwords
        self.login_tab = Frame(self.notebook)
        self.password_tab = Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.login_tab, text="Login/Register")
        self.notebook.add(self.password_tab, text="Manage Passwords")
        self.password_tab.pack_propagate(False)  # Disable resizing of the password tab

        # Initialize login and password tabs
        self.create_login_tab()
        self.create_password_tab()

    def create_login_tab(self):
        # Widgets for the login and registration tab
        Label(self.login_tab, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = Entry(self.login_tab)  # Entry field for the username
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(self.login_tab, text="Master Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = Entry(self.login_tab, show="*")  # Password entry field
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        Button(self.login_tab, text="Register", command=self.register_user).grid(row=2, column=0, padx=10, pady=10)
        Button(self.login_tab, text="Login", command=self.login_user).grid(row=2, column=1, padx=10, pady=10)

    def create_password_tab(self):
        # Widgets for managing passwords
        self.password_frame = Frame(self.password_tab)  # Frame for password-related widgets
        self.password_frame.pack(fill=BOTH, expand=True)

        # Listbox to display stored passwords
        self.password_listbox = Listbox(self.password_frame)
        self.password_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.password_listbox.bind("<Double-1>", self.on_password_selected)  # Bind double-click event to show password details

        # Scrollbar for the password listbox
        self.scrollbar = Scrollbar(self.password_frame, command=self.password_listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.password_listbox.config(yscrollcommand=self.scrollbar.set)

        # Buttons to add passwords, generate passwords, and logout
        Button(self.password_tab, text="Add Password", command=self.add_password).pack(pady=5)
        Button(self.password_tab, text="Generate Password", command=self.generate_password).pack(pady=5)
        self.logout_button = Button(self.password_tab, text="Logout", command=self.logout_user)
        self.logout_button.pack(pady=5)

    def register_user(self):
        # Registers a new user
        username = self.username_entry.get()  # Get username from entry field
        master_password = self.password_entry.get()  # Get master password from entry field
        hashed_password = hashlib.sha256(master_password.encode()).hexdigest()  # Hash the master password
        encryption_key = Fernet.generate_key()  # Generate a unique encryption key

        try:
            # Insert the new user into the 'users' table
            self.cursor.execute("""
                INSERT INTO users (username, hashed_password, encryption_key)
                VALUES (%s, %s, %s)
            """, (username, hashed_password, encryption_key.decode()))
            self.conn.commit()  # Commit the transaction to the database
            messagebox.showinfo("Success", f"User {username} registered successfully!")  # Show success message
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Please try a different one.")  # Handle duplicate username

    def login_user(self):
        # Login an existing user
        username = self.username_entry.get()  # Get username from entry field
        master_password = self.password_entry.get()  # Get master password from entry field
        hashed_password = hashlib.sha256(master_password.encode()).hexdigest()  # Hash the entered password

        # Query to find the user based on the username and hashed password
        self.cursor.execute("""
            SELECT id, encryption_key FROM users WHERE username = %s AND hashed_password = %s
        """, (username, hashed_password))
        result = self.cursor.fetchone()  # Fetch user data

        if result:
            self.user_id, encryption_key = result  # Set the user ID and encryption key
            self.encryption_key = Fernet(encryption_key.encode())  # Initialize encryption key
            messagebox.showinfo("Success", f"Welcome back, {username}!")  # Show welcome message
            self.list_passwords()  # List passwords after login
            self.notebook.select(self.password_tab)  # Switch to the password management tab
        else:
            messagebox.showerror("Error", "Invalid username or password.")  # Show error for invalid credentials

    def check_password_strength(self, password):
        # Check the strength of a password
        score = 0
        if len(password) >= 8:  # Length should be at least 8 characters
            score += 1
        if any(char.isdigit() for char in password):  # Password should contain at least one digit
            score += 1
        if any(char.isupper() for char in password):  # Password should contain at least one uppercase letter
            score += 1
        if any(char.islower() for char in password):  # Password should contain at least one lowercase letter
            score += 1
        if any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):  # Password should contain special characters
            score += 1

        # Determine password strength based on the score
        if score <= 2:
            return "Weak"
        elif score == 3:
            return "Moderate"
        else:
            return "Strong"

    def add_password(self):
        if not self.user_id:  # Check if the user is logged in
            messagebox.showerror("Error", "You need to log in first!")  # Show error if not logged in
            return

        # Collect password details from the user
        website = simpledialog.askstring("Add Password", "Enter website:")  # Ask for website
        username = simpledialog.askstring("Add Password", "Enter username:")  # Ask for username
        password = simpledialog.askstring("Add Password", "Enter password:", show="*")  # Ask for password

        strength = self.check_password_strength(password)  # Check the password strength
        messagebox.showinfo("Password Strength", f"Password strength: {strength}")  # Show strength

        # If the password is weak or moderate, suggest a stronger one
        if strength in ["Weak", "Moderate"]:
            suggested_password = self.generate_password()  # Generate a suggested password
            messagebox.showinfo("Suggestion", f"Suggested password: {suggested_password}")
            use_suggested = messagebox.askyesno("Use Suggested Password", "Use the suggested password?")
            if use_suggested:
                password = suggested_password  # Use the suggested password if user agrees

        # Set expiry date for password (90 days)
        expiry_date = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
        encrypted_password = self.encryption_key.encrypt(password.encode()).decode()  # Encrypt the password

        # Insert the password details into the database
        self.cursor.execute("""
            INSERT INTO passwords (user_id, website, username, encrypted_password, expiry_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.user_id, website, username, encrypted_password, expiry_date))
        self.conn.commit()  # Commit the changes
        messagebox.showinfo("Success", f"Password for {website} added successfully!")  # Show success message
        self.list_passwords()  # List all stored passwords

    def list_passwords(self):
        if not self.user_id:  # Check if the user is logged in
            messagebox.showerror("Error", "You need to log in first!")  # Show error if not logged in
            return

        # Fetch and display all stored passwords for the logged-in user
        self.password_listbox.delete(0, END)  # Clear the listbox
        self.cursor.execute("""
            SELECT website, username, expiry_date FROM passwords WHERE user_id = %s
        """, (self.user_id,))
        results = self.cursor.fetchall()  # Fetch the passwords
        for website, username, expiry_date in results:
            self.password_listbox.insert(END, f"{website} - {username} (Expiry: {expiry_date})")  # Add to listbox

    def on_password_selected(self, event):
        # Display password details when an item is double-clicked
        selected_item = self.password_listbox.get(self.password_listbox.curselection())
        website = selected_item.split(" - ")[0]  # Extract website name from the selection

        self.cursor.execute("""
            SELECT username, encrypted_password, expiry_date
            FROM passwords
            WHERE user_id = %s AND website = %s
        """, (self.user_id, website))
        result = self.cursor.fetchone()  # Fetch password details

        if result:
            username, encrypted_password, expiry_date = result
            password = self.encryption_key.decrypt(encrypted_password.encode()).decode()  # Decrypt the password
            messagebox.showinfo(
                "Password Details",
                f"Website: {website}\nUsername: {username}\nPassword: {password}\nExpiry Date: {expiry_date}"
            )  # Display password details
        else:
            messagebox.showerror("Error", f"No password found for {website}.")  # Show error if password not found

    def generate_password(self, length=12):
        # Generate a random password
        chars = string.ascii_letters + string.digits + string.punctuation  # Characters to choose from
        password = ''.join(random.choice(chars) for _ in range(length))  # Generate password
        messagebox.showinfo("Generated Password", f"Generated password: {password}")  # Show the generated password
        return password

    def logout_user(self):
        # Logout the user and reset session data
        self.user_id = None  # Clear user ID
        self.encryption_key = None  # Clear encryption key
        messagebox.showinfo("Logout", "You have been logged out successfully!")  # Show logout message
        self.notebook.select(self.login_tab)  # Switch back to the login tab


def main():
    root = Tk()  # Create the Tkinter root window
    app = PasswordManagerGUI(root)  # Create the PasswordManagerGUI object
    root.mainloop()  # Start the Tkinter event loop


if __name__ == "__main__":
    main()  # Run the program

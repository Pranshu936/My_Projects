# Password Manager

A simple Python-based password manager with a graphical user interface (GUI) that allows users to securely store and manage passwords. The application uses encryption to protect stored passwords and supports user registration and login.

## Features
- User registration and login system
- Store passwords securely using encryption
- Password strength checker
- Suggest strong passwords if the entered password is weak or moderate
- Expiry date for stored passwords (set to 90 days)
- View password details when selected
- Random password generator
- Logout functionality

## Requirements

### Python Libraries
This project uses the following libraries:
- `mysql-connector`: For MySQL database connection.
- `cryptography`: For password encryption/decryption.
- `tkinter`: For GUI interface.
- `hashlib`: For password hashing.
- `random` and `string`: For generating random passwords.

You can install the required libraries using `pip`:
```bash
pip install mysql-connector-python cryptography
```

### MySQL Setup

1. **Database Creation:**

   Before running the application, you need to create a MySQL database and the required tables. You can execute the following SQL commands to set up the database:

   ```sql
   CREATE DATABASE password_manager;

   USE password_manager;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(255) NOT NULL UNIQUE,
       hashed_password VARCHAR(255) NOT NULL,
       encryption_key VARCHAR(255) NOT NULL
   );

   CREATE TABLE passwords (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT NOT NULL,
       website VARCHAR(255) NOT NULL,
       username VARCHAR(255) NOT NULL,
       encrypted_password TEXT NOT NULL,
       expiry_date DATE NOT NULL,
       FOREIGN KEY (user_id) REFERENCES users(id)
   );
   ```

2. **Database Configuration:**

   In the Python script, ensure that the `mysql.connector.connect()` function is configured correctly with your MySQL username, password, and database name:

   ```python
   self.conn = mysql.connector.connect(
       host="localhost",  # MySQL host
       user="root",  # MySQL username
       password="your_mysql_password",  # Your MySQL password
       database="password_manager"  # Database name
   )
   ```

3. **Creating the Tables:**
   The script will automatically use the `password_manager` database and interact with the `users` and `passwords` tables for user authentication and password storage.

## Usage Instructions

1. **Run the application:**

   You can run the program by executing the script:

   ```bash
   python password_manager.py
   ```

2. **User Registration:**
   - Enter a username and a master password.
   - The system will hash the master password and generate an encryption key, which will be used to encrypt your stored passwords.
   - If the username already exists, the system will show an error.

3. **User Login:**
   - Enter the registered username and master password.
   - The system will verify the username and password, and if successful, will take you to the password management screen.

4. **Managing Passwords:**
   - From the "Manage Passwords" tab, you can:
     - Add a new password (website, username, and password).
     - Generate a new random password.
     - View stored passwords by double-clicking on the listed items.
     - Log out of the application.

5. **Password Expiry:**
   - Each password added will have an expiry date of 90 days, after which it will no longer be valid. 

6. **Password Strength Checker:**
   - When adding a password, the system will check the strength of the password and show a recommendation if it's weak or moderate.

## File Structure

```
password_manager/
├── password_manager.py      # Main Python script containing the logic
├── requirements.txt         # List of Python dependencies
├── README.md                # This README file
└── database.sql             # SQL script for database setup
```


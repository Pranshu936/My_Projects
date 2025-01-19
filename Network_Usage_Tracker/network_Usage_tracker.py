import sys
import psutil
import socket
import sqlite3
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import QTimer, Qt

class NetworkUsageTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Usage Tracker")
        self.setGeometry(100, 100, 600, 400)

        # Database setup: Create/connect to SQLite database to store network usage records.
        self.conn = sqlite3.connect('network_usage.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS network_usage
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               usage REAL)''')
        self.conn.commit()

        # Initialize variables to track network usage.
        self.old_value = 0

        # Create GUI widgets.
        self.usage_label = QLabel("Current Usage: 0 bytes/sec")  # Displays current network usage.
        self.ip_label = QLabel("IP Address: Checking...")  # Displays IP address.
        self.alert_label = QLabel("")  # Displays alerts when usage exceeds a threshold.
        self.records_text = QTextEdit()  # Displays recent network usage records.
        self.records_text.setReadOnly(True)  # Make the text area read-only.

        # Buttons for starting and stopping the tracking process.
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_tracking)  # Connect start button to its handler.
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_tracking)  # Connect stop button to its handler.
        self.stop_button.setEnabled(False)  # Disable stop button initially.

        # Create layouts to organize widgets.
        main_layout = QVBoxLayout()  # Main vertical layout.
        button_layout = QHBoxLayout()  # Horizontal layout for buttons.

        # Add widgets to the main layout.
        main_layout.addWidget(self.usage_label)
        main_layout.addWidget(self.ip_label)
        main_layout.addWidget(self.alert_label)
        main_layout.addWidget(self.records_text)
        
        # Add buttons to the button layout and then to the main layout.
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)

        # Set the main layout as the central widget layout.
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create a timer to periodically update network usage information.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_network_usage)  # Call update method on timer timeout.

    def start_tracking(self):
        """Start tracking network usage."""
        self.start_button.setEnabled(False)  # Disable the start button to prevent multiple starts.
        self.stop_button.setEnabled(True)  # Enable the stop button.
        self.timer.start(1000)  # Start the timer to update every 1 second.

    def stop_tracking(self):
        """Stop tracking network usage."""
        self.start_button.setEnabled(True)  # Enable the start button.
        self.stop_button.setEnabled(False)  # Disable the stop button.
        self.timer.stop()  # Stop the timer.

    def update_network_usage(self):
        """Update network usage data, display, and save to the database."""
        # Get the total bytes sent and received since boot.
        new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        usage = new_value - self.old_value  # Calculate usage in the last interval.

        # Save the usage value to the database.
        self.cursor.execute("INSERT INTO network_usage (usage) VALUES (?)", (usage,))
        self.conn.commit()

        # Update the label displaying current usage.
        self.usage_label.setText(f"Current Usage: {usage} bytes/sec")

        # Determine the IP address and update the label.
        try:
            IPaddress = socket.gethostbyname(socket.gethostname())
            if IPaddress == "127.0.0.1":
                self.ip_label.setText("No internet, your localhost IP is: 127.0.0.1")
            else:
                self.ip_label.setText(f"Connected to the internet with IP address: {IPaddress}")
        except:
            self.ip_label.setText("Unable to determine IP address")

        # Display an alert if usage exceeds 1 MB/sec.
        if usage > 1_000_000:
            self.alert_label.setText("** Alert: Max Limit Usage Exceeded! **")
            self.alert_label.setStyleSheet("color: red;")  # Change text color to red for emphasis.
        else:
            self.alert_label.setText("")  # Clear the alert if usage is within limits.

        # Fetch the most recent 5 records from the database.
        self.cursor.execute("SELECT * FROM network_usage ORDER BY id DESC LIMIT 5")
        rows = self.cursor.fetchall()

        # Update the records text area with the fetched records.
        records_text = "Recent Usage Records:\n"
        for row in rows[::-1]:  # Reverse the order for chronological display.
            records_text += f"Record {row[0]}: Usage {row[1]} bytes\n"
        self.records_text.setText(records_text)

        # Update the old value for the next calculation.
        self.old_value = new_value

    def closeEvent(self, event):
        """Handle the window close event to clean up resources."""
        self.conn.close()  # Close the database connection.
        event.accept()  # Accept the close event.

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application instance.
    window = NetworkUsageTracker()  # Create the main window.
    window.show()  # Show the main window.
    sys.exit(app.exec())  # Execute the application.

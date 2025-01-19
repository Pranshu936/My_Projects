import sys
import psutil
import socket
import sqlite3
import ipaddress
import requests
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import QTimer, Qt


class NetworkUsageTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Network Usage Tracker")
        self.setGeometry(100, 100, 600, 500)

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

        # Additional labels for new features.
        self.geolocation_label = QLabel("Geolocation: Checking...")
        self.hostname_label = QLabel("Hostname: Checking...")
        self.isp_label = QLabel("ISP: Checking...")
        self.ip_version_label = QLabel("IP Version: Checking...")
        self.private_ip_label = QLabel("Private IP: Checking...")
        self.ping_status_label = QLabel("Ping Status: Checking...")

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
        main_layout.addWidget(self.geolocation_label)
        main_layout.addWidget(self.hostname_label)
        main_layout.addWidget(self.isp_label)
        main_layout.addWidget(self.ip_version_label)
        main_layout.addWidget(self.private_ip_label)
        main_layout.addWidget(self.ping_status_label)
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

        # Call IP-related methods once during initialization.
        self.initialize_ip_info()

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

        # **Alert for High Usage**
        if usage > 1_000_000:  # Usage exceeds 1 MB/sec
            self.alert_label.setText("** Alert: Max Limit Usage Exceeded! **")
            self.alert_label.setStyleSheet("color: red;")  # Change text color to red for emphasis
        else:
            self.alert_label.setText("")  # Clear the alert if usage is within limits

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


    def initialize_ip_info(self):
        """Initialize IP-related information once at the start."""
        ip_address = self.get_ip_address()
        self.ip_label.setText(f"IP Address: {ip_address}")

        # Geolocation
        geo_info = self.get_geolocation(ip_address)
        geo_text = ", ".join([f"{key}: {value}" for key, value in geo_info.items()])
        self.geolocation_label.setText(f"Geolocation: {geo_text}")

        # Hostname
        hostname = self.get_hostname(ip_address)
        self.hostname_label.setText(f"Hostname: {hostname}")

        # ISP
        isp = self.get_isp(ip_address)
        self.isp_label.setText(f"ISP: {isp}")

        # IP Version
        ip_version = self.check_ip_version(ip_address)
        self.ip_version_label.setText(f"IP Version: {ip_version}")

        # Private/Public Check
        is_private = self.is_private_ip(ip_address)
        self.private_ip_label.setText(f"Private IP: {'Yes' if is_private else 'No'}")

        # Ping Test
        ping_status = self.ping_server()
        self.ping_status_label.setText(f"Ping Status: {ping_status}")

    # Reuse the IP-related utility functions from the previous code.

    def get_ip_address(self):
        """Get the system's current IP address."""
        try:
            ip_address = socket.gethostbyname(socket.gethostname())
            return ip_address
        except Exception as e:
            return str(e)

    def get_geolocation(self, ip_address):
        """Get geolocation details using an API."""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            if data['status'] == 'success':
                return {
                    'Country': data['country'],
                    'Region': data['regionName'],
                    'City': data['city'],
                    'Latitude': data['lat'],
                    'Longitude': data['lon']
                }
            else:
                return {"Error": "Unable to retrieve geolocation"}
        except Exception as e:
            return {"Error": str(e)}

    def get_hostname(self, ip_address):
        """Perform a reverse DNS lookup to get the hostname."""
        try:
            return socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            return "Unable to resolve hostname"

    def get_isp(self, ip_address):
        """Get ISP information using an API."""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            return data.get('isp', 'Unknown ISP')
        except Exception as e:
            return f"Error: {str(e)}"

    def check_ip_version(self, ip_address):
        """Check if the IP address is IPv4 or IPv6."""
        return "IPv6" if ':' in ip_address else "IPv4"

    def is_private_ip(self, ip_address):
        """Determine if the IP address is private."""
        try:
            return ipaddress.ip_address(ip_address).is_private
        except ValueError:
            return False

    def ping_server(self, server="8.8.8.8"):
        """Check network latency by pinging a server."""
        response = os.system(f"ping -c 1 {server}" if os.name != "nt" else f"ping -n 1 {server}")
        return "Reachable" if response == 0 else "Unreachable"

    def closeEvent(self, event):
        """Handle the window close event to clean up resources."""
        self.conn.close()  # Close the database connection.
        event.accept()  # Accept the close event.


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application instance.
    window = NetworkUsageTracker()  # Create the main window.
    window.show()  # Show the main window.
    sys.exit(app.exec())  # Execute the application.

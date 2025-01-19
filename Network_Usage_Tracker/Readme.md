# Network Usage Tracker

## Overview

The **Network Usage Tracker** is a desktop application built using Python and PyQt6 to monitor real-time network usage. It provides details about current network usage, IP address, and recent usage records. The data is stored in a SQLite database for persistence and analysis.

---

## Features

- **Real-Time Monitoring**: Tracks network usage (bytes sent and received per second).
- **IP Address Detection**: Displays the system's current IP address or indicates if the system is offline.
- **Alert System**: Notifies the user if network usage exceeds a pre-defined threshold.
- **Recent Records**: Displays the last five network usage records from the database.
- **Data Persistence**: Stores network usage data in a SQLite database.

---

## Prerequisites

Ensure you have the following installed:

- Python 3.6+
- Required Python libraries:
  - `PyQt6`
  - `psutil`
  - `sqlite3` (built-in with Python)

You can install the required libraries using:
```bash
pip install PyQt6 psutil
```

---

## How to Run

1. Clone or download the repository to your local machine.
2. Navigate to the project directory.
3. Run the application:
   ```bash
   python <filename>.py
   ```
   Replace `<filename>` with the name of the script file.

---

## Usage

- Click **Start** to begin monitoring network usage.
- View real-time data updates, including:
  - Network usage in bytes per second.
  - IP address of the system.
- Click **Stop** to pause the monitoring process.
- Check recent network usage records in the text box.

---

## Database

The SQLite database (`network_usage.db`) is created automatically in the project directory. It contains a single table, `network_usage`, with the following schema:

- `id`: Auto-incremented unique identifier for each record.
- `usage`: The recorded network usage (in bytes).

---

## Customization

- **Alert Threshold**: The usage threshold for alerts is currently set at `1,000,000 bytes`. Modify this value in the `update_network_usage` method:
  ```python
  if usage > 1_000_000:  # Adjust the value as needed
  ```
- **Update Interval**: The timer updates the data every second. Change the interval in the `start_tracking` method:
  ```python
  self.timer.start(1000)  # Adjust the interval in milliseconds
  ```

---



## Author

Created by **Pranshu kumar**. Contributions and feedback are welcome!


import tkinter as tk
from time import strftime

def update_time():
    """Update the clock display every second."""
    time_string = strftime('%H:%M:%S')  # Format: HH:MM:SS
    date_string = strftime('%A, %d %B %Y')  # Format: Weekday, Day Month Year
    time_label.config(text=time_string)
    date_label.config(text=date_string)
    time_label.after(1000, update_time)  # Update every second

# Create the main window
root = tk.Tk()
root.title("Digital Clock")
root.geometry("400x200")  # Set window size
root.configure(bg="black")  # Background color
root.resizable(False, False)

# Style configurations
font_large = ("Helvetica", 48, "bold")  # Font for time
font_small = ("Helvetica", 16)  # Font for date
fg_color = "white"  # Foreground color (text color)

# Create the clock labels
time_label = tk.Label(root, font=font_large, bg="black", fg=fg_color)
time_label.pack(pady=10)

date_label = tk.Label(root, font=font_small, bg="black", fg=fg_color)
date_label.pack()

# Start the clock
update_time()

# Run the application
root.mainloop()

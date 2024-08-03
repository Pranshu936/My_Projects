# Importing the necessary modules
from tkinter import *  # Tkinter for GUI components
import time  # time for timestamping the saved QR codes
import pyqrcode  # pyqrcode for generating QR codes

# Function to generate a QR code based on user input
def gen_qr():
    global qr, img  # Declare global variables to be used in other functions
    # Create a QR code from the content entered by the user
    qr = pyqrcode.create(con.get())
    # Convert the QR code to XBM format for display in Tkinter
    qr_xbm = qr.xbm(scale=5)
    # Create a BitmapImage from the XBM data
    img = BitmapImage(data=qr_xbm, foreground='black', background='white')
    # Update the label l4 to display the generated QR code
    l4.config(image=img)

# Function to save the generated QR code as a PNG file
def save():
    gen_qr()  # Call the gen_qr function to generate the QR code
    tme = time.time()  # Get the current time to use as the filename
    # Save the QR code as a PNG file with the current timestamp as the filename
    qr.png(f'{tme}.png', scale=8)
    con.set('')  # Clear the content entry field

# Main program
wind = Tk()  # Initialize the main window
wind.title('QR Code Gen')  # Set the title of the window
wind.geometry('500x400')  # Set the size of the window
wind.resizable(0, 0)  # Disable window resizing

# Variable to store the user input content
con = StringVar()

# Create and pack the frames to organize the layout
f1 = Frame(wind, width=500, height=100)
f1.pack()
f2 = Frame(wind, width=500, height=50)
f2.pack()
f3 = Frame(wind, width=500, height=250)
f3.pack()

# Create and place the labels and entry widget
l1 = Label(f1, text='QR Code Generator', font=('SugarFont Bold', 30, 'bold'))
l1.grid(row=0, column=0, columnspan=3, padx=5, pady=10)  # Main title
l2 = Label(f1, text='By Harshit', font=('Arial Rounded MT Bold', 15))
l2.grid(row=0, column=4, sticky='w', pady=10)  # Subtitle

l3 = Label(f2, font=('', 10), text='Enter the content')
l3.grid(row=0, column=0, padx=5)  # Label for entry widget

e1 = Entry(f2, textvariable=con, width=40)
e1.grid(row=0, column=1, padx=5)  # Entry widget for user input

# Create and place the buttons
b1 = Button(f2, text='Generate', command=gen_qr)
b1.grid(row=1, column=0, pady=10)  # Button to generate QR code

b2 = Button(f2, text='Save', command=save)
b2.grid(row=1, column=1, pady=10)  # Button to save QR code

# Label to display the generated QR code
l4 = Label(f3, pady=5)
l4.pack()

# Start the Tkinter event loop to keep the window open and responsive
wind.mainloop()

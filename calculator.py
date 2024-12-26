from tkinter import Tk, END, Entry, N, E, S, W, Button, Label
import tkinter.font as font
from functools import partial
import math

def get_input(entry, argu):
    entry.insert(END, argu)

def backspace(entry):
    input_len = len(entry.get())
    entry.delete(input_len - 1)

def clear(entry):
    entry.delete(0, END)

def calc(entry):
    input_info = entry.get()
    try:
        output = str(eval(input_info.strip(), {"__builtins__": None}, math.__dict__))
    except ZeroDivisionError:
        popupmsg("Cannot divide by 0! Enter valid values.")
        output = ""
    except Exception as e:
        popupmsg(str(e))
        output = ""
    clear(entry)
    entry.insert(END, output)

def popupmsg(msg):
    popup = Tk()
    popup.resizable(0, 0)
    popup.geometry("200x100")
    popup.title("Alert")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", bg="#DDDDDD", command=popup.destroy)
    B1.pack()

def cal():
    root = Tk()
    root.title("Advanced Calculator")
    root.configure(bg='#2E2E2E')
    root.resizable(0, 0)

    entry_font = font.Font(size=18, weight='bold')
    entry = Entry(root, justify="right", font=entry_font, bg='#1C1C1C', fg='#00FF00')
    entry.grid(row=0, column=0, columnspan=4, sticky=N+W+S+E, padx=5, pady=5)

    cal_button_bg = '#FF6600'
    num_button_bg = '#4B4B4B'
    other_button_bg = '#DDDDDD'
    text_fg = '#FFFFFF'
    button_active_bg = '#C0C0C0'

    num_button = partial(Button, root, fg=text_fg, bg=num_button_bg, padx=20, pady=10, activebackground=button_active_bg, font=font.Font(size=14, weight='bold'))
    cal_button = partial(Button, root, fg=text_fg, bg=cal_button_bg, padx=20, pady=10, activebackground=button_active_bg, font=font.Font(size=14, weight='bold'))

    button7 = num_button(text='7', command=lambda: get_input(entry, '7'))
    button7.grid(row=2, column=0, pady=5)

    button8 = num_button(text='8', command=lambda: get_input(entry, '8'))
    button8.grid(row=2, column=1, pady=5)

    button9 = num_button(text='9', command=lambda: get_input(entry, '9'))
    button9.grid(row=2, column=2, pady=5)

    button10 = cal_button(text='+', command=lambda: get_input(entry, '+'))
    button10.grid(row=4, column=3, pady=5)

    button4 = num_button(text='4', command=lambda: get_input(entry, '4'))
    button4.grid(row=3, column=0, pady=5)

    button5 = num_button(text='5', command=lambda: get_input(entry, '5'))
    button5.grid(row=3, column=1, pady=5)

    button6 = num_button(text='6', command=lambda: get_input(entry, '6'))
    button6.grid(row=3, column=2, pady=5)

    button11 = cal_button(text='-', command=lambda: get_input(entry, '-'))
    button11.grid(row=3, column=3, pady=5)

    button1 = num_button(text='1', command=lambda: get_input(entry, '1'))
    button1.grid(row=4, column=0, pady=5)

    button2 = num_button(text='2', command=lambda: get_input(entry, '2'))
    button2.grid(row=4, column=1, pady=5)

    button3 = num_button(text='3', command=lambda: get_input(entry, '3'))
    button3.grid(row=4, column=2, pady=5)

    button12 = cal_button(text='*', command=lambda: get_input(entry, '*'))
    button12.grid(row=2, column=3, pady=5)

    button0 = num_button(text='0', command=lambda: get_input(entry, '0'))
    button0.grid(row=5, column=0, pady=5)

    button13 = num_button(text='.', command=lambda: get_input(entry, '.'))
    button13.grid(row=5, column=1, pady=5)

    button14 = cal_button(text='/', command=lambda: get_input(entry, '/'))
    button14.grid(row=1, column=3, pady=5)

    button15 = Button(root, text='<-', bg=other_button_bg, padx=20, pady=10, command=lambda: backspace(entry), activebackground=button_active_bg, font=font.Font(size=14, weight='bold'))
    button15.grid(row=1, column=0, columnspan=2, padx=3, pady=5, sticky=N+S+E+W)

    button16 = Button(root, text='C', bg=other_button_bg, padx=20, pady=10, command=lambda: clear(entry), activebackground=button_active_bg, font=font.Font(size=14, weight='bold'))
    button16.grid(row=1, column=2, pady=5)

    button17 = Button(root, text='=', fg=text_fg, bg=cal_button_bg, padx=20, pady=10, command=lambda: calc(entry), activebackground=button_active_bg, font=font.Font(size=14, weight='bold'))
    button17.grid(row=5, column=3, pady=5)

    button18 = cal_button(text='^', command=lambda: get_input(entry, '**'))
    button18.grid(row=5, column=2, pady=5)

    button_sin = cal_button(text='sin', command=lambda: get_input(entry, 'math.sin('))
    button_sin.grid(row=6, column=0, pady=5)

    button_cos = cal_button(text='cos', command=lambda: get_input(entry, 'math.cos('))
    button_cos.grid(row=6, column=1, pady=5)

    button_tan = cal_button(text='tan', command=lambda: get_input(entry, 'math.tan('))
    button_tan.grid(row=6, column=2, pady=5)

    button_sqrt = cal_button(text='√', command=lambda: get_input(entry, 'math.sqrt('))
    button_sqrt.grid(row=6, column=3, pady=5)

    root.mainloop()

if __name__ == '__main__':
    cal()
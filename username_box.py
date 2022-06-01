from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

root = Tk()
root.title("Choose user")
root.geometry("300x300")


def clicker_old():
    master = Tk()

    variable = StringVar(master)
    variable.set("one")  # default value

    w = OptionMenu(master, variable, "one", "two", "three")
    w.pack()

    mainloop()


def clicker_new():
    parent = Tk()
    parent.overrideredirect(1)  # Avoid it appearing and then disappearing quickly
    parent.withdraw()  # Hide the window as we do not want to see this one
    string_value = simpledialog.askstring("user", "Enter username")
    parent.quit()
    return string_value


old_user_button = Button(root, text="Choose username", command=clicker_old)
old_user_button.pack()
new_user_button = Button(root, text="New user", command=clicker_new)
new_user_button.pack()

root.mainloop()

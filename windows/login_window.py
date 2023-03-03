import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *

from db_controller import DataBase
from windows.main_window import MainWindow


class LoginWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Вход в систему")
        self.geometry("350x160")

        self.login_label = Label(self, text='Логин')
        self.login_label.pack(side=TOP, anchor=W, padx=50)

        self.login_entry = Entry(self, width=40)
        self.login_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.password_label = Label(self, text='Пароль')
        self.password_label.pack(side=TOP, anchor=W, padx=50)

        self.password_entry = Entry(self, width=40, show="\u25CF")
        self.password_entry.bind('<Return>', self.login_button_click)
        self.password_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.buttons_frame = Frame(self)

        self.login_button = Button(self.buttons_frame, text='Вход', command=lambda: self.login_button_click(None))
        self.login_button.pack(side=LEFT)

        self.cancel_button = Button(self.buttons_frame, text='Отмена', command=lambda: self.destroy())
        self.cancel_button.pack(side=LEFT)

        self.buttons_frame.pack(side=TOP)

        self.mainloop()

    def login_button_click(self, event):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        user_role = DataBase.get_user(login, password)
        # 1 - admin
        if user_role is not None:
            self.destroy()
            main_window = MainWindow(user_role)
        else:
            tkinter.messagebox.showerror('Ошибка', message='Неправильный логин или пароль.')

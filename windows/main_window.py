from tkinter import *
from tkinter.ttk import *

from windows.student_window import StudentWindow


# () - наследование
class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("База данных студентов")
        self.geometry("1024x768")

        self.groups_combobox = Combobox(values=['АСУ1', 'АСУ2', 'АСУ3'])
        self.groups_combobox.grid(row=0, column=0, sticky=N, padx=20, pady=20)

        columns = ('fullname', 'birth_date', 'phone', 'address', 'group', 'average_mark')
        self.table = Treeview(columns=columns, show='headings')
        self.table.heading('fullname', text='ФИО')
        self.table.heading('birth_date', text='Дата рождения')
        self.table.heading('phone', text='Телефон')
        self.table.heading('address', text='Адрес')
        self.table.heading('group', text='Группа')
        self.table.heading('average_mark', text='Успеваемость')
        self.table.column('fullname', width=160)
        self.table.column('birth_date', width=95)
        self.table.column('phone', width=110)
        self.table.column('address', width=160)
        self.table.column('group', width=70)
        self.table.column('average_mark', width=95)
        self.table.grid(row=0, column=1, columnspan=3, padx=20, pady=20)

        self.buttons_frame = Frame()

        self.add_button = Button(self.buttons_frame, text='Добавить', command=self.add_button_click)
        self.add_button.pack(side=LEFT)

        self.delete_button = Button(self.buttons_frame, text='Удалить')
        self.delete_button.pack(side=LEFT)

        self.buttons_frame.grid(row=1, column=3, sticky=E, padx=20)

    def add_button_click(self):
        student_window = StudentWindow()

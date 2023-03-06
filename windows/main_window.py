from tkinter import *
from tkinter.ttk import *

from db_controller import DataBase
from windows.print_window import PrintWindow
from windows.student_window import StudentWindow


# () - наследование
class MainWindow(Tk):
    def __init__(self, role):
        super().__init__()
        self.title("База данных студентов")
        self.geometry("1024x675")

        self.groups = DataBase.get_groups()
        self.students = []

        self.left_frame = Frame(self)

        self.groups_combobox = Combobox(self.left_frame, values=['Все'] + [value[1] for value in self.groups], state='readonly')
        self.groups_combobox.set('Все')
        self.groups_combobox.bind("<<ComboboxSelected>>", self.update_table)
        self.groups_combobox.pack(side=TOP, anchor=W, pady=[0, 25])
        self.update_students()

        self.search_label = Label(self.left_frame, text='Поиск')
        self.search_label.pack(side=TOP, anchor=W)

        self.search_entry = Entry(self.left_frame, width=25)
        self.search_entry.bind('<KeyRelease>', self.on_search_entry_key_pressed)
        self.search_entry.pack(side=TOP, anchor=W)

        self.filters_value = IntVar()
        self.filters_value.set(1)
        self.all_student_radio = Radiobutton(text='Все', variable=self.filters_value, value=1)
        self.excellent_students_radio = Radiobutton(text='Отличники', variable=self.filters_value, value=2)
        self.male_students = Radiobutton(text='Мужчины', variable=self.filters_value, value=3)
        self.female_students = Radiobutton(text='Женщины', variable=self.filters_value, value=4)

        self.left_frame.grid(row=0, column=0, sticky=N, pady=20, padx=20)

        columns = ('id', 'fullname', 'birth_date', 'phone', 'address', 'group', 'average_mark')
        self.table = Treeview(columns=columns, show='headings')
        self.table.heading('id', text='Номер', command=lambda: self.sort_columns(0, False))
        self.table.heading('fullname', text='ФИО', command=lambda: self.sort_columns(1, False))
        self.table.heading('birth_date', text='Дата рождения')
        self.table.heading('phone', text='Телефон')
        self.table.heading('address', text='Адрес')
        self.table.heading('group', text='Группа', command=lambda: self.sort_columns(5, False))
        self.table.heading('average_mark', text='Успеваемость', command=lambda: self.sort_columns(6, False))
        self.table.column('id', width=70)
        self.table.column('fullname', width=160)
        self.table.column('birth_date', width=95)
        self.table.column('phone', width=110)
        self.table.column('address', width=160)
        self.table.column('group', width=70)
        self.table.column('average_mark', width=95)
        self.table.grid(row=0, column=1, columnspan=3, padx=20, pady=20)
        if role == 1:
            self.table.bind('<Double-1>', self.on_table_click)
        self.update_table(None)
        if role == 1:
            self.buttons_frame = Frame()

            self.add_button = Button(self.buttons_frame, text='Добавить', command=self.add_button_click)
            self.add_button.pack(side=LEFT)

            self.print_button = Button(self.buttons_frame, text='Печать', command=lambda: PrintWindow())
            self.print_button.pack(side=LEFT)

            self.save_button = Button(self.buttons_frame, text='Сохранить...')
            self.save_button.pack(side=LEFT)

            self.buttons_frame.grid(row=1, column=3, sticky=E, padx=20)
        self.mainloop()

    def update_table(self, event):
        for item in self.table.get_children():
            self.table.delete(item)
        self.update_students()
        for student in self.students:
            item = (student.id, f'{student.last_name} {student.first_name} {student.middle_name}',
                    student.birth_date, student.phone, student.address, student.group, student.average_mark)
            self.table.insert("", END, values=item)

    def update_students(self):
        self.students = DataBase.get_students(
            self.groups[self.groups_combobox.current() - 1][0] if self.groups_combobox.current() != 0 else None)

    def on_search_entry_key_pressed(self, event):
        self.update_table(event)
        text = self.search_entry.get()
        s = [(self.table.set(i, 1), i) for i in self.table.get_children("")]
        for item in s:
            if item[0].count(text) == 0:
                self.table.delete(item[1])

    def sort_columns(self, index, direction):
        s = [(self.table.set(i, index), i) for i in self.table.get_children("")]
        s.sort(reverse=direction)
        for i, (_, k) in enumerate(s):
            self.table.move(k, "", i)
        self.table.heading(index, command=lambda: self.sort_columns(index, not direction))

    def add_button_click(self):
        student_window = StudentWindow()
        # TODO: ГОВНОКОД
        student_window.add_button.bind('<Destroy>', self.update_table)

    def on_table_click(self, event):
        for selected_item in self.table.selection():
            id = int(self.table.item(selected_item)['values'][0])
            student_window = StudentWindow(student=id)
            # TODO: ГОВНОКОД №2
            student_window.add_button.bind('<Destroy>', self.update_table)
            break



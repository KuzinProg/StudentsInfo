import datetime
import os.path
import pathlib
import shutil
from tkinter import filedialog, TOP, W, LEFT, Canvas, NW, N, Toplevel
from tkinter.ttk import Frame, Label, Entry, Combobox, Button

from PIL import ImageTk, Image
from tkcalendar import *

from db_controller import DataBase
from student import Student


class StudentWindow(Toplevel):
    def __init__(self, student=None):
        super().__init__()
        self.title("Студент")
        self.geometry("550x540")
        self.grab_set()

        self.file_name = ''
        self.student = student
        self.img = None

        self.left_side = Frame(self)

        self.last_name_label = Label(self.left_side, text='Фамилия')
        self.last_name_label.pack(side=TOP, anchor=W, padx=50)

        self.last_name_entry = Entry(self.left_side, width=40)
        self.last_name_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.first_name_label = Label(self.left_side, text='Имя')
        self.first_name_label.pack(side=TOP, anchor=W, padx=50)

        self.first_name_entry = Entry(self.left_side, width=40)
        self.first_name_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.middle_name_label = Label(self.left_side, text='Отчество')
        self.middle_name_label.pack(side=TOP, anchor=W, padx=50)

        self.middle_name_entry = Entry(self.left_side, width=40)
        self.middle_name_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.birth_date_label = Label(self.left_side, text='Дата рождения')
        self.birth_date_label.pack(side=TOP, anchor=W, padx=50)

        self.birth_date_entry = DateEntry(self.left_side, width=37)
        self.birth_date_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.gender_label = Label(self.left_side, text='Пол')
        self.gender_label.pack(side=TOP, anchor=W, padx=50)

        self.gender_combobox = Combobox(self.left_side, values=['Мужской', 'Женский'], width=37, state='readonly')
        self.gender_combobox.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.phone_label = Label(self.left_side, text='Номер телефона')
        self.phone_label.pack(side=TOP, anchor=W, padx=50)

        self.phone_entry = Entry(self.left_side, width=40)
        self.phone_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.address_label = Label(self.left_side, text='Адрес')
        self.address_label.pack(side=TOP, anchor=W, padx=50)

        self.address_entry = Entry(self.left_side, width=40)
        self.address_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.group_label = Label(self.left_side, text='Группа')
        self.group_label.pack(side=TOP, anchor=W, padx=50)

        self.groups = DataBase.get_groups()
        self.group_combobox = Combobox(self.left_side, values=[value[1] for value in self.groups], width=37, state='readonly')
        self.group_combobox.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.average_mark_label = Label(self.left_side, text='Средний балл')
        self.average_mark_label.pack(side=TOP, anchor=W, padx=50)

        self.average_mark_entry = Entry(self.left_side, width=40)
        self.average_mark_entry.pack(side=TOP, anchor=W, padx=50, pady=[0, 15])

        self.buttons_frame = Frame(self)

        self.add_button = Button(self.buttons_frame, text='Добавить', command=self.add_button_click)
        self.add_button.pack(side=LEFT)

        self.cancel_button = Button(self.buttons_frame, text='Отменить', command=lambda: self.destroy())
        self.cancel_button.pack(side=LEFT)

        self.right_side = Frame(self)
        # , highlightthickness=2, highlightbackground='#121212'
        self.photo_canvas = Canvas(self.right_side, bg="white", width=150, height=175)
        self.photo_canvas.pack(side=TOP)
        self.upload_button = Button(self.right_side, text='Загрузить...', command=self.upload_button_click)
        self.upload_button.pack(side=TOP)

        self.left_side.grid(row=0, column=0)
        self.right_side.grid(row=0, column=1, sticky=N, pady=15)
        self.buttons_frame.grid(row=1, column=0, columnspan=2)

        if student is not None:
            self.add_button.configure(text='Сохранить')

            student = DataBase.get_student(student)
            self.last_name_entry.insert(0, student.last_name)
            self.first_name_entry.insert(0, student.first_name)
            self.middle_name_entry.insert(0, student.middle_name)
            date = datetime.datetime.strptime(student.birth_date, "%Y-%m-%d")
            self.birth_date_entry.set_date(date)
            self.gender_combobox.set(student.gender)
            self.phone_entry.insert(0, student.phone)
            self.address_entry.insert(0, student.address)
            self.group_combobox.set(student.group)
            self.average_mark_entry.insert(0, student.average_mark)
            if student.photo is not None:
                self.file_name = student.photo
                self.update_image(student.photo)



    def add_button_click(self):
        if self.student is None:
            student = Student(None, self.first_name_entry.get(), self.last_name_entry.get(), self.middle_name_entry.get(),
                              self.gender_combobox.get(), self.file_name, self.birth_date_entry.get_date(), self.phone_entry.get(),
                              self.address_entry.get(),
                              self.groups[self.group_combobox.current()][0], float(self.average_mark_entry.get()))
            DataBase.add_student(student)
        else:
            student = Student(self.student, self.first_name_entry.get(), self.last_name_entry.get(), self.middle_name_entry.get(),
                              self.gender_combobox.get(), self.file_name, self.birth_date_entry.get_date(),
                              self.phone_entry.get(), self.address_entry.get(),
                              self.groups[self.group_combobox.current()][1], float(self.average_mark_entry.get()))
            DataBase.update_student(student)
        self.destroy()

    def update_image(self, file_name):
        path = f'{pathlib.Path(__file__).parent.parent}/photos/{file_name}'
        self.img = Image.open(path).resize((150, 175))
        self.img = ImageTk.PhotoImage(self.img)
        self.photo_canvas.create_image(0, 0, anchor=NW, image=self.img)

    def upload_button_click(self):
        file = filedialog.askopenfile(filetypes=[('Файлы изображений', '.png .jpg .jpeg')])
        if file is not None:
            src = file.name
            path = pathlib.Path(__file__).parent.parent
            dst = f'{path}/photos/{os.path.basename(src)}'
            shutil.copy(src, dst)
            self.file_name = os.path.basename(src)
            self.update_image(self.file_name)

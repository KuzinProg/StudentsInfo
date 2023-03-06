from tkinter import Toplevel, LEFT, Button, NW, Frame

from PIL import ImageTk, Image


class PrintWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Печать")
        self.geometry("500x200")

        self.main_frame = Frame(self)

        self.first_printer_image = ImageTk.PhotoImage(Image.open('windows/printer1.png').resize((70, 70)))
        self.first_printer_button = Button(self.main_frame, width=70, height=70, image=self.first_printer_image)
        self.first_printer_button.pack(side=LEFT, padx=[0, 20])

        self.second_printer_image = ImageTk.PhotoImage(Image.open('windows/printer2.png').resize((70, 70)))
        self.second_printer_button = Button(self.main_frame, width=70, height=70, image=self.second_printer_image)
        self.second_printer_button.pack(side=LEFT)

        self.main_frame.pack(expand=True, anchor="c")

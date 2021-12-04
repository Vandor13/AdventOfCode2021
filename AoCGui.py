from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import scrolledtext

EXAMPLE_DATA = ""

class AoCGui:

    def __init__(self):
        self.window = Tk()
        self.data_lines = []
        self.label = Label(self.window, text="")
        self.text_box = scrolledtext.ScrolledText(self.window, width=40, height=10)
        self.part = IntVar()
        self.part.set(1)
        self.result = scrolledtext.ScrolledText(self.window, width=40, height=2)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()

    def set_label(self, text):
        self.label.configure(text=text)

    def load_file(self):
        filename = filedialog.askopenfilename()
        with open(filename, "r") as file:
            data_strings = file.readlines()
        self.text_box.delete("1.0", END)
        for data in data_strings:
            self.text_box.insert(INSERT, data)

    def prepare_gui(self, window_title, button_label, example_data):
        self.window.title(window_title)
        self.window.geometry("700x400")

        self.text_box.insert(INSERT, example_data)

        self.text_box.grid(column=0, row=0)

        button = Button(self.window, text=button_label, command=self.button_pressed)
        button.grid(column=0, row=4)

        self.label.grid(column=0, row=5)

        radio_button_1 = Radiobutton(self.window, text="Part 1", value=1, var=self.part)
        radio_button_2 = Radiobutton(self.window, text="Part 2", value=2, var=self.part)
        radio_button_1.grid(column=0, row=2)
        radio_button_2.grid(column=0, row=3)

        self.result.grid(column=0, row=5)

        part_label = Label(self.window, text="Select part:")
        part_label.grid(column=0, row=1)

        menu = Menu(self.window)
        # menu.add_command(label="File")
        new_item = Menu(menu, tearoff=0)
        new_item.add_command(label="Open", command=self.load_file)
        menu.add_cascade(label="File", menu=new_item)
        self.window.config(menu=menu)

        self.window.mainloop()

    def load_text_box_data(self):
        self.data_lines = self.text_box.get("1.0", END).split("\n")

    def write_result(self, text):
        self.result.delete('1.0', END)
        self.result.insert(INSERT, text)


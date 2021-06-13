"""
    Author: Israel Dryer
    Modified: 2021-06-13
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialog import filedialog


class Application(ttk.Application):
    def __init__(self):
        super().__init__(title="Text Reader")
        self.reader = Reader(self)
        self.reader.pack(fill=BOTH, expand=YES)


class Reader(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=10)
        self.filename = ttk.StringVar()

        # scrolled text with custom highlight colors
        self.text_area = ttk.ScrolledText(self, bootstyle=ROUNDED)
        self.text_area.pack(fill=BOTH)

        # insert default text in text area
        self.text_area.insert(END, "Click the browse button to open a new text file.")

        # filepath
        ttk.Entry(self, textvariable=self.filename).pack(side=LEFT, fill=X, expand=YES, padx=(0, 2), pady=4)

        # browse button
        ttk.Button(self, text="Browse", command=self.open_file).pack(side=RIGHT, fill=X, padx=(2, 0), pady=4)

    def open_file(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        with open(path, encoding="utf-8") as f:
            self.text_area.delete("1.0", END)
            self.text_area.insert(END, f.read())
            self.filename.set(path)


if __name__ == "__main__":
    Application().run()

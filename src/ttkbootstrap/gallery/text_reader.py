"""
    Author: Israel Dryer
    Modified: 2021-04-07
"""
import ttkbootstrap as ttk
from tkinter.filedialog import askopenfilename

class Application(ttk.Window):

    def __init__(self):
        super().__init__(title="Text Reader")
        self.reader = Reader(self)
        self.reader.pack(fill='both', expand='yes')


class Reader(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=10)
        self.filename = ttk.StringVar()

        # scrolled text with custom highlight colors
        self.text_area = ttk.ScrolledText(self)
        self.text_area.pack(fill='both')

        # insert default text in text area
        self.text_area.insert('end', 'Click the browse button to open a new text file.')

        # filepath
        ttk.Entry(self, textvariable=self.filename).pack(side='left', fill='x', expand='yes', padx=(0, 2), pady=4)

        # browse button
        ttk.Button(self, text='Browse', command=self.open_file).pack(side='right', fill='x', padx=(2, 0), pady=4)

    def open_file(self):
        path = askopenfilename()
        if not path:
            return

        with open(path, encoding='utf-8') as f:
            self.text_area.delete('1.0', 'end')
            self.text_area.insert('end', f.read())
            self.filename.set(path)


if __name__ == '__main__':
    Application().mainloop()

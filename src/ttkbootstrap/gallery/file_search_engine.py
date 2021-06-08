"""
    Author: Israel Dryer
    Modified: 2021-04-09
    Adapted for ttkbootstrap from: https://github.com/israel-dryer/File-Search-Engine-Tk
"""
import csv
import datetime
import pathlib
import tkinter
from queue import Queue
from threading import Thread
import ttkbootstrap as ttk
from tkinter.filedialog import askdirectory, asksaveasfilename

class Application(ttk.Window):

    def __init__(self):
        super().__init__(
            title="File Search Engine",
            theme="journal"
            )
        self.search = SearchEngine(self, padding=10)
        self.search.pack(fill='both', expand='yes')


class SearchEngine(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # application variables
        self.search_count = 0

        # container for user input
        input_labelframe = ttk.Labelframe(self, text='Complete the form to begin your search', padding=(20, 10, 10, 5))
        input_labelframe.pack(side='top', fill='x')
        input_labelframe.columnconfigure(1, weight=1)

        # file path input
        ttk.Label(input_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        self.search_path = ttk.Entry(input_labelframe, text=pathlib.Path().absolute())
        self.search_path.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b1 = ttk.Button(input_labelframe, text='Browse', command=self.on_browse)
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        # search term input
        ttk.Label(input_labelframe, text='Term').grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        self.search_term = ttk.Entry(input_labelframe, text='txt')
        self.search_term.grid(row=1, column=1, sticky='ew', padx=10, pady=2)
        b2 = ttk.Button(input_labelframe, text='Search', command=self.on_search, bootstyle = 'outline')
        b2.grid(row=1, column=2, sticky='ew', pady=2)

        # search type selection
        ttk.Label(input_labelframe, text='Type').grid(row=2, column=0, padx=10, pady=2, sticky='ew')
        option_frame = ttk.Frame(input_labelframe, padding=(15, 10, 0, 10))
        option_frame.grid(row=2, column=1, columnspan=2, sticky='ew')
        self.search_type = ttk.Radiobutton(option_frame, text='Contains', value='contains', group='search-type')
        self.search_type.pack(side='left', fill='x', pady=2, padx=10)
        r2 = ttk.Radiobutton(option_frame, text='StartsWith', value='startswith', group='search-type')
        r2.pack(side='left', fill='x', pady=2, padx=10)
        r3 = ttk.Radiobutton(option_frame, text='EndsWith', value='endswith', group='search-type', default=True)
        r3.pack(side='left', fill='x', pady=2, padx=10)

        # search results tree
        self.tree = ttk.Treeview(self, bootstyle='info')
        self.tree.pack(fill='both', pady=5)
        self.tree['columns'] = ('modified', 'type', 'size', 'path')
        self.tree.column('#0', width=400)
        self.tree.column('modified', width=150, stretch=False, anchor='e')
        self.tree.column('type', width=50, stretch=False, anchor='e')
        self.tree.column('size', width=50, stretch=False, anchor='e')
        self.tree.heading('#0', text='Name')
        self.tree.heading('modified', text='Modified date')
        self.tree.heading('type', text='Type')
        self.tree.heading('size', text='Size')
        self.tree.heading('path', text='Path')

        # progress bar
        self.progressbar = ttk.Progressbar(self, mode='indeterminate', bootstyle='success striped')
        self.progressbar.pack(fill='x', pady=5)

        # right-click menu for treeview
        self.menu = tkinter.Menu(self, tearoff=False)
        self.menu.add_command(label='Reveal in file manager', command=self.on_doubleclick_tree)
        self.menu.add_command(label='Export results to csv', command=self.export_to_csv)

        # event binding
        self.tree.bind('<Double-1>', self.on_doubleclick_tree)
        self.tree.bind('<Button-3>', self.right_click_tree)

    def on_browse(self):
        """Callback for directory browse"""
        path = askdirectory(title='Directory')
        if path:
            self.search_path.text = path

    def on_doubleclick_tree(self, event=None):
        """Callback for double-click tree menu"""
        try:
            id = self.tree.selection()[0]
        except IndexError:
            return
        if id.startswith('I'):
            self.reveal_in_explorer(id)

    def right_click_tree(self, event=None):
        """Callback for right-click tree menu"""
        try:
            id = self.tree.selection()[0]
        except IndexError:
            return
        if id.startswith('I'):
            self.menu.entryconfigure('Export results to csv', state='disabled')
            self.menu.entryconfigure('Reveal in file manager', state='normal')
        else:
            self.menu.entryconfigure('Export results to csv', state='normal')
            self.menu.entryconfigure('Reveal in file manager', state='disabled')
        self.menu.post(event.x_root, event.y_root)

    def on_search(self):
        """Search for a term based on the search type"""
        search_term = self.search_term.text
        search_path = self.search_path.text
        search_type = self.search_type.value
        if search_term == '':
            return
        Thread(target=SearchEngine.file_search, args=(search_term, search_path, search_type), daemon=True).start()
        self.progressbar.start(10)
        self.search_count += 1
        id = self.tree.insert('', 'end', self.search_count, text=f'Search {self.search_count}')
        self.tree.item(id, open=True)
        self.check_queue(id)

    def reveal_in_explorer(self, id):
        """Callback for double-click event on tree"""
        values = self.tree.item(id, 'values')
        path = pathlib.Path(values[-1]).absolute().parent
        pathlib.os.startfile(path)

    def export_to_csv(self, event=None):
        """Export values to csv file"""
        try:
            id = self.tree.selection()[0]
        except IndexError:
            return

        filename = asksaveasfilename(initialfile='results.csv',
                                     filetypes=[('Comma-separated', '*.csv'), ('Text', '*.txt')])
        if filename:
            with open(filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Modified date', 'Type', 'Size', 'Path'])
                children = self.tree.get_children(id)
                for child in children:
                    name = [self.tree.item(child, 'text')]
                    values = list(self.tree.item(child, 'values'))
                    writer.writerow(name + values)
        # open file in explorer
        pathlib.os.startfile(filename)

    def check_queue(self, id):
        """Check file queue and print results if not empty"""
        if searching and not file_queue.empty():
            filename = file_queue.get()
            self.insert_row(filename, id)
            self.update_idletasks()
            self.after(1, lambda: self.check_queue(id))
        elif not searching and not file_queue.empty():
            while not file_queue.empty():
                filename = file_queue.get()
                self.insert_row(filename, id)
            self.update_idletasks()
            self.progressbar.stop()
        elif searching and file_queue.empty():
            self.after(100, lambda: self.check_queue(id))
        else:
            self.progressbar.stop()

    def insert_row(self, file, id):
        """Insert new row in tree search results"""
        try:
            file_stats = file.stat()
            file_name = file.stem
            file_modified = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%m/%d/%Y %I:%M:%S%p')
            file_type = file.suffix.lower()
            file_size = SearchEngine.convert_size(file_stats.st_size)
            file_path = file.absolute()
            iid = self.tree.insert(id, 'end', text=file_name, values=(file_modified, file_type, file_size, file_path))
            self.tree.selection_set(iid)
            self.tree.see(iid)
        except OSError:
            return

    @staticmethod
    def file_search(term, search_path, search_type):
        """Recursively search directory for matching files"""
        SearchEngine.set_searching(1)
        if search_type == 'contains':
            SearchEngine.find_contains(term, search_path)
        elif search_type == 'startswith':
            SearchEngine.find_startswith(term, search_path)
        elif search_type == 'endswith':
            SearchEngine.find_endswith(term, search_path)

    @staticmethod
    def find_contains(term, search_path):
        """Find all files that contain the search term"""
        for path, _, files in pathlib.os.walk(search_path):
            if files:
                for file in files:
                    if term in file:
                        file_queue.put(pathlib.Path(path) / file)
        SearchEngine.set_searching(False)

    @staticmethod
    def find_startswith(term, search_path):
        """Find all files that start with the search term"""
        for path, _, files in pathlib.os.walk(search_path):
            if files:
                for file in files:
                    if file.startswith(term):
                        file_queue.put(pathlib.Path(path) / file)
        SearchEngine.set_searching(False)

    @staticmethod
    def find_endswith(term, search_path):
        """Find all files that end with the search term"""
        for path, _, files in pathlib.os.walk(search_path):
            if files:
                for file in files:
                    if file.endswith(term):
                        file_queue.put(pathlib.Path(path) / file)
        SearchEngine.set_searching(False)

    @staticmethod
    def set_searching(state=False):
        """Set searching status"""
        global searching
        searching = state

    @staticmethod
    def convert_size(size):
        """Convert bytes to mb or kb depending on scale"""
        kb = size // 1000
        mb = round(kb / 1000, 1)
        if kb > 1000:
            return f'{mb:,.1f} MB'
        else:
            return f'{kb:,d} KB'


if __name__ == '__main__':
    file_queue = Queue()
    searching = False
    Application().mainloop()

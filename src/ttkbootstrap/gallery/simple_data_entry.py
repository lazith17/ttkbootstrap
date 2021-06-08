"""
    Author: Israel Dryer
    Modified: 2021-06-08
"""
import ttkbootstrap as ttk

class Application(ttk.Window):

    def __init__(self):
        super().__init__(title="Simple data entry form", theme="minty")
        self.form = EntryForm(self)
        self.form.pack(fill='both', expand='yes')


class EntryForm(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=(20, 10))
        self.columnconfigure(2, weight=1)

        # form headers
        ttk.Label(self, text='Please enter your contact information', width=60).grid(columnspan=3, pady=10)

        # create label/entry rows
        for i, label in enumerate(['name', 'address', 'phone']):
            self.setvar(label, value='')
            ttk.Label(self, text=label.title()).grid(row=i + 1, column=0, sticky='ew', pady=10, padx=(0, 10))
            ttk.Entry(self, textvariable=label).grid(row=i + 1, column=1, columnspan=2, sticky='ew')

        # submit button
        self.submit = ttk.Button(self, text='Submit', bootstyle='success', command=self.print_form_data)
        self.submit.grid(row=4, column=0, sticky='ew', pady=10, padx=(0, 10))

        # cancel button
        self.cancel = ttk.Button(self, text='Cancel', bootstyle='danger', command=self.quit)
        self.cancel.grid(row=4, column=1, sticky='ew')

    def print_form_data(self):
        print(self.getvar('name'), self.getvar('address'), self.getvar('phone'))


if __name__ == '__main__':
    Application().mainloop()

import ttkbootstrap as ttk
from ttkbootstrap.dialog import Dialog
from ttkbootstrap.dialog import messagebox

class QueryDialog(Dialog):

    def __init__(self, parent, title, prompt, initialvalue=None, minvalue=None, maxvalue=None, errormessage=None, vartype=None):
        self.prompt = prompt
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.initialvalue = initialvalue
        self.errormessage = errormessage
        self.vartype = vartype
        Dialog.__init__(self, parent, title)

    def destroy(self):
        self.entry = None
        Dialog.destroy(self)

    def body(self, master):
        ttk.Label(master, text=self.prompt, justify='left').grid(row=0, padx=5, pady=1, sticky='w')
        self.entry = ttk.Entry(master, name="entry", text=self.initialvalue)
        self.entry.grid(row=1, padx=5, sticky="we")
        self.entry.select_range(0, 'end')
        return self.entry
    
    def validate(self):
        try:
            if self.vartype == int:
                self.result = self.getint(self.entry.get())
            elif self.vartype == float:
                self.result = self.getdouble(self.entry.get())
            else:
                self.result = self.entry.get()
                return 1

        except ValueError:
            self.bell()
            messagebox.showwarning(parent=self, title="Illegal value", message=self.errormessage + "\nPlease try again")
            return 0

        if self.minvalue is not None and self.result < self.minvalue:
            self.bell()
            messagebox.showwarning(
                parent=self, 
                title="Too small", 
                message=f"The allowed minimum value is {self.minvalue}. Please try again.")
            return 0
        
        if self.maxvalue is not None and self.result > self.maxvalue:
            self.bell()
            messagebox.showwarning(
                parent=self, 
                title="Too large", 
                message=f"The allowed maximum value is {self.maxvalue}. Please try again.")
            return 0
        return 1


#---------CONVENIENCE METHODS------------------------------------------------------------------------------------------

def askinteger(parent, title, prompt, **kw):
    """Get an integer from the user.

    Args:
        parent: The parent widget.
        title (str): The dialog title.
        prompt (str): The label text.
        **kw: See the SimpleDialog and QueryDialog classes

    Returns:
        int: an integer value
    """
    i = QueryDialog(parent, title, prompt, errormessage="Not an integer", vartype=int, **kw)
    return i.result


def askfloat(parent, title, prompt, **kw):
    """Get an integer from the user.

    Args:
        parent: The parent widget.
        title (str): The dialog title.
        prompt (str): The label text.
        **kw: See the SimpleDialog class

    Returns:
        float: a float value.
    """
    i = QueryDialog(parent, title, prompt, errormessage="Not a float", vartype=float, **kw)
    return i.result

def askstring(parent, title, prompt, **kw):
    """Get an integer from the user.

    Args:
        parent: The parent widget.
        title (str): The dialog title.
        prompt (str): The label text.
        **kw: See the SimpleDialog class

    Returns:
        str: a string.
    """
    i = QueryDialog(parent, title, prompt, errormessage="Not a string", vartype=str, **kw)
    return i.result


# TODO When a message is shown from a top level that already exists... the <Return> bind does not seem
#   to transfer to the new toplevel.

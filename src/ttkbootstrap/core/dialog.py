from abc import abstractmethod
from src.ttkbootstrap.widgets import button
import ttkbootstrap as ttk
from tkinter import Toplevel, _get_default_root
from ttkbootstrap.core import DialogImages
from ttkbootstrap.core.themes import ThemeColors


class Dialog(Toplevel):
    """A class to open dialogs.

    This class is intended as a base class for custom dialogs
    """

    def __init__(self, parent, title=None):
        """Initialize a dialog

        Args:
            parent: The parent widget.
            title (str): The dialog title.
        """
        master = parent or _get_default_root("create a dialog window")

        Toplevel.__init__(self, master)
        self.parent = parent
        self.title(title)
        self.result = None
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # hide window until ready & set window type
        self.withdraw()
        if self._windowingsystem == "x11":
            self.attributes("-type", "dialog")

        # add body
        body = ttk.Frame(self)
        body.pack(padx=5, pady=5)

        # set focus
        self.initial_focus = self.body(body)
        if not self.initial_focus:
            self.initial_focus = self

        # add buttons
        self.button_box(self)

        ## get the geometry of the master widget
        self.update_idletasks()
        self.transient(parent)
        if self.parent.winfo_ismapped():
            m_width = self.parent.winfo_width()
            m_height = self.parent.winfo_height()
            m_x = self.parent.winfo_rootx()
            m_y = self.parent.winfo_rooty()
        else:
            m_width = self.parent.winfo_screenwidth()
            m_height = self.parent.winfo_screenheight()
            m_x = m_y = 0

        # get the geometry of the toplevel widget
        w_width = self.winfo_reqwidth()
        w_height = self.winfo_reqheight()
        x = int(min(max(m_x + (m_width - w_width) * 0.5, 0), self.parent.winfo_screenwidth()))
        y = int(min(max(m_y + (m_height - w_height) * 0.3, 0), self.parent.winfo_screenheight()))
        self.geometry(f"+{x}+{y}")
        self.deiconify()

        # show window
        self.deiconify()
        self.initial_focus.focus_set()
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    @abstractmethod
    def body(self, master):
        """Create a dialog body"""
        pass

    def button_box(self, master):
        """Add standard button box.

        Override if you do not want the standard buttons.
        """
        box = ttk.Frame(self)
        ttk.Button(box, text="OK", width=10, command=self.ok).pack(side="right", padx=5, pady=5)
        ttk.Button(box, text="Cancel", width=10, command=self.cancel).pack(side="right", padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def destroy(self):
        """Destroy the window"""
        self.initial_focus = None
        Toplevel.destroy(self)

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self):
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    @abstractmethod
    def validate(self):
        """Validate the data

        This method is called automatically to validate the data `before` the dialog is destroyed. By default, it
        always validates OK.
        """
        return True

    @abstractmethod
    def apply(self):
        """Process the data

        This method is called automatically to process the data, `after` the dialog is destroyed. By default, it does
        nothing.
        """
        pass


class SimpleDialog(Dialog):
    """Pops up a window message box and waits for user input"""

    def __init__(self, parent, title, message, buttons=[], icon=None, default=None, cancel=None):
        """
        Args:
            master: The parent widget.
            title (str): Text to appear in the title bar.
            message (str): Text to appear in the widget.
            buttons (List[str]): A list of button names to appear below the message text.
            icon (str): The name of the icon to appear on the left side of the message text. Legal values include: `info`, `warning`, `question`, `error`.
            default (int): The index of the default button from the ``buttons`` option. The ``<<Return>>`` event is bound to the default button.
        """
        self.action = None
        self._buttons = buttons
        self._cancel = cancel
        self._default = default
        self._icon = icon
        self._message = message

        super().__init__(parent, title=title)

    def body(self, master):
        """Create a message body; override superclass method"""
        # message container
        self.msg_frame = ttk.Frame(master, padding=15)
        self.msg_frame.pack(side="top", fill="x", expand="yes")

        # message icon
        img = DialogImages.__dict__.get(self._icon)
        if img:
            self.icon = ttk.PhotoImage(data=img)
            self.icon_lbl = ttk.Label(self.msg_frame, image=self.icon)
            self.icon_lbl.pack(side="left", padx=5, pady=5)

        # message text
        self.colors = self.msg_frame.colors
        self.message = ttk.Label(self.msg_frame, text=self._message, justify="left", wraplength=350)
        self.message.pack(padx=5, pady=5)

    def button_box(self, master):
        """Create a button box; override superclass method"""
        btn_bg_color = ThemeColors.update_hsv(self.colors.bg, vd=-0.2)
        self.btn_frame = ttk.Frame(master, padding=(10, 5), background=btn_bg_color)
        self.btn_frame.pack(fill="x")
        for index, btn in enumerate(self._buttons):
            btn_text = self._buttons[index]
            command = lambda x=index: self.done(x if index != self._cancel else None)
            btn = ttk.Button(self.btn_frame, text=btn_text, command=command)
            btn.pack(side="right", padx=2, pady=2)
            if index == self._default:
                btn.bind('<Return>', self.ok)

    def done(self, action):
        """Collect the action number when an action is completed, and close the window."""
        self.action = action
        self.cancel()

# -------------CONVENIENCE METHODS-------------------------------------------------------------------------------------

# MESSAGE TYPES
OK = ['Ok']
OKCANCEL = ['Cancel', 'Ok']
YESNO = ['No', 'Yes']
YESNOCANCEL = ['Cancel', 'No', 'Yes']
RETRYCANCEL = ['Cancel', 'Retry']

# ICONS
ERROR = 'error'
WARNING = 'warning'
QUESTION = 'question'
INFO = 'info'


def showinfo(parent=None, title=None, message=None):
    """Show an info message"""
    s = SimpleDialog(parent, title, message, OK, INFO, default=0)

def showwarning(parent=None, title=None, message=None):
    """Show a warning message"""
    s = SimpleDialog(parent, title, message, OK, WARNING, default=0)

def showerror(parent=None, title=None, message=None):
    """Show an error message"""
    s = SimpleDialog(parent, title, message, OK, ERROR, default=0)

def askquestion(parent=None, title=None, message=None):
    """Ask a question"""
    s = SimpleDialog(parent, title, message, YESNO, QUESTION, default=0)
    return s.action == 0

def askokcancel(parent=None, title=None, message=None):
    """Ask if operation should proceed; return true if the answer is ok"""
    s = SimpleDialog(parent, title, message, OKCANCEL, QUESTION, default=1, cancel=0)
    return s.action == 1

def askyesno(parent=None, title=None, message=None):
    """Ask a question; return True if the answer is YES."""
    s = SimpleDialog(parent, title, message, YESNO, QUESTION, default=1)
    return s.action == 1

def askyesnocancel(parent=None, title=None, message=None):
    """Ask a question; return True if the answer is YES, None if cancelled."""
    s = SimpleDialog(parent, title, message, YESNOCANCEL, QUESTION, default=2, cancel=0)
    return None if s.action == 0 else s.action == 2

def askretrycancel(parent=None, title=None, message=None):
    """Ask if operation should be retried; return True if the answer is yes."""
    s = SimpleDialog(parent, title, message, RETRYCANCEL, WARNING, default=1, cancel=0)
    return s.action == 1


if __name__ == '__main__':

    root = ttk.Window()
    answer = askretrycancel(root, title="Continue", message='Do you want to proceed with the operation?')
    print(answer)
    root.mainloop()
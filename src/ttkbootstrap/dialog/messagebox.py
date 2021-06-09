from ttkbootstrap.dialog import SimpleDialog, Dialog
import ttkbootstrap as ttk

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

def showwarning(parent, title=None, message=None):
    """Show a warning message"""
    s = SimpleDialog(parent, title, message, OK, WARNING, default=0)

def showerror(parent, title=None, message=None):
    """Show an error message"""
    s = SimpleDialog(parent, title, message, OK, ERROR, default=0)

def askquestion(parent, title=None, message=None):
    """Ask a question"""
    s = SimpleDialog(parent, title, message, YESNO, QUESTION, default=0)
    return s.action == 0

def askokcancel(parent, title=None, message=None):
    """Ask if operation should proceed; return true if the answer is ok"""
    s = SimpleDialog(parent, title, message, OKCANCEL, QUESTION, default=1, cancel=0)
    return s.action == 1

def askyesno(parent, title=None, message=None):
    """Ask a question; return True if the answer is YES."""
    s = SimpleDialog(parent, title, message, YESNO, QUESTION, default=1)
    return s.action == 1

def askyesnocancel(parent, title=None, message=None):
    """Ask a question; return True if the answer is YES, None if cancelled."""
    s = SimpleDialog(parent, title, message, YESNOCANCEL, QUESTION, default=2, cancel=0)
    return None if s.action == 0 else s.action == 2

def askretrycancel(parent, title=None, message=None):
    """Ask if operation should be retried; return True if the answer is yes."""
    s = SimpleDialog(parent, title, message, RETRYCANCEL, WARNING, default=1, cancel=0)
    return s.action == 1

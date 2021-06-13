from ttkbootstrap.dialog import SimpleDialog
from ttkbootstrap.constants import *

# MESSAGE TYPES
OK = ["Ok"]
OKCANCEL = ["Cancel", "Ok"]
YESNO = ["No", "Yes"]
YESNOCANCEL = ["Cancel", "No", "Yes"]
RETRYCANCEL = ["Cancel", "Retry"]




def showinfo(title=None, message=None, **kw):
    """Show an info message"""
    s = SimpleDialog(title, message, OK, INFO, default=0, **kw)
    s.show()


def showwarning(title=None, message=None, **kw):
    """Show a warning message"""
    s = SimpleDialog(title, message, OK, WARNING, default=0, **kw)
    s.show()


def showerror(title=None, message=None, **kw):
    """Show an error message"""
    s = SimpleDialog(title, message, OK, ERROR, default=0, **kw)
    s.show()


def askquestion(title=None, message=None, **kw):
    """Ask a question"""
    s = SimpleDialog(title, message, YESNO, QUESTION, default=0)
    s.show()
    return s.action == 0


def askokcancel(title=None, message=None, **kw):
    """Ask if operation should proceed; return true if the answer is ok"""
    s = SimpleDialog(title, message, OKCANCEL, QUESTION, default=1, cancel=0, **kw)
    s.show()
    return s.action == 1


def askyesno(title=None, message=None, **kw):
    """Ask a question; return True if the answer is YES."""
    s = SimpleDialog(title, message, YESNO, QUESTION, default=1, **kw)
    s.show()
    return s.action == 1


def askyesnocancel(title=None, message=None, **kw):
    """Ask a question; return True if the answer is YES, None if cancelled."""
    s = SimpleDialog(title, message, YESNOCANCEL, QUESTION, default=2, cancel=0, **kw)
    s.show()
    return None if s.action == 0 else s.action == 2


def askretrycancel(title=None, message=None, **kw):
    """Ask if operation should be retried; return True if the answer is yes."""
    s = SimpleDialog(title, message, RETRYCANCEL, WARNING, default=1, cancel=0, **kw)
    s.show()
    return s.action == 1

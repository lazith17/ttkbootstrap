"""
    A **ttkbootstrap** styled **OptionMenu** widget.
    Created: 2021-06-08
"""

import tkinter
from ttkbootstrap.widgets import Menubutton
from ttkbootstrap.constants import *


class OptionMenu(Menubutton):
    """A button with a drop-down menu that allows users to select from available options.

    !! WARNING !! This widget API is not compatable with the legacy ttk.OptionMenu extension widget.
    """

    def __init__(
        self,
        master=None,
        bootstyle=DEFAULT,
        defaultvalue=None,
        defaultindex=None,
        variable=None,
        command=None,
        values=[],
        **kw
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            defaultvalue (Any): The initial value to show on the button.
            defaultindex (int): The index of the initial value in a list of values.
            variable (Variable): A tkinter variable which stores the selected button value.
            command (func): A function that is evaluated whenever an option is selected.
            values (List): A list of options to include in the menu.
            **kw: Optional keyword arguments passed to the parent MenuButton widget.
        """
        # set the default selected value
        if defaultvalue:
            default = defaultvalue
        elif defaultindex and values:
            default = list(values)[defaultindex]
        else:
            default = None

        Menubutton.__init__(self, master=master, text=default, textvariable=variable, bootstyle=bootstyle, **kw)
        self._callback = command
        self["menu"] = tkinter.Menu(self, tearoff=False)
        self.set_menu(default, *values)

    def __getitem__(self, item):
        if item == "menu":
            return self.nametowidget(Menubutton.__getitem__(self, item))

        return Menubutton.__getitem__(self, item)

    def set_menu(self, default=None, *values):
        """Build a new menu of radiobuttons with *values and optionally a default value."""
        menu = self["menu"]
        menu.delete(0, "end")
        for val in values:
            menu.add_radiobutton(
                label=val, command=tkinter._setit(self.textvariable, val, self._callback), variable=self.textvariable
            )

        if default:
            self.textvariable.set(default)

    def destroy(self):
        """Destroy this widget and its associated variable."""
        try:
            del self.textvariable
        except AttributeError:
            pass
        super().destroy()

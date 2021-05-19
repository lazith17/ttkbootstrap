"""
    A ``ttkbootstrap`` abstract base class widgets.

    Created: 2021-05-12
    Author: Israel Dryer, israel.dryer@gmail.com

"""
import re
from abc import ABC

from tkinter.ttk import setup_master
from tkinter.ttk import Widget
from tkinter.ttk import _script_from_settings as script_from_settings

from ttkbootstrap.core.themes import DEFINITIONS
from ttkbootstrap.core.themes import COLOR_PATTERN, STYLE_PATTERN

WIDGET_PATTERN = re.compile(r"btn|button|progressbar|checkbutton|radiobutton|toggle|checkbtn|radiobtn|label|lbl")

WIDGET_LOOKUP = {
    "button": "TButton",
    "btn": "TButton",
    "progressbar": "TProgressbar",
    "checkbutton": "TCheckbutton",
    "checkbtn": "TCheckbutton",
    "radiobutton": "TRadiobutton",
    "radiobtn": "TRadiobutton",
    "toggle": "TCheckbutton",
    "label": "TLabel",
}


class Widget(Widget, ABC):
    """An abstract base class for all **ttkbootstrap** widgets."""

    def __init__(self, widgetclass, master=None, bootstyle=None, style=None, **kw):
        """
        Args:
            widgetclass (str): The base ``ttk`` style class, which can be found with the ``.winfo_class`` method.
            master (Widget, optional): The parent widget.
            bootstyle (str, optional): A string of **ttkbootstrap** style keywords.
            style (str, optional): A ``ttk`` style; will override ``bootstyle`` options.
            **kw (optional): Other widget options.
        """
        self.widgetclass = widgetclass
        self.master = setup_master(master)
        self.bootstyle = bootstyle.lower()
        self.style = style
        self.tk = self.master.tk
        self.settings = {}
        self.images = {}
        self.theme = DEFINITIONS.get(self.tk.call("ttk::style", "theme", "use"))
        self.colors = self.theme.colors
        self.themed_color = self.get_style_color()
        self.set_ttk_style()

    def update_ttk_style(self, settings):
        """Temporarily sets the current theme to themename, apply specified settings and then restore the previous
        theme.

        Args:
            settings (dict): Each key in settings is a style and each value may contain the keys `configure`, `map`,
                `layout` and `element create` and they are expected to have the same format as specified by the methods
                configure, map, layout and element_create respectively.
        """
        script = script_from_settings(settings)
        theme_name = self.tk.call("ttk::style", "theme", "use")
        self.theme = DEFINITIONS.get(theme_name)
        self.tk.call("ttk::style", "theme", "settings", self.theme.name, script)

    def get_style_color(self):
        """Identity themed color in the style name. Returns the matched name if found, otherwise None.

        Returns:
            str: The themed color found in the style name; ie. `primary`, `secondary`, etc...
        """
        if not self.bootstyle:
            return
        result = re.search(COLOR_PATTERN, self.bootstyle)
        if result:
            return result.group(0)
        else:
            return None

    def get_style_type(self):
        """Identity themed style in the style name. Returns the matched name if found, otherwise None.

        Returns:
            str: The themed style found in the style name; ie. `outline`, `link`, etc...
        """
        if not self.bootstyle:
            return
        result = re.search(STYLE_PATTERN, self.bootstyle)
        if result:
            return result.group(0)
        else:
            return None

    def get_widget_type(self):
        """Identity themed style in the style name. Returns the matched name if found, otherwise None.

        Returns:
            str: The themed style found in the style name; ie. `TButton`, `TLabel`, etc...
        """
        if not self.bootstyle:
            return
        result = re.search(WIDGET_PATTERN, self.bootstyle)
        if result:
            return result.group(0)
        else:
            return None

    def set_ttk_style(self):
        """Set the ``ttk`` style based on the ``style`` option if given, otherwise, build the ``style`` options from
        the ``bootstyle``
        """
        # use the ttk style
        if self.style:
            return

        # build ttk style from bootstyle parameters
        themed_style = self.get_style_type()
        widget_type = self.get_widget_type()
        c = "" if not self.themed_color else self.themed_color + "."
        s = "" if not themed_style else themed_style.title() + "."
        t = self.widgetclass if not widget_type else WIDGET_LOOKUP.get(widget_type) or self.widgetclass
        self.style = f"{c}{s}{t}"

"""
    A ``ttkbootstrap`` abstract base class widgets.

    Created: 2021-05-12
    Author: Israel Dryer, israel.dryer@gmail.com

"""
import re
from abc import ABC, abstractmethod

from tkinter import ttk
from ttkbootstrap.themes import DEFINITIONS, COLOR_PATTERN


STYLE_PATTERN = re.compile(r"outline|link|inverse|rounded|striped")
ORIENT_PATTERN = re.compile(r"horizontal|vertical")
WIDGET_LOOKUP = {
    "button": "TButton",
    "btn": "TButton",
    "progressbar": "TProgressbar",
    "progress": "TProgressbar",
    "check": "TCheckbutton",
    "checkbutton": "TCheckbutton",
    "checkbtn": "TCheckbutton",
    "combo": "TCombobox",
    "combobox": "TCombobox",
    "frame": "TFrame",
    "floodgauge": "TFloodgauge",
    "gauge": "TFloodgauge",
    "grip": "TSizegrip",
    "lbl": "TLabel",
    "label": "TLabel",
    "labelframe": "TLabelframe",  # labelframe could conflict with label, but this api
    "lblframe": "TLabelframe",  # is not likely to be used in that way... so ok for now.
    "lblfrm": "TLabelframe",
    "radio": "TRadiobutton",
    "radiobutton": "TRadiobutton",
    "radiobtn": "TRadiobutton",
    "roundtoggle": "Roundtoggle.Toolbutton",
    "separator": "TSeparator",
    "scrollbar": "TScrollbar",
    "sizegrip": "TSizegrip",
    "scale": "TScale",
    "slider": "TScale",
    "squaretoggle": "Squaretoggle.Toolbutton",
    "toggle": "Roundtoggle.Toolbutton",
    "toolbutton": "Toolbutton",
    "tool": "Toolbutton",
    "tree": "Treeview",
    "treeview": "Treeview",
}
WIDGET_PATTERN = "|".join(WIDGET_LOOKUP.keys())


class Widget(ttk.Widget, ABC):
    """An abstract base class for **ttkbootstrap** widgets."""

    def __init__(self, widgetclass, master=None, bootstyle=None, orient=None, style=None, **kw):
        """
        Args:
            widgetclass (str): The base ``ttk`` style class, which can be found with the ``.winfo_class`` method.
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
        """
        self.widgetclass = widgetclass
        self.master = ttk.setup_master(master)
        self.tk = self.master.tk
        self.style = style
        self.theme = DEFINITIONS.get(self.tk.call("ttk::style", "theme", "use"))
        try:
            self.colors = self.theme.colors
        except AttributeError:
            # not a ttkbootstrap theme
            pass
        self.customized = False
        self.settings = dict()
        self._bootstyle = bootstyle.lower()
        self._widget_id = None
        self._orient = orient
        self._bsoptions = []

        self._set_ttk_style()
        #self.after(100, lambda: self.bind("<<ThemeChanged>>", self.on_theme_change))

        # tkinter compatability
        self.config = self.configure

    @abstractmethod
    def _customize_widget(self):
        """Apply color customizations"""
        return NotImplementedError

    def _set_ttk_style(self):
        """Set the ``ttk`` style based on the ``style`` option if given, otherwise, build the ``style`` options from
        the ``bootstyle``
        """
        if not self.style:
            self.get_bootstyle()

    def configure(self, cnf=None, **kw):
        """Modify or query widget options."""
        options = set(self._bsoptions) & set(kw.keys())

        if not options:
            # adjust standard ttk options
            retval = super().configure(cnf=cnf, **kw)
            return retval
        else:
            # adjust bootstyle options
            bsoptions = {k: w for k, w in kw.items() if k in options}
            for k, w in bsoptions.items():
                self.__dict__[f"_{k}"] = w
            if "bootstyle" in bsoptions:
                self.get_bootstyle()
            self._customize_widget()

            # adjust standard ttk options
            ttkoptions = {k: w for k, w in kw.items() if k not in options}
            ttkoptions["style"] = self.style
            retval = super().configure(cnf, **ttkoptions) or {}
        return dict(**retval, **bsoptions)

    def on_theme_change(self, event):
        """Callback for <<ThemeChanged>> virtual event

        Args:
            event (Event): The event initiating the callback
        """
        theme_name = self.tk.call("ttk::style", "theme", "use")
        self.theme = DEFINITIONS.get(theme_name)
        try:
            self.colors = self.theme.colors
        except AttributeError:
            # Not a ttkbootstrap theme
            return
        if not self.style_exists(self.style):
            self._customize_widget()

    def update_ttk_style(self, settings):
        """Update a ttk theme using the settings dictionary.

        Args:
            settings (dict): A dictionary of settings used to create, configure, and map ttk styles.
        """
        script = ttk._script_from_settings(settings)
        theme_name = self.tk.call("ttk::style", "theme", "use")
        self.theme = DEFINITIONS.get(theme_name)
        self.colors = self.theme.colors
        self.tk.call("ttk::style", "theme", "settings", self.theme.name, script)

    def style_exists(self, style):
        """Query a style configuration and return if true, else return an empty string.

        Args:
            style (str): A ttk style to check.

        Returns:
            bool or ''
        """
        return self.tk.call("ttk::style", "configure", style, None)

    def get_style_color(self):
        """Identity themed color in the style name. Returns the matched name if found, otherwise None.

        Returns:
            str: The themed color found in the style name; ie. `primary`, `secondary`, etc...
        """
        if not self._bootstyle:
            return
        result = re.search(COLOR_PATTERN, self._bootstyle)
        if result:
            return result.group(0)
        else:
            return None

    def get_style_type(self):
        """Identity themed style in the style name. Returns the matched name if found, otherwise None.

        Returns:
            str or None: The themed style found in the style name; ie. `outline`, `link`, etc...
        """
        if not self._bootstyle:
            return
        result = re.search(STYLE_PATTERN, self._bootstyle)
        if result:
            return result.group(0).title()
        else:
            return None

    def get_widget_orientation(self):
        """Identify the widget orientation for widgets with such settings

        Returns:
            str: The widget orientation if existing.

        """
        if self._orient:
            result = re.search(ORIENT_PATTERN, self._orient.lower())
            return result.group(0)
        else:
            return None

    def get_widget_type(self):
        """Identity widget type in the style name. Returns the matched name if found, otherwise None.

        Returns:
            str or None: The themed style found in the style name; ie. `TButton`, `TLabel`, etc...
        """
        if not self._bootstyle:
            return
        result = re.search(WIDGET_PATTERN, self._bootstyle)
        if result:
            return result.group(0)
        else:
            return None

    def get_bootstyle(self):
        """Build the bootstyle from keywords"""
        self.themed_color = self.get_style_color()
        themed_style = self.get_style_type()
        widget_type = self.get_widget_type()
        widget_orient = self.get_widget_orientation()
        c = "" if not self.themed_color else self.themed_color + "."
        s = "" if not themed_style else themed_style.title() + "."
        o = "" if not widget_orient else widget_orient.title() + "."
        t = self.widgetclass if not widget_type else WIDGET_LOOKUP.get(widget_type) or self.widgetclass
        self.style = f"{c}{s}{o}{t}"

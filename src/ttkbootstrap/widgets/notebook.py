"""
    A **ttkbootstrap** styled **Notebook** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.themes import DEFAULT_FONT
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.widgets import Widget
from ttkbootstrap.constants import *

# TODO the background color affects the tab color only. Is this the desired behavior?
# TODO the tabs are not working on theme changes


class Notebook(Widget, ttk.Notebook):
    """A Notebook widget manages a collection of windows and displays a single one at a time. Each content window is
    associated with a tab, which the user may select to change the currently-displayed window."""

    def __init__(
        self,
        # widget options
        master=None,
        bootstyle=DEFAULT,
        cursor=None,
        height=None,
        padding=None,
        takefocus=True,
        width=None,
        style=None,
        # custom style options
        background=None,
        foreground=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            height (int): The widget's requested height in pixels.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            takefocus (bool): Determines whether the widget accepts the focus during keyboard traversal.
            width (int): The widget's requested width in pixels.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The notebook background color; setting this option will override theme settings.
            foreground (str): The color of the label text on the tab; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TNotebook", master=master, bootstyle=bootstyle, style=style)

        self._background = background
        self._foreground = foreground
        self._bsoptions = ["background", "foreground", "bootstyle"]
        self.register_style()

        ttk.Notebook.__init__(
            self,
            master=master,
            cursor=cursor,
            height=height,
            padding=padding,
            style=self.style,
            takefocus=takefocus,
            width=width,
            **kw,
        )

    def style_widget(self):

        # custom styles
        if any([self._background != None, self._foreground != None]):
            self.customized = True
            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

            options = {
                "theme": self.theme,
                "settings": self.settings,
                "background": self._background,
                "foreground": self._foreground,
                "style": self.style,
            }
            StylerTTK.style_notebook(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "background": self.themed_color,
                "style": self.style,
            }
            StylerTTK.style_notebook(**options)

"""
    A **ttkbootstrap** styled **Notebook** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Notebook(Widget, ttk.Notebook):
    """A Notebook widget manages a collection of windows and displays a single one at a time. Each content window is
    associated with a tab, which the user may select to change the currently-displayed window."""

    def __init__(
        self,

        # widget options
        master=None,
        bootstyle="default",
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
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.            takefocus (bool): Determines whether the window accepts the focus during keyboard traversal
            takefocus (bool): Determines whether the widget accepts the focus during keyboard traversal.
            width (int): The widget's requested width in pixels.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The notebook background color; setting this option will override theme settings.
            foreground (str): The color of the label text on the tab; setting this. Setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TNotebook", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.foreground = foreground
        self.widget_id = None

        self.customized = False
        self._customize_widget()

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

    def _customize_widget(self):

        if any([self.background != None, self.foreground != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background,
                "foreground": self.foreground,
                "style": self.style,
            }
            settings = StylerTTK.style_notebook(**options)

            self.update_ttk_style(settings)

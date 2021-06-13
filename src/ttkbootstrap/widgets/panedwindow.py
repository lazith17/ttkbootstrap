"""
    A **ttkbootstrap** styled **Panedwindow** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.widgets import Widget
from ttkbootstrap.constants import *


class PanedWindow(Widget, ttk.PanedWindow):
    """A PanedWindow widget displays a number of subwindows, stacked either vertically or horizontally. The user may
    adjust the relative sizes of the subwindows by dragging the sash between panes."""

    def __init__(
        self,
        # widget options
        master=None,
        bootstyle=DEFAULT,
        cursor=None,
        height=None,
        orient=VERTICAL,
        padding=None,
        takefocus=False,
        width=None,
        style=None,
        # style options
        sashcolor=None,
        sashthickness=5,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            height (int): The height of the widget in pixels.
            orient (str): orient (str): One of 'horizontal' or 'vertical'.  Specifies the orientation of the panedwindow.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            takefocus (bool): Determines whether the widget accepts the focus during keyboard traversal.
            width (int): The width of the widget in pixels.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            sashcolor (str): The color of the sash; setting this option will override theme settings.
            sashthickness (int): The thickness of the sash in pixels; default is 5; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TPanedwindow", master=master, bootstyle=bootstyle, style=style)

        self._sashcolor = sashcolor
        self._sashthickness = sashthickness
        self._bsoptions = ["sashcolor", "sashthickness", "bootstyle"]
        self.register_style()

        ttk.PanedWindow.__init__(
            self,
            master=master,
            cursor=cursor,
            height=height,
            orient=orient,
            padding=padding,
            style=self.style,
            takefocus=takefocus,
            width=width,
            **kw,
        )

    def style_widget(self):

        # custom styles
        if any([self._sashcolor != None, self._sashthickness != 5]):
            self.customized = True
            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

            options = {
                "theme": self.theme,
                "settings": self.settings,
                "sashcolor": self._sashcolor or self.themed_color,
                "sashthickness": self._sashthickness,
                "style": self.style,
            }
            StylerTTK.style_panedwindow(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "sashcolor": self.themed_color,
                "style": self.style,
            }
            StylerTTK.style_panedwindow(**options)

"""
    A **ttkbootstrap** styled **Panedwindow** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class PanedWindow(Widget, ttk.PanedWindow):
    """A PanedWindow widget displays a number of subwindows, stacked either vertically or horizontally. The user may 
    adjust the relative sizes of the subwindows by dragging the sash between panes."""

    def __init__(
        self,

        # widget options
        master=None,
        bootstyle="default",
        cursor=None,
        height=None,
        orient='horizontal',
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

        self.tk = master.tk
        self.sashcolor = sashcolor
        self.sashthickness = sashthickness
        self.widget_id = None

        self.customized = False
        self._customize_widget()

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

    def _customize_widget(self):

        if any([self.sashcolor != None, self.sashthickness != 5]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "sashcolor": self.sashcolor or self.themed_color,
                "sashthickness": self.sashthickness,
                "style": self.style,
            }
            settings = StylerTTK.style_panedwindow(**options)

            self.update_ttk_style(settings)

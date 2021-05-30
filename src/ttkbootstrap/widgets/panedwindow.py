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
    """A ttk.PanedWindow widget displays a number of subwindows, stacked either vertically or horizontally. The user
    may adjust the relative sizes of the subwindows by dragging the sash between panes."""

    def __init__(
        self,
        master=None,
        bootstyle="default",
        cursor=None,
        height=None,
        orient=None,
        padding=None,
        sashcolor=None,
        sashthickness=5,
        style=None,
        takefocus=False,
        width=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            height (int, optional): If present and greater than zero, specifies the desired height of the widget in
                pixels. Otherwise, the requested height is determined by the height of the managed windows.
            orient (str, optional): Specifies the orientation of the window. If vertical, subpanes are stacked
                top-to-bottom; if horizontal, subpanes are stacked left-to-right.
            padding (Any, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            sashcolor (str, optional): The color of the sash. Setting this option will override all other style-based
                sashcolor settings.
            sashthickness (int, optional): The thickness of the sash in pixels; default is 5.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            width (int, optional): If present and greater than zero, specifies the desired width of the widget in
                pixels. Otherwise, the requested width is determined by the width of the managed windows.

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
        self.bind("<<ThemeChanged>>", self.on_theme_change)

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

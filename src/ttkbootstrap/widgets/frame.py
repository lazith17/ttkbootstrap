"""
    A **ttkbootstrap** styled **Frame** widget.

    Created: 2021-05-25
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Frame(Widget, ttk.Frame):
    """A Frame widget is a container, used to group other widgets together."""

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        cursor=None,
        height=None,
        padding=None,
        style=None,
        takefocus=False,
        width=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            background (str, optional): The normal color to use on the Frame when displaying the widget. Setting
                this option will override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            height (int, optional): The widget's requested height in pixels.
            padding (Any, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            width (int, optional): The widget's requested width in pixels.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TFrame", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Frame.__init__(
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

        if self.background != None:
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background or self.themed_color,
                "style": self.style,
            }
            settings = StylerTTK.style_frame(**options)

            self.update_ttk_style(settings)

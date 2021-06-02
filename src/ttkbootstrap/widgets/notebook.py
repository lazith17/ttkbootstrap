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
        master=None,
        background=None,
        bootstyle="default",
        cursor=None,
        foreground=None,
        height=None,
        padding=None,
        style=None,
        takefocus=True,
        width=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            background (str, optional): The normal background color to use for the Notebook border and tab background.
                Setting this option will override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            foreground (str, optional): The color of the label text on the tab. Setting this option will override all
                other style-based foreground setting.
            height (int, optional): If present and greater than zero, specifies the desired height of the pane area
                (not including internal padding or tabs). Otherwise, the maximum height of all panes is used.
            padding (Any, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            width (int, optional): If present and greater than zero, specifies the desired width of the pane area
                (not including internal padding). Otherwise, the maximum width of all panes is used.

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

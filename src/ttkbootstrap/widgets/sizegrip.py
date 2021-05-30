"""
    A **ttkbootstrap** styled **Sizegrip** widget.

    Created: 2021-05-21
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Sizegrip(Widget, ttk.Sizegrip):
    """A Sizegrip widget (also known as a grow box) allows the user to resize the containing toplevel window by
    pressing and dragging the grip."""

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        cursor=None,
        foreground=None,
        style=None,
        takefocus=True,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            background (str, optional): The normal background color to use when displaying the widget. Setting this
                option will override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            foreground (str, optional): The color used to render the grip when displaying the widget. Setting this
                option will override all other style based foreground settings.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). To remove the widget from focus traversal, use ``takefocus=False``.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html                
        """

        Widget.__init__(self, "TSizegrip", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.foreground = foreground
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Sizegrip.__init__(
            self,
            master=master,
            cursor=cursor,
            style=self.style,
            takefocus=takefocus,
            **kw,
        )
        self.bind("<<ThemeChanged>>", self.on_theme_change)

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
                "foreground": self.foreground or self.themed_color,
                "style": self.style,
            }
            settings = StylerTTK.style_sizegrip(**options)

            self.update_ttk_style(settings)

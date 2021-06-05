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
    """A Sizegrip widget allows the user to resize the containing toplevel window by pressing and dragging the grip."""

    def __init__(
        self,

        # widget options
        master=None,
        bootstyle="default",
        cursor=None,
        takefocus=True,
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
            takefocus (bool): Adds or removes the widget from focus traversal.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The sizegrip background color; setting this option will override theme settings.
            foreground (str): The color of the grips; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html                
        """

        Widget.__init__(self, "TSizegrip", master=master, bootstyle=bootstyle, style=style)

        self.background = background
        self.foreground = foreground
        self._customize_widget()

        ttk.Sizegrip.__init__(
            self,
            master=master,
            cursor=cursor,
            style=self.style,
            takefocus=takefocus,
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
                "foreground": self.foreground or self.themed_color,
                "style": self.style,
            }
            settings = StylerTTK.style_sizegrip(**options)

            self.update_ttk_style(settings)

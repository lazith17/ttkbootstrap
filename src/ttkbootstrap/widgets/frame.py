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
        
        # widget options
        master=None,
        bootstyle="default",
        cursor=None,
        height=None,
        padding=None,
        takefocus=False,
        width=None,
        style=None,

        # custom style options
        background=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            height (int): The widget's requested height in pixels.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            takefocus (bool): Determines whether the window accepts the focus during keyboard traversal
            width (int): The widget's requested width in pixels.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The frame background color; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TFrame", master=master, bootstyle=bootstyle, style=style)

        self.background = background
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

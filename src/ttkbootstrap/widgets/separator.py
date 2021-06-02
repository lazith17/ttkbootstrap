"""
    A **ttkbootstrap** styled **Separator** widget.

    Created: 2021-05-22
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Separator(Widget, ttk.Separator):
    """A ttk.Separator widget displays a horizontal or vertical separator bar"""

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        cursor=None,
        orient='horizontal',
        sashthickness = 1,
        style=None,
        takefocus=False,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            background (str, optional): The normal color to use on the separator when displaying the widget. Setting 
                this option will override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            orient (str, optional): One of 'horizontal' or 'vertical'.  Specifies the orientation of the separator.
            sashthickness (int, optional): The thickness of the separator line in pixels. Default is 1.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
        
        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TSeparator", master=master, bootstyle=bootstyle, orient=orient, style=style)

        self.tk = master.tk
        self.background = background
        self.sashthickness = sashthickness
        self.orient = orient
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Separator.__init__(
            self,
            master=master,
            cursor=cursor,
            style=self.style,
            takefocus=takefocus,
            **kw,
        )

    def _customize_widget(self):

        if any([self.background != None, self.sashthickness != 1]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background or self.themed_color,
                "sashthickness": self.sashthickness,
                "style": self.style,
            }
            settings = StylerTTK.style_separator(**options)

            self.update_ttk_style(settings)

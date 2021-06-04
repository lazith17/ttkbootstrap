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
    """A Separator widget displays a horizontal or vertical separator bar"""

    def __init__(
        self,

        # widget options
        master=None,
        bootstyle="default",
        cursor=None,
        orient='horizontal',
        takefocus=False,
        style=None,

        # style options
        sashcolor=None,
        sashthickness = 1,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            orient (str): One of 'horizontal' or 'vertical'.  Specifies the orientation of the separator.
            takefocus (bool): Adds or removes the widget from focus traversal.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            sashcolor (str): The normal color to use on the separator when displaying the widget. Setting 
                this option will override all other style-based background settings.
            sashthickness (int): The thickness of the separator line in pixels. Default is 1.
        
        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TSeparator", master=master, bootstyle=bootstyle, orient=orient, style=style)

        self.tk = master.tk
        self.sashcolor = sashcolor
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

        if any([self.sashcolor != None, self.sashthickness != 1]):
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
            settings = StylerTTK.style_separator(**options)

            self.update_ttk_style(settings)

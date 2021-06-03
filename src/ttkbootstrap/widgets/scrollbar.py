"""
    A **ttkbootstrap** styled **Scrollbar** widget.

    Created: 2021-06-01
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Scrollbar(Widget, ttk.Scrollbar):
    """Scrollbar widgets are typically linked to an associated window that displays a document of some sort, such as a 
    file being edited or a drawing. A scrollbar displays a thumb in the middle portion of the scrollbar, whose 
    position and size provides information about the portion of the document visible in the associated window. The 
    thumb may be dragged by the user to control the visible region. Depending on the theme, two or more arrow buttons 
    may also be present; these are used to scroll the visible region in discrete units."""

    def __init__(
        self,

        # widget options
        master=None,
        bootstyle="default",
        command=None,
        cursor=None,
        orient="vertical",
        style=None,
        takefocus=False,
        
        # custom style options
        showarrows=True,
        thumbcolor=None,
        troughcolor=None,
        **kw,

    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            command (func): A function that is called when the view in the associate widget changes.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            orient (str): One of horizontal or vertical. Specifies the orientation of the scrollbar.
            takefocus (bool): Adds or removes the widget from focus traversal.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            showarrows (bool, optional): Show or hide the arrow buttons on the scrollbar; this option is ignored for 'rounded' scrollbar.
            thumbcolor (str, optional): The color of the scrollbar thumb; setting this option will override theme settings.
            troughcolor (str, optional): The color of the scrollbar trough; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TScrollbar", master=master, bootstyle=bootstyle, style=style, orient=orient)

        self.tk = master.tk
        self.showarrows = showarrows
        self.thumbcolor = thumbcolor
        self.troughcolor = troughcolor
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Scrollbar.__init__(
            self,
            master=master,
            command=command,
            cursor=cursor,
            orient=orient,
            style=self.style,
            takefocus=takefocus,
            **kw,
        )

    def _customize_widget(self):
        """Create a custom widget style if custom settings are used"""
        if any([self.troughcolor != None, self.thumbcolor != None, not self.showarrows]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "thumbcolor": self.thumbcolor or self.themed_color,
                "troughcolor": self.troughcolor,
                "orient": self.orient,
                "style": self.style,
                "showarrows": self.showarrows
            }
            settings = StylerTTK.style_scrollbar(**options)
            self.update_ttk_style(settings)

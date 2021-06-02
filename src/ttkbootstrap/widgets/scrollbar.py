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
        master=None,
        bootstyle="default",
        command=None,
        cursor=None,
        orient="vertical",
        style=None,
        takefocus=False,
        thickness=12,
        thumbcolor=None,
        troughcolor=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            command (func, optional): A script prefix to evaluate to change the view in the widget associated with the
                scrollbar. Additional arguments are appended to the value of this option whenever the user requests a 
                view change by manipulating the scrollbar.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            orient (str, optional): One of horizontal or vertical. Specifies the orientation of the scrollbar.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            thickness (int, optional): The widget's requested thickness in pixels along the short side of the widget.
            thumbcolor (str, optional): The normal color used on the Scrollbar thumb. Setting this option will override
                all other style-based thumbcolor settings.
            troughcolor (str, optional): The normal color to use on the Scrollbar trough. Setting this option will 
                override all other style-based troughcolor settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TScrollbar", master=master, bootstyle=bootstyle, style=style, orient=orient)

        self.tk = master.tk
        self.thickness = thickness
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
        if any([self.troughcolor != None, self.thumbcolor != None, self.thickness != 12]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "thickness": self.thickness,
                "thumbcolor": self.thumbcolor or self.themed_color,
                "troughcolor": self.troughcolor,
                "orient": self.orient,
                "style": self.style,
            }
            settings = StylerTTK.style_scrollbar(**options)
            self.update_ttk_style(settings)

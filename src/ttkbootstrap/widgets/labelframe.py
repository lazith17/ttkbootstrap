"""
    A **ttkbootstrap** styled **Labelframe** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_COLORS, ThemeColors
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Labelframe(Widget, ttk.Label):
    """A Labelframe widget is a container used to group other widgets together. It has an optional label, which may be 
    a plain text string or another widget."""

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        bordercolor=None,
        cursor=None,
        foreground=None,
        height=None,
        labelanchor=None,
        labelwidget=None,
        padding=None,
        style=None,
        takefocus=False,
        text=None,
        underline=None,
        width=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            background (str, optional): The normal color of the widget background. Setting this option will override 
                all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            bordercolor (str, optional): The color of the labelframe border.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            foreground (str, optional): The label text color.
            height (int, optional): If specified, the widget's requested height in pixels.
            labelanchor (str, optional): Specifies where to place the label. Allowed values are (clockwise from the top
                upper left corner): nw, n, ne, en, e, es, se, s,sw, ws, w and wn. 
            labelwidget (str, optional): The name of a widget to use for the label. If set, overrides the ``text`` 
                option. The ``labelwidget`` must be a child of the labelframe widget or one of the labelframe's 
                ancestors, and must belong to the same top-level widget as the labelframe.
            padding (Any, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            text (str, optional): Specifies the text of the label. 
            underline (int, optional): If set, specifies the integer index (0-based) of a character to underline in the
                text string. The underlined character is used for mnemonic activation.
            width (int, optional): The widget's requested width in pixels.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TLabelframe", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.bordercolor = bordercolor
        self.foreground = foreground
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Labelframe.__init__(
            self,
            master=master,
            cursor=cursor,
            height=height,
            labelanchor=labelanchor,
            labelwidget=labelwidget,
            padding=padding,
            style=self.style,
            takefocus=takefocus,
            text=text,
            underline=underline,
            width=width,
            **kw,
        )
        self.bind("<<ThemeChanged>>", self.on_theme_change)

    def _customize_widget(self):

        if any([self.background != None, self.foreground != None, self.bordercolor != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background or self.themed_color,
                "bordercolor": self.bordercolor,
                "foreground": self.foreground,
                "style": self.style,
            }

            settings = StylerTTK.style_labelframe(**options)
            self.update_ttk_style(settings)

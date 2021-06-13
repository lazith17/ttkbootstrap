"""
    A **ttkbootstrap** styled **Checkbutton** widget.

    Created: 2021-05-23
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.themes import DEFAULT_FONT
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.widgets import Widget
from ttkbootstrap.constants import *


class Checkbutton(Widget, ttk.Checkbutton):
    """A Checkbutton widget is used to show or change a setting. It has two states, selected and deselected. The state
    of the checkbutton may be linked to a tkinter variable.
    """

    def __init__(
        self,
        # widget options
        master=None,
        bootstyle=DEFAULT,
        command=None,
        compound=None,
        cursor=None,
        default=False,
        image=None,
        offvalue=0,
        onvalue=1,
        padding=None,
        state=NORMAL,
        takefocus=True,
        textvariable=None,
        text=None,
        underline=None,
        variable=None,
        width=None,
        style=None,
        # custom style options
        background=None,
        font=None,
        foreground=None,
        indicatorcolor=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            command (func): A function that is called when the checkbutton is invoked.
            compound (str): Controls the position of the text and image when both are displayed. Legal values include: `none`, `bottom`, `top`, `left`, `right`, `center`.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            default (bool): Sets the initial widget value to ``True`` or ``False``, which corresponds to ``selected`` or ``deselected``.
            image (PhotoImage): An image to display on the checkbutton. The position of the image is controlled by the ``compound`` option.
            offvalue (Any): The value of the checkbutton when in the (unchecked) state. Default is 0.
            onvalue (Any): The value of the checkbutton when in the (checked) state. Default is 1.
            padding (str): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            state (str): Either `normal` or `disabled`. A disabled state will prevent user input.
            takefocus (bool): Adds or removes the checkbutton from focus traversal.
            text (str): The text to display in the checkbutton label.
            textvariable (Variable): A tkinter variable whose value is used in place of the checkbutton label text.
            underline (int): The index of the character to underline in the checkbutton label.
            variable (Variable): A tkinter variable whose value is used to control the checkbutton value. If none is provided, it is generated automatically and can be accessed directly or via the ``value`` property.
            width (int): The absolute width of the text area; avg character size if text or pixels if an image.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The checkbutton background color; setting this option will override the theme settings.
            foreground (str): The checkbutton text color; setting this option will override theme settings.
            font (str): The font used to draw text inside the widget; setting this option will override theme settings.
            indicatorcolor (str): The color of the checkbutton indicator; setting this option will override the theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TCheckbutton", master=master, bootstyle=bootstyle, style=style)

        self.variable = variable or Variable(value=onvalue if default else offvalue)
        self._background = background
        self._font = font
        self._foreground = foreground
        self._indicatorcolor = indicatorcolor
        self._bsoptions = ["background", "font", "foreground", "indicatorcolor", "bootstyle"]
        self.register_style()

        ttk.Checkbutton.__init__(
            self,
            master=master,
            command=command,
            compound=compound,
            cursor=cursor,
            image=image,
            padding=padding,
            onvalue=onvalue,
            offvalue=offvalue,
            state=state,
            style=self.style,
            takefocus=takefocus,
            text=text,
            textvariable=textvariable,
            underline=underline,
            variable=self.variable,
            width=width,
            **kw,
        )

    @property
    def value(self):
        """Get the current value specified by the ``onvalue`` or ``offvalue``."""
        return self.variable.get()

    @value.setter
    def value(self, value):
        """Set the current value of the ``variable``"""
        self.variable.set(value)

    def style_widget(self):

        # custom styles
        if any([self._background != None, self._foreground != None, self._font != None, self._indicatorcolor != None]):
            self.customized = True
            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

            options = {
                "theme": self.theme,
                "settings": self.settings,
                "background": self._background,
                "foreground": self._foreground,
                "indicatorcolor": self._indicatorcolor,
                "font": self._font or DEFAULT_FONT,
                "style": self.style,
            }

            if "Roundtoggle" in self.style:
                StylerTTK.style_roundtoggle(**options)
            elif "Squaretoggle" in self.style:
                StylerTTK.style_squaretoggle(**options)
            elif "Outline.Toolbutton" in self.style:
                options.pop("foreground")
                StylerTTK.style_outline_toolbutton(**options)
            elif "Toolbutton" in self.style:
                options.pop("background")
                StylerTTK.style_toolbutton(**options)
            else:
                StylerTTK.style_checkbutton(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "indicatorcolor": self.themed_color,
                "style": self.style,
            }

            if "Roundtoggle" in self.style:
                StylerTTK.style_roundtoggle(**options)
            elif "Squaretoggle" in self.style:
                StylerTTK.style_squaretoggle(**options)
            elif "Outline.Toolbutton" in self.style:
                StylerTTK.style_outline_toolbutton(**options)
            elif "Toolbutton" in self.style:
                StylerTTK.style_toolbutton(**options)
            else:
                StylerTTK.style_checkbutton(**options)

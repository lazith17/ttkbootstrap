"""
    A **ttkbootstrap** styled **Menubutton** widget.
    Created: 2021-05-28
"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.themes import DEFAULT_FONT
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.widgets import Widget
from ttkbootstrap.constants import *


class Menubutton(Widget, ttk.Menubutton):
    """A Menubutton widget displays a textual label and/or image, and displays a menu when pressed.
    """

    def __init__(
        self,

        # widget options
        master=None,
        bootstyle=DEFAULT,
        compound=None,
        cursor=None,
        direction=None,
        font=None,
        image=None,
        menu=None,
        padding=None,
        showarrow=True,
        state=NORMAL,
        takefocus=True,
        textvariable=None,
        text=None,
        underline=None,
        width=None,
        style=None,

        # style options
        background=None,
        foreground=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.            
            compound (str): Controls the position of the text and image when both are displayed. Legal values include: `none`, `bottom`, `top`, `left`, `right`, `center`.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            direction (str): Specifies where the menu is to be popped up relative to the menubutton. Legal values include: `above`, `below`, `left`, `right`, or `flush`.
            image (PhotoImage): An image to display on the button. The position of the image is controlled by the ``compound`` option.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            showarrow (bool): Shows or hides the arrow on the combobox button.
            state (str): Either `normal` or `disabled`. A disabled state will prevent user input.
            takefocus (bool): Adds or removes the widget from focus traversal.
            text (str): Specifies a string to be displayed inside the widget.
            textvariable (Variable): A tkinter variable whose value is used in place of the button text.
            underline (int): The index of the character to underline.
            width (int): The absolute width of the text area; avg character size if text or pixels if an image.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The button background color; setting this option will override theme settings.
            foreground (str): The button text color; setting this option will override theme settings.
            font (str): The font used to draw text inside the widget; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TMenubutton", master=master, bootstyle=bootstyle, style=style)

        self.textvariable = textvariable or Variable(value=text)
        self._arrowsize = 0 if showarrow else 4
        self._background = background
        self._font = font
        self._foreground = foreground
        self._bsoptions = ['background', 'foreground', 'bootstyle']
        self.register_style()

        ttk.Menubutton.__init__(
            self,
            master=master,
            compound=compound,
            cursor=cursor,
            direction=direction,
            image=image,
            menu=menu,
            padding=padding,
            state=state,
            style=self.style,
            takefocus=takefocus,
            text=text,
            textvariable=self.textvariable,
            underline=underline,
            width=width,
            **kw,
        )

    def style_widget(self):

        # custom styles
        if any([self._background != None, self._foreground != None, self._font != None]):
            self.customized = True
            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

            options = {
                "theme": self.theme,
                "settings": self.settings,
                "background": self._background,
                "foreground": self._foreground,
                "font": self._font or DEFAULT_FONT,
                "style": self.style,
            }

            if "Outline" in self.style:
                self._foreground = self._foreground or self.themed_color
                StylerTTK.style_outline_menubutton(**options)
            else:
                self._background = self._background or self.themed_color
                StylerTTK.style_menubutton(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "style": self.style,
            }
            if "Outline" in self.style:
                options['foreground'] = self.themed_color
                StylerTTK.style_outline_menubutton(**options)
            else:
                options['background'] = self.themed_color
                StylerTTK.style_menubutton(**options)

    @property
    def text(self):
        """Return the button text"""
        return self.textvariable.get()

    @text.setter
    def text(self, value):
        """Set the button text"""
        self.textvariable.set(value=value)

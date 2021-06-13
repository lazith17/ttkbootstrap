"""
    A **ttkbootstrap** styled **Button** widget.

    Created: 2021-05-19
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.themes import DEFAULT_FONT
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.widgets import Widget
from ttkbootstrap.constants import *


class Button(Widget, ttk.Button):
    """A Button widget displays a textual string, bitmap or image. If text is displayed, it must all be in a single
    font, but it can occupy multiple lines on the screen (if it contains newlines or if wrapping occurs because of the
    ``wraplength`` option). One of the characters may optionally be underlined using the ``underline`` option. When a
    user invokes the button (by pressing mouse button 1 with the cursor over the button), then the command specified in
    the ``command`` option is invoked.
    """

    def __init__(
        self,
        # widget options
        master=None,
        bootstyle=DEFAULT,
        command=None,
        compound=None,
        cursor=None,
        image=None,
        padding=None,
        state=NORMAL,
        takefocus=True,
        text=None,
        textvariable=None,
        underline=None,
        width=None,
        wraplength=None,
        style=None,
        # custom style options
        anchor=CENTER,
        background=None,
        font="Helvetica 10",
        foreground=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            command (func): A function that is called when the button is pushed.
            compound (str): Controls the position of the text and image when both are displayed. Legal values include: `none`, `bottom`, `top`, `left`, `right`, `center`.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            image (PhotoImage): An image to display on the button. The position of the image is controlled by the ``compound`` option.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            state (str): Either `normal` or `disabled`. A disabled state will prevent the button from being pushed.
            takefocus (bool): Adds or removes the widget from focus traversal.
            text (str): Specifies a string to be displayed inside the widget.
            textvariable (Variable): A tkinter variable whose value is used in place of the button text.
            underline (int): The index of the character to underline.
            width (int): The absolute width of the text area; avg character size if text or pixels if an image.
            wraplength (int): The maximum line length in pixels.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            anchor (str): Controls how the text or image is positioned relative to the inner margins. Legal values include: `n`, `ne`, `e`, `se`, `s`, `sw`, `w`, `nw`, and `center`.
            background (str): The button background color; setting this option will override theme settings.
            font (str): The font used to draw text inside the widget; setting this option will override theme settings.
            foreground (str): The button text color; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TButton", master=master, bootstyle=bootstyle, style=style)

        self.textvariable = textvariable
        self._anchor = anchor
        self._background = background
        self._bootstyle = bootstyle
        self._font = font
        self._foreground = foreground
        self._bsoptions = ["anchor", "background", "font", "foreground", "bootstyle"]
        self.register_style()

        ttk.Button.__init__(
            self,
            master=self.master,
            command=command,
            compound=compound,
            cursor=cursor,
            image=image,
            padding=padding,
            state=state,
            style=self.style,
            takefocus=takefocus,
            text=text,
            textvariable=self.textvariable,
            underline=underline,
            width=width,
            wraplength=wraplength,
            **kw,
        )

    def style_widget(self):

        # custom styles
        if any(
            [self._background != None, self._foreground != None, self._anchor != CENTER, self._font != DEFAULT_FONT]
        ):
            self.customized = True
            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

            options = {
                "theme": self.theme,
                "settings": self.settings,
                "anchor": self._anchor,
                "background": self._background or self.themed_color,
                "font": self._font,
                "foreground": self._foreground,
                "style": self.style,
            }

            if "Outline" in self.style:
                self._foreground = self._foreground or self.themed_color
                StylerTTK.style_outline_button(**options)

            elif "Link" in self.style:
                self._foreground = self._foreground or self.themed_color
                StylerTTK.style_link_button(**options)

            else:
                self._background = self._background or self.themed_color
                StylerTTK.style_button(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "style": self.style,
            }
            if "Outline" in self.style:
                options["foreground"] = self.themed_color
                StylerTTK.style_outline_button(**options)

            elif "Link" in self.style:
                options["foreground"] = self.themed_color
                StylerTTK.style_link_button(**options)

            else:
                options["background"] = self.themed_color
                StylerTTK.style_button(**options)

    @property
    def text(self):
        """Return the value of the button text"""
        if self.textvariable:
            return self.textvariable.get()
        else:
            return self["text"]

    @text.setter
    def text(self, value):
        """Set the value of the button text"""
        if self.textvariable:
            self.textvariable.set(value=value)
        else:
            self["text"] = value

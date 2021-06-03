"""
    A **ttkbootstrap** styled **Button** widget.

    Created: 2021-05-19
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


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
        bootstyle="default",
        command=None,
        compound=None,
        cursor=None,
        image=None,
        padding=None,
        state="normal",
        takefocus=True,
        text=None,
        textvariable=None,
        underline=None,
        width=None,
        wraplength=None,
        style=None,
        
        # custom style options
        anchor=None,
        background=None,
        foreground=None,
        font=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that control the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available. COLOR KEYWORDS: `primary`, `secondary`, `success`, `info`, `warning`, `danger`. BUTTON TYPES: `outline`, `link`.
            command (func): A function that is called when the button is pushed.
            compound (str): Controls the position of the text and image when both are displayed. Legal values include: `none`, `bottom`, `top`, `left`, `right`, `center`.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            image (PhotoImage): An image to display on the button. The position of the image is controlled by the ``compound`` option.
            padding (str): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            state (str): Either 'normal' or 'disabled'. A disabled state will prevent user input.
            takefocus (bool): Adds or removes the widget from focus traversal.
            textvariable (Variable): A tkinter variable whose value is used in place of the button text.
            underline (int): The index of the character to underline.
            width (int): The absolute width of the text area; avg character size if text or pixels if an image.
            wraplength (int): The maximum line length in pixels.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            anchor (str): Controls how the text or image is positioned relative to the inner margins. Legal values include: `n`, `ne`, `e`, `se`, `s`, `sw`, `w`, `nw`, and `center`.
            background (str): The button background color; setting this options will override theme settings.
            foreground (str): The button text color; setting this option will override theme settings.
            font (str): The font used to draw text inside the widget; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TButton", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.anchor = anchor
        self.background = background
        self.font = font
        self.foreground = foreground
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Button.__init__(
            self,
            master=master,
            command=command,
            compound=compound,
            cursor=cursor,
            image=image,
            padding=padding,
            state=state,
            style=self.style,
            takefocus=takefocus,
            text=text,
            textvariable=textvariable,
            underline=underline,
            width=width,
            wraplength=wraplength,
            **kw,
        )

    def _customize_widget(self):

        if any([self.background != None, self.foreground != None, self.anchor != None, self.font != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "anchor": self.anchor,
                "background": self.background,
                "foreground": self.foreground,
                "font": self.font,
                "style": self.style,
            }

            if "Outline" in self.style:
                self.foreground = self.foreground or self.themed_color
                settings = StylerTTK.style_outline_button(**options)
            elif "Link" in self.style:
                self.foreground = self.foreground or self.themed_color
                settings = StylerTTK.style_link_button(**options)
            else:
                self.background = self.background or self.themed_color
                settings = StylerTTK.style_button(**options)

            self.update_ttk_style(settings)

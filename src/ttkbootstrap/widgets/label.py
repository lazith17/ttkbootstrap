"""
    A **ttkbootstrap** styled **Label** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Label(Widget, ttk.Label):
    """A Label widget displays a textual label and/or image. The label may be linked to a variable to automatically
    change the displayed text."""

    def __init__(
        self,
        
        # widget options
        master=None,
        anchor=None,
        bootstyle="default",
        compound=None,
        cursor=None,
        font=None,
        image=None,
        justify=None,
        padding=None,
        state="normal",
        takefocus=False,
        text=None,
        textvariable=None,
        underline=None,
        width=None,
        wraplength=None,
        style=None,

        # custom style options
        background=None,
        foreground=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            anchor (str): Controls how the text or image is positioned relative to the inner margins. Legal values include: `n`, `ne`, `e`, `se`, `s`, `sw`, `w`, `nw`, and `center`.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            compound (str): Controls the position of the text and image when both are displayed. Legal values include: `none`, `bottom`, `top`, `left`, `right`, `center`.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            image (PhotoImage): An image to display on the label. The position of the image is controlled by the ``compound`` option.
            font (str): The font used to draw text inside the label; setting this option will override theme settings.
            justify (str): Aligns text within the widget. Legal values include: `left`, `center`, `right`.
            padding (Any): Sets the internal label padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            state (str): May be set to `normal` or `disabled`. If disabled, the user cannot change the content.
            takefocus (bool): Adds or removes the widget from focus traversal.
            text (str): Specifies a text string to be displayed inside label (unless overridden by ``textvariable``).
            textvariable (Variable): A tkinter variable whose value is used in place of the label text.
            underline (int): The index of the character to underline.
            width (int): The absolute width of the text area; avg character size if text or pixels if an image.
            wraplength (int): The maximum line length in pixels.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The label background color; setting this option will override theme settings.
            foreground (str, optional): The label text color; setting this option will override the theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TLabel", master=master, bootstyle=bootstyle, style=style)

        self.textvariable = textvariable
        self._background = background
        self._foreground = foreground
        self._bsoptions = ['background', 'foreground', 'bootstyle']
        self._customize_widget()

        ttk.Label.__init__(
            self,
            master=master,
            anchor=anchor,
            compound=compound,
            cursor=cursor,
            font=font,
            image=image,
            justify=justify,
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

    def _customize_widget(self):

        if any([self._background != None, self._foreground != None]):
            self.customized = True

            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self._background,
                "foreground": self._foreground,
                "style": self.style,
            }

            if "Inverse" in self.style:
                options["background"] = self._background or self.themed_color
            else:
                options["foreground"] = self._foreground or self.themed_color
            settings = StylerTTK.style_label(**options)
            self.update_ttk_style(settings)

    @property
    def text(self):
        if self.textvariable:
            return self.textvariable.get()
        else:
            return self['text']

    @text.setter
    def text(self, value):
        if self.textvariable:
            self.textvariable.set(value)
        else:
            self['text'] = value


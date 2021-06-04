"""
    A **ttkbootstrap** styled **Menubutton** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com


"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget



class Menubutton(Widget, ttk.Menubutton):
    """A Menubutton widget displays a textual label and/or image, and displays a menu when pressed.
    """

    def __init__(
        self,

        # widget options
        master=None,
        bootstyle="default",
        compound=None,
        cursor=None,
        direction=None,
        font=None,
        image=None,
        menu=None,
        padding=None,
        showarrow=True,
        state="normal",
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

        self.tk = master.tk
        self.arrowsize = 0 if showarrow else 4
        self.background = background
        self.font = font
        self.foreground = foreground
        self.widget_id = None

        self.customized = False
        self._customize_widget()

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
            textvariable=textvariable or Variable(),
            underline=underline,
            width=width,
            **kw,
        )

    def _customize_widget(self):

        if any([self.background != None, self.foreground != None, self.font != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background,
                "foreground": self.foreground,
                "font": self.font,
                "style": self.style,
            }

            if "Outline" in self.style:
                self.foreground = self.foreground or self.themed_color
                settings = StylerTTK.style_outline_menubutton(**options)
            else:
                self.background = self.background or self.themed_color
                settings = StylerTTK.style_menubutton(**options)

            self.update_ttk_style(settings)

    @property
    def value(self):
        """Get the current value selected"""
        return self.textvariable.get()

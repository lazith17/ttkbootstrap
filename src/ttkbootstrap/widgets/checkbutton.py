"""
    A **ttkbootstrap** styled **Checkbutton** widget.

    Created: 2021-05-23
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Checkbutton(Widget, ttk.Checkbutton):
    """A Checkbutton widget is used to show or change a setting. It has two states, selected and deselected. The state
    of the checkbutton may be linked to a tkinter variable.
    """

    def __init__(
        self,
        
        # widget options
        master=None,
        bootstyle="default",
        command=None,
        compound=None,
        cursor=None,
        default=False,
        image=None,
        offvalue=0,
        onvalue=1,
        padding=None,
        state="normal",
        takefocus=True,
        textvariable=None,
        text=None,
        underline=None,
        variable=None,
        width=None,
        style=None,

        # custom style options
        background=None,
        foreground=None,
        font=None,
        indicatorcolor=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that control the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            command (func): A function that is called when the checkbutton is invoked.
            compound (str): Controls the position of the text and image when both are displayed. Legal values include: `none`, `bottom`, `top`, `left`, `right`, `center`.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.  
            default (bool): Sets the initial widget value to ``True`` or ``False``, which corresponds to ``selected`` or ``deselected``.
            image (PhotoImage): An image to display on the checkbutton. The position of the image is controlled by the ``compound`` option.            
            offvalue (Any): The value of the checkbutton when in the (unchecked) state. Default is 0.
            onvalue (Any): The value of the checkbutton when in the (checked) state. Default is 1.
            padding (str): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.            
            state (str): Either 'normal' or 'disabled'. A disabled state will prevent user input.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            takefocus (bool): Adds or removes the checkbutton from focus traversal.
            text (str): The text to display in the checkbutton label.
            textvariable (Variable): A tkinter variable whose value is used in place of the checkbutton label text.
            underline (int): The index of the character to underline in the checkbutton label.
            variable (Variable): A tkinter variable whose value is used to control the checkbutton value. If none is provided, it is generated automatically and can be accessed directly or via the ``value`` property.
            width (int): The absolute width of the text area; avg character size if text or pixels if an image.
            background (str): The checkbutton background color; setting this option will override the theme settings.
            foreground (str): The checkbutton text color; setting this option will override theme settings.
            font (str): The font used to draw text inside the widget; setting this option will override theme settings.
            indicatorcolor (str): The color of the checkbutton indicator; setting this option will override the theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TCheckbutton", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.font = font
        self.foreground = foreground
        self.indicatorcolor = indicatorcolor
        self.widget_id = None
        self.variable = variable or Variable(value=onvalue if default else offvalue)

        self.customized = False
        self._customize_widget()

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

    def _customize_widget(self):

        if any([self.background != None, self.foreground != None, self.font != None, self.indicatorcolor != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background,
                "foreground": self.foreground,
                "indicatorcolor": self.indicatorcolor,
                "font": self.font or DEFAULT_FONT,
                "style": self.style,
            }

            if "Roundtoggle" in self.style:
                settings = StylerTTK.style_roundtoggle(**options)
            elif "Squaretoggle" in self.style:
                settings = StylerTTK.style_squaretoggle(**options)                
            elif "Outline.Toolbutton" in self.style:
                options.pop('foreground')
                settings = StylerTTK.style_outline_toolbutton(**options)                
            elif "Toolbutton" in self.style:
                options.pop('background')
                settings = StylerTTK.style_toolbutton(**options)                
            else:
                settings = StylerTTK.style_checkbutton(**options)

            self.update_ttk_style(settings)

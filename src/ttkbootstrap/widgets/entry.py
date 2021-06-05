"""
    A **ttkbootstrap** styled **Entry** widget.

    Created: 2021-05-27
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import Variable, ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Entry(Widget, ttk.Entry):
    """The Entry widget displays a one-line text string and allows that string to be edited by the user. The value of
    the string may be linked to a variable with the textvariable option. Entry widgets support horizontal scrolling
    with the standard xscrollcommand option and xview widget command."""

    def __init__(
        self,
        
        # widget options
        master=None,
        bootstyle="default",
        cursor=None,
        exportselection=False,
        font=None,
        invalidcommand=None,
        justify=None,
        padding=None,
        show=None,
        state="normal",
        takefocus=True,
        text=None,
        textvariable=None,
        validate=None,
        validatecommand=None,
        width=None,
        xscrollcommand=None,
        style=None,

        # style options
        background=None,
        focuscolor=None,
        foreground=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            exportselection (bool): If set, the widget selection is linked to the X selection.
            font (str): The font used to draw text inside the widget; setting this option will override theme settings.
            font (str): The font used to render the widget text.
            invalidcommand (func): A function to evaluate whenever the ``validatecommand`` returns 0.
            justify (str): Aligns text within the widget. Legal values include: `left`, `center`, `right`.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            show (str): A character to use as a mask; such as "*" for passwords.
            state (str): Either `normal`, `disabled`, or `readonly`. A disabled state will prevent user input; in the readonly state, the value may not be edited directly.
            takefocus (bool): Adds or removes the widget from focus traversal.
            text (str): The initial value of the entry text.
            textvariable (Variable): A tkinter variable whose value is linked to the widget value.
            validate (str): The validation mode. Legal values include: `none`, `focus`, `focusin`, `focusout`, `key`, or `all`; Default is `none`.
            validatecommand (func): A function to evaluate whenever validation is triggered.
            width (int): The absolute width of the text area using the average character size of the widget font.
            xscrollcommmand (func): A reference to ``xscrollbar.set`` method of another widget; used to communicate with horizontal scrollbars.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The entry field background color; setting this options will override theme settings.
            focuscolor (str): The color of the focus ring when the widget has focus; setting this option will override theme settings.
            foreground (str): The entry text color; setting this option will override theme settings.
        
        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TEntry", master=master, bootstyle=bootstyle, style=style)

        self.background = background
        self.focuscolor = focuscolor
        self.foreground = foreground
        self.font = font or DEFAULT_FONT
        self.textvariable = textvariable or Variable(value=text)
        self._customize_widget()

        ttk.Entry.__init__(
            self,
            master=master,
            cursor=cursor,
            exportselection=exportselection,
            font=font,
            invalidcommand=invalidcommand,
            justify=justify,
            padding=padding,
            show=show,
            state=state,
            style=self.style,
            takefocus=takefocus,
            textvariable=self.textvariable,
            validate=validate,
            validatecommand=validatecommand,
            width=width,
            xscrollcommand=xscrollcommand,
            **kw,
        )

    def _customize_widget(self):

        if any([self.background != None, self.foreground != None, self.focuscolor != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background,
                "foreground": self.foreground,
                "focuscolor": self.focuscolor or self.themed_color,
                "style": self.style,
            }
            settings = StylerTTK.style_entry(**options)

            self.update_ttk_style(settings)

    @property
    def text(self):
        """Return the entry text"""
        return self.textvariable.get()

    @text.setter
    def text(self, value):
        """Set the value of the text"""
        self.textvariable.set(value=value)

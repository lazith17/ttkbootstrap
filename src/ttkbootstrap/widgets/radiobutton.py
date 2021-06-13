"""
    A **ttkbootstrap** styled **Radiobutton** widget.

    Created: 2021-05-24
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.themes import DEFAULT_FONT
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.widgets import Widget
from ttkbootstrap.constants import *


class Radiobutton(Widget, ttk.Radiobutton):
    """A Radiobutton widget is used in groups to show or change a set of mutually-exclusive options. Radiobuttons are
    linked to a variable and have an associated value; when a radiobutton is clicked, it sets the variable to its
    associated value.
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
        group=None,
        image=None,
        padding=None,
        state=NORMAL,
        takefocus=True,
        text=None,
        textvariable=None,
        underline=None,
        variable=None,
        value=None,
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
            command (func): A function that is called when the radiobutton is invoked.
            compound (str): Controls the position of the text and image when both are displayed. Legal values include: `none`, `bottom`, `top`, `left`, `right`, `center`.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            default (bool): Sets the value of this element as the default selected widget in the group.
            group (str): Specifies the name of the radiobutton group. This name will be assigned to an internal tkinter variable that is bound to each radiobutton in the group. This group name will be ignored if a variable is assigned to the ``variable`` option. If no variable is assigned and no group is provided, one will be generated automatically. If placed in a group, each Radiobutton must be given a value with the ``value`` option.
            image (PhotoImage): An image to display on the radiobutton. The position of the image is controlled by the ``compound`` option.
            value (Any): The value to store in the associated variable when the widget is selected.
            padding (str): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            state (str): Either `normal` or `disabled`. A disabled state will prevent user input.
            takefocus (bool): Adds or removes the radiobutton from focus traversal.
            text (str): The text to display in the radiobutton label.
            textvariable (Variable): A tkinter variable whose value is used in place of the radiobutton label text.
            underline (int): The index of the character to underline in the radiobutton label.
            variable (Variable): A variable that tracks the current state of the radiobutton. If a variable is not provided, one is created automatically and can be changed or retrieved via the ``value`` property. If a ``groupname`` is provided, then this variable will be assigned as the control variable for the entire button group.
            width (int): The absolute width of the text area; avg character size if text or pixels if an image.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The radiobutton background color; setting this option will override the theme settings.
            foreground (str): The radiobutton text color; setting this option will override theme settings.
            font (str): The font used to draw text inside the widget; setting this option will override theme settings.
            indicatorcolor (str): The color of the radiobutton indicator; setting this option will override the theme settings.


        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TRadiobutton", master=master, bootstyle=bootstyle, style=style)

        self.variable = variable
        self._background = background
        self._default = default
        self._font = font
        self._foreground = foreground
        self._group = group
        self._indicatorcolor = indicatorcolor
        self._bsoptions = ["background", "font", "foreground", "indicatorcolor", "bootstyle"]
        self._set_variable(value)
        self._customize_widget()

        ttk.Radiobutton.__init__(
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
            variable=self.variable,
            value=value or 1,
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

    def _set_variable(self, value=1):
        """Create a group variable if not existing; and set default value if requested.

        Args:
            value (Any): The default value of the widget when selected (Default is 1).
        """
        if self.variable:
            self._group = self.variable._name
        else:
            if self._group:
                self.variable = Variable(name=self._group)
            else:
                self.variable = Variable()
                self._group = self.variable._name
        if self._default:
            self.value = value

    def _customize_widget(self):

        if not self.theme:
            # not a ttkbootstrap theme; use ttk styling.
            return

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

            if "Outline.Toolbutton" in self.style:
                options.pop("foreground")
                StylerTTK.style_outline_toolbutton(**options)
            elif "Toolbutton" in self.style:
                options.pop("background")
                StylerTTK.style_toolbutton(**options)
            else:
                options.pop("background")
                StylerTTK.style_radiobutton(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "indicatorcolor": self.themed_color,
                "style": self.style,
            }

            if "Outline.Toolbutton" in self.style:
                StylerTTK.style_outline_toolbutton(**options)
            elif "Toolbutton" in self.style:
                StylerTTK.style_toolbutton(**options)
            else:
                StylerTTK.style_radiobutton(**options)

        self.update_ttk_style(self.settings)

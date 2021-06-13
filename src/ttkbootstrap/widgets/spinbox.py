"""
    A **ttkbootstrap** styled **Spinbox** widget.

    Created: 2021-05-30
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from numbers import Number
from tkinter import ttk
from tkinter import StringVar
from ttkbootstrap.themes import DEFAULT_FONT
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.widgets import Widget
from ttkbootstrap.constants import *


class Spinbox(Widget, ttk.Spinbox):
    """A Spinbox widget is an Entry widget with built-in up and down buttons that are used to either modify a numeric
    value or to select among a set of values. The widget implements all the features of the Entry widget including
    support of the textvariable option to link the value displayed by the widget to a tkinter variable."""

    def __init__(
        self,
        # widget options
        master=None,
        bootstyle=DEFAULT,
        command=None,
        cursor=None,
        defaultvalue=None,
        defaultindex=None,
        font=None,
        format="%0.0f",
        from_=0,
        increment=1,
        padding=None,
        state=NORMAL,
        style=None,
        takefocus=True,
        textvariable=None,
        to=100,
        validate=None,
        validatecommand=None,
        values=None,
        wrap=False,
        xscrollcommand=None,
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
            command (func): A function that is called whenever a spinbutton is pressed.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            defaultvalue (Any): The initial value shown in the spinbox.
            defaultindex (int): The index of the item to show by default if a list of values is provided.
            font (str or Font): The font used to render the widget text.
            format (str): Specifies an alternate format to use when setting the string value when using the ``from`` and ``to`` range. This must be a format specifier of the form %<pad>.<pad>f, as it will format a floating-point number.
            from_ (float): A floating-point value specifying the lowest value for the spinbox. This is used in conjunction with ``to`` and ``increment`` to set a numerical range. Default is `0.0`.
            increment (float): The amount of change to add or subtract between the ``from_`` and ``to`` values.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            state (str): Either `normal`, `disabled`, or `readonly`. A disabled state will prevent user input; in the readonly state, the value may not be edited directly.
            takefocus (bool): Adds or removes the widget from focus traversal.
            textvariable (Variable): A tkinter variable whose value is linked to the widget value.
            validate (str): The validation mode. Legal values include: `none`, `focus`, `focusin`, `focusout`, `key`, or `all`; Default is `none`.
            validatecommand (func): A function to evaluate whenever validation is triggered.
            values (List or Tuple): The values to use in the spinbox. This will override any range set using the ``from``, ``to`` and ``increment`` options.
            wrap (bool): Cycle through the values of the spinbox when reaching the end of the range instead of stopping at the min or max value.
            xscrollcommmand (func): A reference to ``xscrollbar.set`` method; used to communicate with horizontal scrollbars.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The field background color; setting this options will override theme settings.
            focuscolor (str): The color of the focus ring when the widget has focus; setting this option will override theme settings.
            foreground (str): The spinbox text color; setting this option will override theme settings.


        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TSpinbox", master=master, bootstyle=bootstyle, style=style)

        self.textvariable = textvariable or StringVar()
        self._background = background
        self._focuscolor = focuscolor
        self._foreground = foreground
        self._font = font or DEFAULT_FONT
        self._format = format
        self._from = from_
        self._to = to
        self._defaultvalue = defaultvalue
        self._defaultindex = defaultindex
        self._values = values
        self._bsoptions = ["background", "focuscolor", "foreground", "bootstyle"]
        self._set_variable()
        self.register_style()

        ttk.Spinbox.__init__(
            self,
            master=master,
            command=command,
            cursor=cursor,
            font=font,
            format=format,
            from_=from_,
            increment=increment,
            padding=padding,
            state=state,
            style=self.style,
            takefocus=takefocus,
            textvariable=self.textvariable,
            to=to,
            validate=validate,
            validatecommand=validatecommand,
            values=values,
            wrap=wrap,
            xscrollcommand=xscrollcommand,
            **kw,
        )

    def style_widget(self):

        # custom styles
        if any([self._background != None, self._foreground != None, self._focuscolor != None]):
            self.customized = True
            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

            options = {
                "theme": self.theme,
                "settings": self.settings,
                "background": self._background,
                "foreground": self._foreground,
                "focuscolor": self._focuscolor or self.themed_color,
                "style": self.style,
            }
            StylerTTK.style_spinbox(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "focuscolor": self.themed_color,
                "style": self.style,
            }
            StylerTTK.style_spinbox(**options)

    def _set_variable(self):
        """Set initial variable value upon instantiation"""
        if self._defaultvalue:
            self.value = (
                self._format % self._defaultvalue if isinstance(self._defaultvalue, Number) else self._defaultvalue
            )
            return
        if self._values and self._defaultindex is not None:
            # override to ensure that the index is a valid
            item_index = min(max(self._defaultindex, len(self._values) - 1), 0)
            if isinstance(self._values[item_index], Number):
                self.value = self._format % self._values[item_index]
            else:
                self.value = self._values[item_index]

    @property
    def value(self):
        """Get the current value of the spinbox widget. Alias for ``Spinbox.get``"""
        return self.textvariable.get()

    @value.setter
    def value(self, value):
        """Set the current value of the spinbox widget. Alias for ``Spinbox.set``"""
        self.textvariable.set(value)

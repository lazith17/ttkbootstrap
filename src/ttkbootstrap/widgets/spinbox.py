"""
    A **ttkbootstrap** styled **Spinbox** widget.

    Created: 2021-05-30
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import ttk
from tkinter import StringVar
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Spinbox(Widget, ttk.Spinbox):
    """A Spinbox widget is a ttk.Entry widget with built-in up and down buttons that are used to either modify a
    numeric value or to select among a set of values. The widget implements all the features of the ttk.Entry widget
    including support of the textvariable option to link the value displayed by the widget to a tkinter variable."""

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        command=None,
        cursor=None,
        defaultvalue=None,
        focuscolor=None,
        font=None,
        foreground=None,
        format=None,
        from_=0.0,
        increment=1.0,
        padding=None,
        state="normal",
        style=None,
        takefocus=True,
        textvariable=None,
        to=100.0,
        validate=None,
        validatecommand=None,
        values=None,
        wrap=None,
        xscrollcommand=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            background (str, optional): The normal background color to use for the Spinbox. Setting this option will
                override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            command (func, optional): Specifies a command to be invoked whenever a spinbutton is invoked.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            defaultvalue (Any, optional): The initial value shown in the spinbox.
            focuscolor (str, optional): The color of the focus ring when the widget has focus.
            font (str or Font, optional): The font used to render the widget text.
            foreground (str, optional): The color of the text inside the Spinbox widget. Setting this option will
                override all other style-based foreground setting.
            format (str, optional): Specifies an alternate format to use when setting the string value when using the 
                ``from`` and ``to`` range. This must be a format specifier of the form %<pad>.<pad>f, as it will format
                a floating-point number.
            from_ (float, optional): A floating-point value specifying the lowest value for the spinbox. This is used in
                conjunction with ``to`` and ``increment`` to set a numerical range. Default is `0.0`.
            increment (float, optional): A floating-point value specifying the change in value to be applied each time
                one of the widget spin buttons is pressed. The up button applies a positive increment, the down button
                applies a negative increment. Default is `1.0`.
            padding (Any, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            state (str, optional): One of `normal`, `readonly`, or `disabled`. In the readonly state, the value may not
                be edited directly, and the user can only select one of the -values from the dropdown list. In the
                normal state, the text field is directly editable. In the disabled state, no interaction is possible.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            textvariable (Variable, optional): Specifies the name of a variable whose value is linked to the spinbox
                widget's selected value. Whenever the variable changes value, the widget's contents are updated, and
                vice versa. This variable is accessible directly and via the ``value`` property.
            validate (str, optional): Specifies the mode in which validation should operate: none, focus, focusin,
                focusout, key, or all. Default is none, meaning that validation is disabled.
            validatecommand (func, optional): A script template to evaluate whenever validation is triggered. If set to
                the empty string (the default), validation is disabled. The script must return a boolean value.
            values (List or Tuple, optional): This must be a List or Tuple of values. If this option is set then this
                will override any range set using the ``from``, ``to`` and ``increment`` options. The widget will
                instead use the values specified beginning with the first value.
            wrap (bool, optional): Must be a proper boolean value. If on, the spinbox will wrap around the values of
                data in the widget.
            xscrollcommmand (func, optional): A command prefix, used to communicate with horizontal scrollbars. When
                the view in the widget's window changes, the widget will generate a command by concatenating the
                scroll command and two numbers. Each of the numbers is a fraction between 0 and 1 indicating a
                position in the document; 0 indicates the beginning, and 1 indicates the end. The first fraction
                indicates the first information in the widget that is visible in the window, and the second fraction
                indicates the information just after the last portion that is visible. If this option is set to the
                empty string (the default), then no command will be executed.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TSpinbox", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.focuscolor = focuscolor
        self.foreground = foreground
        self.font = font or DEFAULT_FONT
        self.from_ = from_
        self.to = to
        self.defaultvalue = defaultvalue
        self.values = values
        self.textvariable = textvariable or StringVar()
        self.widget_id = None

        self.customized = False
        self._set_variable()
        self._customize_widget()

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
            settings = StylerTTK.style_spinbox(**options)

            self.update_ttk_style(settings)

    def _set_variable(self):
        """Set initial variable value upon instantiation"""
        if self.values and not self.defaultvalue:
            self.value = self.values[0]
        elif self.defaultvalue:
            self.value = self.defaultvalue
        else:
            self.value = self.from_

    @property
    def value(self):
        """Get the current value of the spinbox widget"""
        return self.textvariable.get()

    @value.setter
    def value(self, value):
        """Set the current value of the spinbox widget"""
        self.textvariable.set(value)

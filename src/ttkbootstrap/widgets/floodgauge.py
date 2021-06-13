"""
    A **ttkbootstrap** styled **Floodgauge** widget.

    Created: 2021-06-09
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable, DoubleVar, IntVar
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.widgets import Widget

DEFAULT_FONT = "helvetica 24 bold"
DEFAULT_THICKNESS = 100


class Floodgauge(Widget, ttk.Progressbar, ttk.Label):
    """A ``Floodgauge`` is a dashboard style gauge that has a similar API as the ``Progressbar`` except with text
    options. This widget can operate in two modes: **determinate** mode shows the amount completed relative to the
    total amount of work to be done, and **indeterminate** mode provides an animated display to let the user know
    that something is happening.

    Optionally, you can turn on the ``showvalue`` option to show the Floodgauge value,though this will override the
    text label option.
    """

    def __init__(
        self,
        # widget options
        master=None,
        bootstyle="default",
        cursor=None,
        maximum=100,
        mode="determinate",
        orient="horizontal",
        phase=None,
        showvalue=False,
        size=(200, 200),
        takefocus=False,
        text=None,
        textappend=None,
        textprepend=None,
        textvariable=None,
        value=0,
        valuetype="int",
        variable=None,
        style=None,
        # custom style options
        barcolor=None,
        font=None,
        foreground=None,
        troughcolor=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            maximum (int): A floating point number specifying the maximum ``value``. Defaults to 100.
            mode (str): One of `determinate` or `indeterminate`.
            orient (str): One of 'horizontal' or 'vertical'.  Specifies the orientation of the Progressbar.
            phase (str): Read-only option. The widget periodically increments the value of this option whenever the ``value`` is greater than 0 and, in determinate mode, less than ``maximum``. This option may be used by the current theme to provide additional animation effects.
            takefocus (bool): Adds or removes the widget from focus traversal.
            text (str): A string of text to be displayed in the progress bar. This is assigned to the ``textvariable``. This value can be accessed via the ``text`` property.
            textappend (str): A string to append to the end of the ``text`` option. Some common examples includes `mph`, `deg`, etc...
            textprepend (str): A string to insert at the beginning of the ``text`` option.
            textvariable (Variable): A tkinter variable which controls the text displayed inside the progressbar. This is generated automatically if not provided.
            value (float): The current value of the progress bar. Can also be accessed via the ``value`` property.
            valuetype (str): The data type to use for the progressbar. Options include `int` or `float`. Default is `int`.
            variable (Variable): A variable which is linked to the ``value``. If associated to an existing variable, the ``value`` of the progress bar is automatically set to the value of the variable whenever the latter is modified. If not provided, one is created by default.
            showvalue (bool): If true, the value text will be displayed on the widget. This will override the text option.
            size (Tuple[int, int]): The width and height of the widget. This option will be overridden by geometry manager options that allow the widget to expand or contract.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            barcolor (str): The color of the progressbar; setting this option will override theme settings.
            foreground (str): The color of the widget text.
            troughcolor (str): The color of the trough; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(
            self, "TFloodgauge", class_="Floodgauge", master=master, bootstyle=bootstyle, orient=orient, style=style
        )

        self.textvariable = textvariable or Variable(value=f"{textprepend or ''}{text or ''}{textappend or ''}")
        self.variable = variable or IntVar(value=value) if valuetype == "int" else DoubleVar(value=value)
        self._textappend = textappend or ""
        self._textprepend = textprepend or ""
        self._showvalue = showvalue

        self._font = font or DEFAULT_FONT
        self._foreground = foreground
        self._orient = orient
        self._barcolor = barcolor or self.themed_color
        self._length = size[0] if orient == "horizontal" else size[1]
        self._thickness = size[1] if orient == "vertical" else size[0]
        self._troughcolor = troughcolor
        self._bsoptions = ["barcolor", "troughcolor", "foreground", "font", "bootstyle"]
        self.register_style()

        ttk.Progressbar.__init__(
            self,
            master=master,
            cursor=cursor,
            length=self._length,
            maximum=maximum,
            mode=mode,
            orient=orient,
            phase=phase,
            variable=self.variable,
            style=self.style,
            takefocus=takefocus,
            **kw,
        )
        self.tk.call("ttk::style", "configure", self.style, "-%s" % "text", self.text, None)
        self.variable.trace_add("write", self._textvariable_write)
        self._textvariable_write()

    @property
    def text(self):
        """Get the widget text"""
        return self.textvariable.get()

    @text.setter
    def text(self, value):
        """Set the widget text"""
        self.textvariable.set(value)

    @property
    def value(self):
        """Get the current value of the widget"""
        return self.variable.get()

    @value.setter
    def value(self, value):
        """Set the current value of the widget"""
        self.variable.set(value)

    def style_widget(self):

        # custom styles
        if any(
            [
                self._barcolor != None,
                self._troughcolor != None,
                self._foreground != None,
                self._font != DEFAULT_FONT,
                self._thickness != DEFAULT_THICKNESS,
            ]
        ):
            self.customized = True
            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

            options = {
                "theme": self.theme,
                "settings": self.settings,
                "barcolor": self._barcolor or self.themed_color,
                "troughcolor": self._troughcolor,
                "font": self._font,
                "foreground": self._foreground,
                "thickness": self._thickness,
                "orient": self._orient,
                "style": self.style,
            }
            StylerTTK.style_floodgauge(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "barcolor": self.themed_color,
                "orient": self._orient,
                "style": self.style,
            }
            StylerTTK.style_floodgauge(**options)

    def _textvariable_write(self, *args):
        """Callback to update the label text when there is a `write` action on the variable

        Args:
            *args: if triggered by a trace, will be `variable`, `index`, `mode`.
        """
        if self._showvalue:
            label = f"{self._textprepend}{self.value}{self._textappend}"
            self.tk.call("ttk::style", "configure", self.style, "-%s" % "text", label, None)

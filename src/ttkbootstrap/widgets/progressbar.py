"""
    A **ttkbootstrap** styled **Progressbar** widget.

    Created: 2021-06-03
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Progressbar(Widget, ttk.Progressbar):
    """A Progressbar widget shows the status of a long-running operation. They can operate in two modes: determinate
    mode shows the amount completed relative to the total amount of work to be done, and indeterminate mode provides
    an animated display to let the user know that something is happening."""

    def __init__(
        self,
        master=None,
        bootstyle="default",
        cursor=None,
        length=None,
        maximum=100,
        mode="determinate",
        orient="horizontal",
        phase=None,
        value=0,
        variable=None,
        style=None,
        takefocus=False,
        barcolor=None,
        troughcolor=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            barcolor (str): The color of the progressbar. Setting this value will override any bootstrap styles for
                barcolor.
            bootstyle (str): The **ttkbootstrap** style used to render the widget. This is a short-hand API for setting
                the widget style. You may also use the ``style`` option directly using the standard ``ttk`` API. Using
                the ``Style`` option will overwrite the ``bootstyle``.
            cursor (str): Specifies the `mouse cursor`_ to be used for the widget. Names and values will vary according
                to your operating system.
            length (int): Specifies the length of the long axis of the progress bar.
            maximum (int): A floating point number specifying the maximum ``value``. Defaults to 100.
            orient (str): One of 'horizontal' or 'vertical'.  Specifies the orientation of the Progressbar.
            slidercolor (str): The color of the round slider; setting this will override the ``bootstyle`` settings.
            style (str): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool): Determines whether the widget accepts the focus during keyboard traversal (e.g., Tab and
                Shift-Tab).
            troughcolor (str): The color of the trough. Using this will override ``bootstyle`` settings.
            value (float): The current value of the progress bar. In determinate mode, this represents the amount of
                work completed. In indeterminate mode, it is interpreted modulo ``maximum``; that is, the progress bar
                completes one “cycle” when the ``value`` increases by ``maximum``. If ``variable`` is set to an
                existing variable, specifying ``value`` has no effect (the variable value takes precedence).
            variable (Variable): A variable which is linked to the ``value``. If specified to an existing variable, the
                ``value`` of the progress bar is automatically set to the value of the variable whenever the latter is
                modified. If not provided, one is created by default.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TProgressbar", master=master, bootstyle=bootstyle, orient=orient, style=style)

        self.tk = master.tk
        self.orient = orient
        self.widget_id = None
        self.variable = Variable(value=value) or variable
        self.barcolor = barcolor
        self.troughcolor = troughcolor

        self.customized = False
        self._customize_widget()

        ttk.Progressbar.__init__(
            self,
            master=master,
            cursor=cursor,
            length=length,
            maximum=maximum,
            mode=mode,
            orient=orient,
            phase=phase,
            variable=self.variable,
            style=self.style,
            takefocus=takefocus,
            **kw,
        )

    @property
    def value(self):
        """Get the current value of the widget"""
        return self.variable.get()

    @value.setter
    def value(self, value):
        """Set the current value of the widget"""
        self.variable.set(value)

    def _customize_widget(self):

        if any([self.barcolor != None, self.troughcolor != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "barcolor": self.barcolor or self.themed_color,
                "troughcolor": self.troughcolor,
                "orient": self.orient,
                "style": self.style,
            }
            settings = StylerTTK.style_progressbar(**options)

            self.update_ttk_style(settings)

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

        # widget options
        master=None,
        bootstyle="default",
        cursor=None,
        length=None,
        maximum=100,
        mode="determinate",
        orient="horizontal",
        phase=None,
        takefocus=False,
        value=0,
        variable=None,
        style=None,

        # custom style options
        barcolor=None,
        troughcolor=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.            
            length (int): The length of the long axis of the progress bar in pixels.
            maximum (int): A floating point number specifying the maximum ``value``. Defaults to 100.
            mode (str): One of `determinate` or `indeterminate`.
            orient (str): One of 'horizontal' or 'vertical'.  Specifies the orientation of the Progressbar.
            phase (str): Read-only option. The widget periodically increments the value of this option whenever the ``value`` is greater than 0 and, in determinate mode, less than ``maximum``. This option may be used by the current theme to provide additional animation effects. 
            takefocus (bool): Adds or removes the widget from focus traversal.
            value (float): The current value of the progress bar.
            variable (Variable): A variable which is linked to the ``value``. If associated to an existing variable, the ``value`` of the progress bar is automatically set to the value of the variable whenever the latter is modified. If not provided, one is created by default.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            barcolor (str): The color of the progressbar; setting this option will override theme settings.
            troughcolor (str): The color of the trough; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TProgressbar", master=master, bootstyle=bootstyle, orient=orient, style=style)

        self.orient = orient
        self.variable = variable or Variable(value=value)
        self.barcolor = barcolor
        self.troughcolor = troughcolor
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

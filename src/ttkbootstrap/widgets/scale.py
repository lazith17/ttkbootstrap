"""
    A **ttkbootstrap** styled **Scale** widget.

    Created: 2021-06-02
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Scale(Widget, ttk.Scale):
    """A Scale widget is typically used to control the numeric value of a linked variable that varies uniformly over 
    some range. A scale displays a slider that can be moved along over a trough, with the relative position of the 
    slider over the trough indicating the value of the variable."""

    def __init__(
        self,
        master=None,
        bootstyle="default",
        command=None,
        cursor=None,
        defaultvalue=0,
        format='%0.2f',
        from_=0,
        length=None,
        orient='horizontal',
        slidercolor=None,
        style=None,
        takefocus=False,
        to=100,
        troughcolor=None,
        value=0,
        variable=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            command (func, optional): Specifies the function to invoke whenever the scale's value is changed.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            defaultvalue (float, optional): The starting value of the widget.
            format (str, optional): A format specifier when returning value from the ``value`` property. To get the
                unformatted number, use the ``.variable.get()`` method. NOT IMPLEMENTED.
            from_ (float, optional): A real value corresponding to the left or top end of the scale. 
            length (int, optional): Specifies the desired long dimension of the scale in screen units.
            orient (str, optional): One of 'horizontal' or 'vertical'.  Specifies the orientation of the Scale.
            slidercolor (str, optional): The color of the round slider; setting this will override the ``bootstyle``
                settings.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the widget accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). 
            to (float, optional):
            troughcolor (str, optional): The color of the trough. Using this will override ``bootstyle`` settings.
            value (float, optional): 
            variable (Variable, optional): Specifies the variable to link to the scale. Whenever the value of the 
                variable changes, the scale will update to reflect this value. Whenever the scale is manipulated 
                interactively, the variable will be modified to reflect the scale's new value. If none is provided, one
                will be created automatically, and can be accessed or set via the ``value`` property.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TScale", master=master, bootstyle=bootstyle, orient=orient, style=style)

        self.tk = master.tk
        self.defaultvalue = defaultvalue or value
        self.format = format
        self.from_ = from_
        self.to_ = to
        self.slidercolor = slidercolor
        self.troughcolor = troughcolor
        self.orient = orient
        self.widget_id = None
        self.variable = Variable(value=self.defaultvalue) or variable

        self.customized = False
        self._customize_widget()

        ttk.Scale.__init__(
            self,
            master=master,
            command=command,
            cursor=cursor,
            from_=from_,
            length=length,
            orient=orient,
            variable=self.variable,
            style=self.style,
            takefocus=takefocus,
            to=to,
            **kw,
        )

    @property
    def value(self):
        """Get the current value of the spinbox widget"""
        return self.format.format(self.textvariable.get())

    @value.setter
    def value(self, value):
        """Set the current value of the spinbox widget"""
        self.textvariable.set(value)

    def _customize_widget(self):

        if any([self.troughcolor != None, self.slidercolor != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "slidercolor": self.slidercolor or self.themed_color,
                "troughcolor": self.troughcolor,
                "orient": self.orient,
                "style": self.style,
            }
            settings = StylerTTK.style_scale(**options)

            self.update_ttk_style(settings)

"""
    A **ttkbootstrap** styled **Combobox** widget.

    Created: 2021-05-27
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Combobox(Widget, ttk.Combobox):
    """A Combobox widget is a combination of an Entry and a drop-down menu. In your application, you will see the usual
    text entry area, with a downward-pointing arrow. When the user clicks on the arrow, a drop-down menu appears. If
    the user clicks on one, that choice replaces the current contents of the entry. However, the user may still type
    text directly into the entry (when it has focus), or edit the current text."""

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        cursor=None,
        defaultvalue=None,
        exportselection=False,
        focuscolor=None,
        font=None,
        foreground=None,
        height=None,
        justify=None,
        padding=None,
        postcommand=None,
        state="normal",
        style=None,
        takefocus=True,
        textvariable=None,
        values=None,
        width=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            background (str, optional): The normal background color to use for the Combobox. Setting this option will
                override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            defaultvalue (Any, optional): The initial value shown in the combobox.
            exportselection (bool, optional): Boolean value. If set, the widget selection is linked to the X selection.
            focuscolor (str, optional): The color of the focus ring when the widget has focus.
            font (str or Font, optional): The font used to render the widget text.
            foreground (str, optional): The color of the text inside the Combobox widget. Setting this option will
                override all other style-based foreground setting.
            height (int, optional): Specifies the height of the pop-down listbox, in rows.
            justify (str, optional): Specifies how the text is aligned within the widget. Must be one of left, center,
                or right.
            padding (Any, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            postcommand (func, optional): A script to evaluate immediately before displaying the listbox. The
                ``postcommand`` script may specify the ``values`` to display.
            state (str, optional): One of `normal`, `readonly`, or `disabled`. In the readonly state, the value may not
                be edited directly, and the user can only select one of the -values from the dropdown list. In the
                normal state, the text field is directly editable. In the disabled state, no interaction is possible.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            textvariable (Variable, optional): Specifies the name of a variable whose value is linked to the widget 
                value. Whenever the variable changes value the widget value is updated, and vice versa. If a variable
                is not provided, one is created by default and can be access via the ``value`` property.
            values (List or Tuple, optional): Specifies the list of values to display in the drop-down listbox. 
            width (int, optional): Specifies an integer value indicating the desired width of the entry window, in 
                average-size characters of the widget's font. 

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TCombobox", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.defaultvalue = defaultvalue
        self.focuscolor = focuscolor
        self.foreground = foreground
        self.font = font or DEFAULT_FONT
        self.textvariable = textvariable or Variable()
        self.values = values
        self.widget_id = None

        self.customized = False

        self._set_variable()
        self._customize_widget()

        ttk.Combobox.__init__(
            self,
            master=master,
            cursor=cursor,
            exportselection=exportselection,
            font=font,
            justify=justify,
            height=height,
            padding=padding,
            postcommand=postcommand,
            state=state,
            style=self.style,
            takefocus=takefocus,
            textvariable=textvariable,
            values=values,
            width=width,
            **kw,
        )
        self.bind("<<ThemeChanged>>", self.on_theme_change)

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
            settings = StylerTTK.style_combobox(**options)

            self.update_ttk_style(settings)

    def _set_variable(self):
        """Set initial variable value upon instantiation"""
        if self.values and not self.defaultvalue:
            self.value = self.values[0]
        elif self.defaultvalue:
            self.value = self.defaultvalue

    @property
    def value(self):
        """Get the current value of the spinbox widget"""
        return self.textvariable.get()

    @value.setter
    def value(self, value):
        """Set the current value of the spinbox widget"""
        self.textvariable.set(value)
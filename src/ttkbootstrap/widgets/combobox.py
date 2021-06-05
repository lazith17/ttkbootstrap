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
        
        # widget options
        master=None,
        bootstyle="default",
        cursor=None,
        default=None,
        exportselection=False,
        font=None,
        height=None,
        justify=None,
        padding=None,
        postcommand=None,
        state="normal",
        takefocus=True,
        textvariable=None,
        values=None,
        width=None,
        style=None,

        # custom style options
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
            default (Any): The initial value shown in the combobox.
            exportselection (bool): If set, the widget selection is linked to the X selection.
            font (str): The font used to draw text inside the widget; setting this option will override theme settings.
            height (int): The height of the combobox in `rows`.
            justify (str): Aligns text within the widget. Legal values include: `left`, `center`, `right`.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            postcommand (func): A function to invoke immediately before displaying the listbox. The ``postcommand`` function may specify the ``values`` to display.
            state (str): Either `normal`, `disabled`, or `readonly`. A disabled state will prevent user input; in the readonly state, the value may not be edited directly.
            takefocus (bool): Adds or removes the widget from focus traversal.
            textvariable (Variable): A tkinter variable whose value is linked to the selected widget value.
            values (List or Tuple): The list of values to display in the drop-down listbox.
            width (int): The absolute width of the text area using the average character size of the widget font.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            background (str): The button background color; setting this options will override theme settings.
            focuscolor (str): The color of the focus ring when the widget has focus; setting this option will override theme settings.
            foreground (str): The entry text color; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TCombobox", master=master, bootstyle=bootstyle, style=style)

        self.background = background
        self.default = default
        self.focuscolor = focuscolor
        self.foreground = foreground
        self.font = font or DEFAULT_FONT
        self.textvariable = textvariable or Variable(value=default)
        self.values = values
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
            textvariable=self.textvariable,
            values=values,
            width=width,
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
            settings = StylerTTK.style_combobox(**options)

            self.update_ttk_style(settings)

    def _set_variable(self):
        """Set initial variable value upon instantiation"""
        if self.values and not self.default:
            self.value = self.values[0]
        elif self.default:
            self.value = self.default

    @property
    def value(self):
        """Get the current value of the spinbox widget"""
        return self.textvariable.get()

    @value.setter
    def value(self, value):
        """Set the current value of the spinbox widget"""
        self.textvariable.set(value)

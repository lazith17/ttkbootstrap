"""
    A **ttkbootstrap** styled **Radiobutton** widget.

    Created: 2021-05-24
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import ttk
from tkinter import TclError
from tkinter import Variable
from ttkbootstrap.core import StylerTTK, Style
from ttkbootstrap.widgets import Widget


class Radiobutton(Widget, ttk.Radiobutton):
    """A Radiobutton widget is used in groups to show or change a set of mutually-exclusive options. Radiobuttons are 
    linked to a variable and have an associated value; when a radiobutton is clicked, it sets the variable to its 
    associated value.
    """

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        command=None,
        compound=None,
        cursor=None,
        default=False,
        font=None,
        foreground=None,
        group=None,
        image=None,
        indicatorcolor=None,
        padding=None,
        state=False,
        style=None,
        takefocus=True,
        text=None,
        textvariable=None,
        underline=None,
        variable=None,
        value=None,
        width=None,
        **kw,
    ):
        """
        Args:
            master (Widget, optional): The parent widget.
            background (str, optional): The normal background color to use when displaying the widget. Setting this
                option will override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            command (func, optional): A callback function to evaluate when the widget is invoked.
            compound (str, optional): Specifies if the widget should display text and bitmaps/images at the same time,
                and if so, where the bitmap/image should be placed relative to the text. Must be one of the values
                **none**, **bottom**, **top**, **left**, **right**, or **center**. For example, the (default) value
                **none** specifies that the bitmap or image should (if defined) be displayed `instead` of the text, the
                value **left** specifies that the bitmap or image should be displayed to the `left` of the text, and
                the value **center** specifies  that the bitmap or image should be displayed `underneath` the text.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            default (bool, optional): Sets the value of this element as the default selected widget in the group.
            font (str, Font, optional): The font to use when drawing text inside the widget.
            foreground (str, optional): The text color. Setting this option will override all other style based 
                foreground settings.
            group (str, optional): Specifies the name of the radiobutton group. This name will be assigned to an 
                internal tkinter variable that is bound to each radiobutton in the group. This group name will be 
                ignored if a variable is assigned to the ``variable`` option. If no variable is assigned and no group 
                is provided, one will be generated automatically. If placed in a group, each Radiobutton must be given 
                a value with the ``value`` option.
            image (PhotoImage, optional): Specifies an image to display in the widget, which must have been created
                with ``tk.PhotoImage`` or `TkPhotoImage`` if using **pillow**. Can also be a string representing the
                name of the photo if the photo has been given a name using the ``name`` parameter.  Typically, if
                the ``image`` option is specified then it overrides other options that specify a bitmap or textual
                value to display in the widget, though this is controlled by the ``compound`` option; the ``image``
                option may be reset to an empty string to re-enable a bitmap or text display.
            indicatorcolor (str, optional): The normal color to use for the widget indicator. Setting this option will
                override all other styled based indicatorcolor options.
            value (Any, optional): The value to store in the associated variable when the widget is selected.
            padding (str, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            state (str, optional): Sets the button to a `normal` or `disabled` state.
            style (str, optional): May be used to specify a custom widget style.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). To remove the widget from focus traversal, use ``takefocus=False``.
            text (str, optional): Specifies a string to be displayed inside the widget.
            textvariable (Variable, optional): Specifies the name or instance of a tkinter variable that can be used in
                place of the ``text`` resource.
            underline (int, optional): Specifies the integer index of a character to underline in the widget. This
                option is used by the default bindings to implement keyboard traversal for menu buttons and menu
                entries. 0 corresponds to the first character of the text displayed in the widget, 1 to the next
                character, and so on.
            variable (Variable, optional): A variable that tracks the current state of the Radiobutton. If a variable 
                is not provided, one is created automatically and can be changed or retrieved via the ``value`` 
                property. If a ``groupname`` is provided, then this variable will be assigned as the control variable
                for the entire button group.
            width (int, optional): If the label is text, this option specifies the absolute width of the text area on
                the button, as a number of characters; the actual width is that number multiplied by the average width
                of a character in the current font. For image labels, this option is ignored. The option may also be
                configured in a style.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TRadiobutton", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.default = default
        self.font = font
        self.foreground = foreground
        self.group = group
        self.indicatorcolor = indicatorcolor
        self.widget_id = None
        self.variable = variable
        self.set_group_variable(value)

        self.customized = False
        self.customize_widget()

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
        self.bind("<<ThemeChanged>>", self.on_theme_change)

    @property
    def value(self):
        """Get the current value specified by the ``onvalue`` or ``offvalue``."""
        return self.variable.get()

    @value.setter
    def value(self, value):
        """Set the current value of the ``variable``"""
        self.variable.set(value)

    def set_group_variable(self, value=1):
        """Create a group variable if not existing; and set default value if requested.
        
        Args:
            value (Any): The default value of the widget when selected (Default is 1).
        """
        if self.variable:
            self.group = self.variable._name
        else:
            if self.group:
                self.variable = Variable(name=self.group)
            else:
                self.variable = Variable()
                self.group = self.variable._name
        if self.default:
            self.value = value

    def customize_widget(self):

        if any([self.background != None, self.foreground != None, self.font != None, self.indicatorcolor != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background,
                "foreground": self.foreground,
                "indicatorcolor": self.indicatorcolor,
                "font": self.font or DEFAULT_FONT,
                "style": self.style,
            }

            if "Outline.Toolbutton" in self.style:
                options.pop('foreground')
                settings = StylerTTK.style_outline_toolbutton(**options)
            elif "Toolbutton" in self.style:
                options.pop('background')
                settings = StylerTTK.style_toolbutton(**options)
            else:
                options.pop('background')
                settings = StylerTTK.style_radiobutton(**options)                
            self.update_ttk_style(settings)


if __name__ == "__main__":

    style = Style('journal')
    root = style.master
    #root.configure(background=style.colors.bg)
    pack_settings = {'padx': 10, 'pady': 10, 'fill': 'x', 'expand': 'yes'}

    # smart keyword based style builder
    Radiobutton(root, text='default', group='colors', value=1).pack(**pack_settings)
    Radiobutton(root, text='success', group='colors', value=2, bootstyle='success').pack(**pack_settings)
    Radiobutton(root, text='info', group='colors', value=3, default=True, bootstyle='info').pack(**pack_settings)
    Radiobutton(root, text='warning', group='colors', value=4, bootstyle='warning').pack(**pack_settings)

    Radiobutton(root, text='danger toolbutton', group='colors', value=5, bootstyle='danger tool').pack(**pack_settings)
    Radiobutton(root, text='custom pink toolbutton', group='colors', value=6, indicatorcolor='pink', bootstyle='toolbutton').pack(**pack_settings)

    Radiobutton(root, text='info toolbutton', group='colors', value=5, bootstyle='info outline tool').pack(**pack_settings)
    Radiobutton(root, text='custom pink toolbutton', group='colors', value=6, background='red', indicatorcolor='pink', bootstyle='outline toolbutton').pack(**pack_settings)


    root.mainloop()

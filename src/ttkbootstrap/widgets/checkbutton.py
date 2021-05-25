"""
    A **ttkbootstrap** styled **Checkbutton** widget.

    Created: 2021-05-23
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.core import StylerTTK, Style
from ttkbootstrap.widgets import Widget


class Checkbutton(Widget, ttk.Checkbutton):
    """A Checkbutton widget is used to show or change a setting. It has two states, selected and deselected. The state
    of the checkbutton may be linked to a tkinter variable.
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
        image=None,
        indicatorcolor=None,
        offvalue=0,
        onvalue=1,
        padding=None,
        state="normal",
        style=None,
        takefocus=True,
        textvariable=None,
        text=None,
        underline=None,
        variable=None,
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
            default (bool, optional): If ``True``, the widget will initialize as selected.
            font (str, Font, optional): The font to use when drawing text inside the widget.
            foreground (str, optional): The text color. Setting this option will override all other style based 
                foreground settings.
            image (PhotoImage, optional): Specifies an image to display in the widget, which must have been created
                with ``tk.PhotoImage`` or `TkPhotoImage`` if using **pillow**. Can also be a string representing the
                name of the photo if the photo has been given a name using the ``name`` parameter.  Typically, if
                the ``image`` option is specified then it overrides other options that specify a bitmap or textual
                value to display in the widget, though this is controlled by the ``compound`` option; the ``image``
                option may be reset to an empty string to re-enable a bitmap or text display.
            indicatorcolor (str, optional): The normal color to use for the widget indicator. Setting this option will
                override all other styled based indicatorcolor options.
            offvalue (Any, optional): By default, when a checkbutton is in the off (unchecked) state, the value of the 
                variable is 0. You can use the ``offvalue`` option to specify a different value for the off state.
            onvalue (Any, optional): By default, when a checkbutton is in the on (checked) state, the value of the 
                variable is 1. You can use the ``onvalue`` option to specify a different value for the on state.
            padding (str, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            state (str, optional): May be set to ``normal`` or ``disabled`` to control the disabled state bit. This is
                a write-only option: setting it changes the widget state, but the state widget command does not affect
                the ``state`` option.
            style (str, optional): May be used to specify a custom widget style.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). To remove the widget from focus traversal, use ``takefocus=False``.
            text (str, optional): Specifies a string to be displayed inside the widget.
            textvariable (Variable, optional): Specifies the name or instance of a tkinter variable whose value will be
                used in place of the ``text`` resource.
            underline (int, optional): Specifies the integer index of a character to underline in the widget. This
                option is used by the default bindings to implement keyboard traversal for menu buttons and menu
                entries. 0 corresponds to the first character of the text displayed in the widget, 1 to the next
                character, and so on.
            variable (Variable, optional): A control variable that tracks the current state of the checkbutton. If a 
                variable is not provided, one is created by default and can be set and accessed directly or via the 
                ``value`` property.
            width (int, optional): If the label is text, this option specifies the absolute width of the text area on
                the button, as a number of characters; the actual width is that number multiplied by the average width
                of a character in the current font. For image labels, this option is ignored. The option may also be
                configured in a style.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TCheckbutton", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.font = font
        self.foreground = foreground
        self.indicatorcolor = indicatorcolor
        self.widget_id = None
        self.variable = variable or Variable(value=onvalue if default else offvalue)

        self.customized = False
        self.customize_widget()

        ttk.Checkbutton.__init__(
            self,
            master=master,
            command=command,
            compound=compound,
            cursor=cursor,
            image=image,
            padding=padding,
            onvalue=onvalue,
            offvalue=offvalue,
            state=state,
            style=self.style,
            takefocus=takefocus,
            text=text,
            textvariable=textvariable,
            underline=underline,
            variable=self.variable,
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

            if "Roundtoggle" in self.style:
                settings = StylerTTK.style_roundtoggle(**options)
            elif "Squaretoggle" in self.style:
                settings = StylerTTK.style_squaretoggle(**options)                
            else:
                settings = StylerTTK.style_checkbutton(**options)

            self.update_ttk_style(settings)


if __name__ == "__main__":

    style = Style()
    root = style.master
    #root.configure(background=style.colors.bg)
    pack_settings = {'padx': 10, 'pady': 10, 'fill': 'x', 'expand': 'yes'}

    # smart keyword based style builder
    Checkbutton(root, text='default').pack(**pack_settings)
    Checkbutton(root, text='secondary', bootstyle='secondary').pack(**pack_settings)
    Checkbutton(root, text='info outline', indicatorcolor='blue', bootstyle='info').pack(**pack_settings)
    Checkbutton(root, text='danger link', state='disabled', bootstyle='danger-link').pack(**pack_settings)

    # customizable colors
    Checkbutton(root, text='custom solid', indicatorcolor='purple', foreground='pink').pack(**pack_settings)
    Checkbutton(root, text='custom outline', foreground='yellow', default=True).pack(**pack_settings)
    Checkbutton(root, text='custom link', foreground='orange').pack(**pack_settings)

    Checkbutton(root, text='default toggle', bootstyle='info toggle').pack(**pack_settings)
    Checkbutton(root, font='Consolas 10', text='custom toggle', indicatorcolor='purple', bootstyle='toggle').pack(**pack_settings)

    Checkbutton(root, text='info square toggle', bootstyle='info squaretoggle').pack(**pack_settings)
    Checkbutton(root, text='square toggle', indicatorcolor='pink', bootstyle='squaretoggle').pack(**pack_settings)    
    Checkbutton(root, text='square toggle', state='disabled', bootstyle='squaretoggle').pack(**pack_settings)

    root.mainloop()

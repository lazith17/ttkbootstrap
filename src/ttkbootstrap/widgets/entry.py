"""
    A **ttkbootstrap** styled **Entry** widget.

    Created: 2021-05-27
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Entry(Widget, ttk.Entry):
    """The Entry widget displays a one-line text string and allows that string to be edited by the user. The value of
    the string may be linked to a variable with the textvariable option. Entry widgets support horizontal scrolling
    with the standard xscrollcommand option and xview widget command."""

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        cursor=None,
        exportselection=False,
        focuscolor=None,
        font=None,
        foreground=None,
        invalidcommand=None,
        justify=None,
        padding=None,
        show=None,
        state="normal",
        style=None,
        takefocus=True,
        textvariable=None,
        validate=None,
        validatecommand=None,
        width=None,
        xscrollcommand=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            background (str, optional): The normal background color to use for the Entry. Setting this option will
                override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            exportselection (bool, optional): Boolean value. If set, the widget selection is linked to the X selection.
            focuscolor (str, optional): The color of the focus ring when the widget has focus.
            font (str or Font, optional): The font used to render the widget text.
            foreground (str, optional): The color of the text inside the Entry widget. Setting this option will
                override all other style-based foreground setting.
            invalidcommand (func, optional): A script template to evaluate whenever the ``validatecommand`` returns 0.
            justify (str, optional): Specifies how the text is aligned within the widget. Must be one of left, center,
                or right.
            padding (Any, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            show (str, optional): If this option is specified, then the true contents of the entry are not displayed in
                the window. Instead, each character in the entry's value will be displayed as the first character in
                the value of this option, such as “*” or a bullet. This is useful, for example, if the entry is to be
                used to enter a password. If characters in the entry are selected and copied elsewhere, the information
                copied will be what is displayed, not the true contents of the entry.
            state (str, optional): One of `normal`, `readonly`, or `disabled`. In the readonly state, the value may not
                be edited directly, and the user can only select one of the -values from the dropdown list. In the
                normal state, the text field is directly editable. In the disabled state, no interaction is possible.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            textvariable(Variable, optional): Specifies the name of a global variable whose value is linked to the
                entry widget's contents. Whenever the variable changes value, the widget's contents are updated, and
                vice versa.
            validate (str, optional): Specifies the mode in which validation should operate: none, focus, focusin,
                focusout, key, or all. Default is none, meaning that validation is disabled.
            validatecommand (func, optional): A script template to evaluate whenever validation is triggered. If set to
                the empty string (the default), validation is disabled. The script must return a boolean value.
            width (int, optional): Specifies an integer value indicating the desired width of the entry window, in
                average-size characters of the widget's font.
            xscrollcommmand (func, optional): A command prefix, used to communicate with horizontal scrollbars. When
                the view in the widget's window changes, the widget will generate a command by concatenating the
                scroll command and two numbers. Each of the numbers is a fraction between 0 and 1 indicating a
                position in the document; 0 indicates the beginning, and 1 indicates the end. The first fraction
                indicates the first information in the widget that is visible in the window, and the second fraction
                indicates the information just after the last portion that is visible. If this option is set to the
                empty string (the default), then no command will be executed.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TEntry", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.focuscolor = focuscolor
        self.foreground = foreground
        self.font = font or DEFAULT_FONT
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Entry.__init__(
            self,
            master=master,
            cursor=cursor,
            exportselection=exportselection,
            font=font,
            invalidcommand=invalidcommand,
            justify=justify,
            padding=padding,
            show=show,
            state=state,
            style=self.style,
            takefocus=takefocus,
            textvariable=textvariable,
            validate=validate,
            validatecommand=validatecommand,
            width=width,
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
            settings = StylerTTK.style_entry(**options)

            self.update_ttk_style(settings)

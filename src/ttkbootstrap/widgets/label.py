"""
    A **ttkbootstrap** styled **Label** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from tkinter import Variable
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Label(Widget, ttk.Label):
    """A Label widget displays a textual label and/or image. The label may be linked to a variable to automatically
    change the displayed text."""

    def __init__(
        self,
        master=None,
        anchor=None,
        background=None,
        bootstyle="default",
        compound=None,
        cursor=None,
        font=None,
        foreground=None,
        image=None,
        justify=None,
        padding=None,
        state="normal",
        style=None,
        takefocus=False,
        text=None,
        textvariable=None,
        underline=None,
        width=None,
        wraplength=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            anchor (str, optional): Specifies how the information in the widget is positioned relative to the inner
                margins. Legal values are n, ne, e, se, s, sw, w, nw, and center.
            background (str, optional): The normal color to use on the Label when displaying the widget. Setting
                this option will override all other style-based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            compound (str, optional): Specifies how to display the image relative to the text, in the case both
                ``text`` and ``image`` are present. Valid values are: text, image, center, top, bottom, left, right,
                none.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            font (str or Font, optional): The font to use for text displayed by the widget.
            foreground (str, optional): The text color.
            image (PhotoImage, optional): Specifies an image to display.
            justify (str, optional): If there are multiple lines of text, specifies how the lines are laid out
                relative to one another. One of left, center, or right.
            padding (Any, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            state (str, optional): May be set to `normal` or `disabled`. If disabled, the user cannot change the content.
            style (str, optional): May be used to specify a style using the ``ttk`` style api.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). This widget does not accept traversal by default.
            text (str, optional): Specifies a text string to be displayed inside the widget (unless overridden by
                ``textvariable``). This is also a property which can be used to access and set the value of the label.
            textvariable (Variable, optional): Specifies the name of a variable whose value will be used in place of
                the ``text`` resource. If not assigned, this is created by default and can be accessed directly or via
                the ``text`` property.
            underline (int, optional): If set, specifies the integer index (0-based) of a character to underline in the
                text string. The underlined character is used for mnemonic activation.
            width (int, optional): The widget's requested width in pixels.
            wraplength (int, optional): Specifies the maximum line length (in pixels). If this option is less than or
                equal to zero, then automatic wrapping is not performed; otherwise the text is split into lines such
                that no line is longer than the specified value.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TLabel", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.foreground = foreground
        self.textvariable = textvariable or Variable(value=text)
        self.widget_id = None

        self.customized = False
        self.customize_widget()

        ttk.Label.__init__(
            self,
            master=master,
            anchor=anchor,
            compound=compound,
            cursor=cursor,
            font=font,
            image=image,
            justify=justify,
            padding=padding,
            state=state,
            style=self.style,
            takefocus=takefocus,
            text=text,
            textvariable=self.textvariable,
            underline=underline,
            width=width,
            wraplength=wraplength,
            **kw,
        )
        self.bind("<<ThemeChanged>>", self.on_theme_change)

    def customize_widget(self):

        if any([self.background != None, self.foreground != None]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "background": self.background,
                "foreground": self.foreground,
                "style": self.style,
            }

            if "Inverse" in self.style:
                options["background"] = self.background or self.themed_color
            else:
                options["foreground"] = self.foreground or self.themed_color
            settings = StylerTTK.style_label(**options)
            self.update_ttk_style(settings)

    @property
    def text(self):
        return self.textvariable.get()

    @text.setter
    def text(self, value):
        self.textvariable.set(value)

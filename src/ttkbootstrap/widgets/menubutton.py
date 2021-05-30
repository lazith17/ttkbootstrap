"""
    A **ttkbootstrap** styled **Menubutton** widget.

    Created: 2021-05-28
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Menubutton(Widget, ttk.Menubutton):
    """A ttk.Menubutton widget displays a textual label and/or image, and displays a menu when pressed.
    """

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        compound=None,
        cursor=None,
        direction=None,
        font=None,
        hidearrow=False,
        foreground=None,
        image=None,
        menu=None,
        padding=None,
        state="normal",
        style=None,
        takefocus=True,
        textvariable=None,
        text=None,
        underline=None,
        width=None,
        **kw,
    ):
        """
        Args:
            master (Widget, optional): The parent widget.
            background (str, optional): The normal background color to use when displaying the widget. Setting this
                option will override all other style based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a short-hand
                API for setting the widget style. You may also use the ``style`` option directly using the standard
                ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            compound (str, optional): Specifies if the widget should display text and bitmaps/images at the same time,
                and if so, where the bitmap/image should be placed relative to the text. Must be one of the values
                **none**, **bottom**, **top**, **left**, **right**, or **center**. For example, the (default) value
                **none** specifies that the bitmap or image should (if defined) be displayed `instead` of the text, the
                value **left** specifies that the bitmap or image should be displayed to the `left` of the text, and
                the value **center** specifies  that the bitmap or image should be displayed `underneath` the text.
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values will
                vary according to your operating system.
            direction (str, optional): Specifies where the menu is to be popped up relative to the menubutton. One of: 
                above, below, left, right, or flush. The default is below. flush pops the menu up directly over the 
                menubutton. 
            font (str or Font, optional): The font to use when drawing text inside the widget.
            foreground (str, optional): The normal foreground color to use when displaying the widget. Setting this
                option will override all other style based foreground settings.
            hidearrow (bool, optional): Hides the downarrow that is shown on the button by default.
            image (PhotoImage, optional): Specifies an image to display in the widget, which must have been created
                with ``tk.PhotoImage`` or `TkPhotoImage`` if using **pillow**. Can also be a string representing the
                name of the photo if the photo has been given a name using the ``name`` parameter.  Typically, if
                the ``image`` option is specified then it overrides other options that specify a bitmap or textual
                value to display in the widget, though this is controlled by the ``compound`` option; the ``image``
                option may be reset to an empty string to re-enable a bitmap or text display.
            padding (str, optional): Specifies the internal padding for the widget. The padding is a list of up to four
                length specifications left top right bottom. If fewer than four elements are specified, bottom defaults
                to top, right defaults to left, and top defaults to left. In other words, a list of three numbers
                specify the left, vertical, and right padding; a list of two numbers specify the horizontal and the
                vertical padding; a single number specifies the same padding all the way around the widget.
            state (str, optional): May be set to ``normal`` or ``disabled`` to control the disabled state bit. This is
                a write-only option: setting it changes the widget state, but the state widget command does not affect
                the ``state`` option.
            style (str, optional): May be used to specify a custom widget style.
            takefocus (bool, optional): Determines whether the widget accepts the focus during keyboard traversal
                (e.g., Tab and Shift-Tab). To remove the widget from focus traversal, use ``takefocus=False``.
            text (str, optional): Specifies a string to be displayed inside the widget.
            textvariable (Variable, optional): Specifies the name or instance of a tkinter variable whose value will be
                used in place of the ``text`` resource.
            underline (int, optional): Specifies the integer index of a character to underline in the widget. This
                option is used by the default bindings to implement keyboard traversal for menu buttons and menu
                entries. 0 corresponds to the first character of the text displayed in the widget, 1 to the next
                character, and so on.
            width (int, optional): If greater than zero, specifies how much space, in character widths, to allocate for
                the text label. If less than zero, specifies a minimum width. If zero or unspecified, the natural width
                of the text label is used.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "TMenubutton", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.arrowsize = 0 if hidearrow else 4
        self.background = background
        self.font = font
        self.foreground = foreground
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Menubutton.__init__(
            self,
            master=master,
            compound=compound,
            cursor=cursor,
            direction=direction,
            image=image,
            menu=menu,
            padding=padding,
            state=state,
            style=self.style,
            takefocus=takefocus,
            text=text,
            textvariable=textvariable,
            underline=underline,
            width=width,
            **kw,
        )
        self.bind("<<ThemeChanged>>", self.on_theme_change)

    def _customize_widget(self):

        if any([self.background != None, self.foreground != None, self.font != None, self.arrowsize == 0]):
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "arrowsize": self.arrowsize,
                "background": self.background,
                "foreground": self.foreground,
                "font": self.font,
                "style": self.style,
            }

            if "Outline" in self.style:
                self.foreground = self.foreground or self.themed_color
                settings = StylerTTK.style_outline_menubutton(**options)
            else:
                self.background = self.background or self.themed_color
                settings = StylerTTK.style_menubutton(**options)

            self.update_ttk_style(settings)

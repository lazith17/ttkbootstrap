"""
    A **ttkbootstrap** styled **Button** widget.

    Created: 2021-05-13
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from tkinter import ttk
from ttkbootstrap.core import StylerTTK, Style
from ttkbootstrap.widgets import Widget


class Button(Widget, ttk.Button):
    """A Button widget displays a textual string, bitmap or image. If text is displayed, it must all be in a single
    font, but it can occupy multiple lines on the screen (if it contains newlines or if wrapping occurs because of
    the wraplength option) and one of the characters may optionally be underlined using the underline option. It
    can display itself in either of three different ways, according to the state option; it can be made to appear
    raised, sunken, or flat; and it can be made to flash. When a user invokes the button (by pressing mouse button
    1 with the cursor over the button), then the command specified in the command option is invoked.
    """

    def __init__(self,

                 # widget options
                 master=None,
                 anchor=None,
                 bootstyle='default',
                 command=None,
                 compound=None,
                 cursor=None,
                 font=None,
                 image=None,
                 state='normal',
                 style=None,
                 takefocus=True,
                 textvariable=None,
                 text=None,
                 underline=None,

                 # custom style options
                 background=None,
                 foreground=None,
                 **kw):
        """
        Args:
            master (Widget, optional): The parent widget.
            anchor (str, optional): Specifies how the information in the widget is positioned relative to 
                the inner margins. Legal values are `n`, `ne`, `e`, `se`, `s`, `sw`, `w`, `nw`, and `center`.
            background (str, optional): The normal background color to use when displaying the widget.
                Setting this option will override all other style based background settings.
            bootstyle (str, optional): The **ttkbootstrap** style used to render the widget. This is a
                short-hand API for setting the widget style. You may also use the ``style`` option directly
                using the standard ``ttk`` API. Using the ``Style`` option will overwrite the ``bootstyle``.
            command (func, optional): A callback function to evaluate when the widget is invoked.
            compound (str, optional): Specifies if the widget should display text and bitmaps/images at the 
                same time, and if so, where the bitmap/image should be placed relative to the text. Must be 
                one of the values **none**, **bottom**, **top**, **left**, **right**, or **center**. For 
                example, the (default) value **none** specifies that the bitmap or image should (if defined) 
                be displayed `instead` of the text, the value **left** specifies that the bitmap or image 
                should be displayed to the `left` of the text, and the value **center** specifies  that the 
                bitmap or image should be displayed `underneath` the text. 
            cursor (str, optional): Specifies the `mouse cursor`_ to be used for the widget. Names and values
                will vary according to your operating system.
            font (str, Font, optional): The font to use when drawing text inside the widget. The value may 
                have any of the forms described in the `font manual page`_ under FONT DESCRIPTION.
            foreground (str, optional): The normal foreground color to use when displaying the widget.
                Setting this options will override all other style based foreground settings.
            image (PhotoImage, optional): Specifies an image to display in the widget, which must have been 
                created with ``tk.PhotoImage`` or `TkPhotoImage`` if using **pillow**. Can also be a 
                string representing the name of the photo if the photo has been given a name using the 
                ``name`` parameter.  Typically, if the ``image`` option is specified then it overrides other 
                options that specify a bitmap or textual value to display in the widget, though this is 
                controlled by the ``compound`` option; the ``image`` option may be reset to an empty string 
                to re-enable a bitmap or text display. 
            padding (str, optional): Specifies the internal padding for the widget. The padding is a list 
                of up to four length specifications left top right bottom. If fewer than four elements are 
                specified, bottom defaults to top, right defaults to left, and top defaults to left. In other 
                words, a list of three numbers specify the left, vertical, and right padding; a list of two 
                numbers specify the horizontal and the vertical padding; a single number specifies the same 
                padding all the way around the widget.
            state (str, optional): May be set to ``normal`` or ``disabled`` to control the disabled state 
                bit. This is a write-only option: setting it changes the widget state, but the state widget 
                command does not affect the ``state`` option.
            style (str, optional): May be used to specify a custom widget style.
            takefocus (bool, optional): Determines whether the window accepts the focus during keyboard 
                traversal (e.g., Tab and Shift-Tab). To remove the widget from focus traversal, use 
                ``takefocus=False``.
            text (str, optional): Specifies a string to be displayed inside the widget.
            textvariable (Variable, optional): Specifies the name or instance of a tkinter variable whose 
                value will be used in place of the ``text`` resource.
            underline (int, optional): Specifies the integer index of a character to underline in the 
                widget. This option is used by the default bindings to implement keyboard traversal for menu 
                buttons and menu entries. 0 corresponds to the first character of the text displayed in the 
                widget, 1 to the next character, and so on. 
            width (int, optional): If the label is text, this option specifies the absolute width of the 
                text area on the button, as a number of characters; the actual width is that number 
                multiplied by the average width of a character in the current font. For image labels, this 
                option is ignored. The option may also be configured in a style.
            wraplength (int, optional): Specifies the maximum line length (in pixels). If this option is 
                less than or equal to zero, then automatic wrapping is not performed; otherwise the text is 
                split into lines such that no line is longer than the specified value    

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, 'TButton', master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.anchor = anchor
        self.background = background
        self.font = font
        self.foreground = foreground

        self.customized = False
        self.customize_widget()

        ttk.Button.__init__(self, master=master, command=command, compound=compound, cursor=cursor,
                            image=image, state=state, style=self.style, takefocus=takefocus, text=text,
                            textvariable=textvariable, underline=underline, **kw)

    def style_exists(self):
        """Check if a ttk style exists and return a boolean

        Returns:
            bool: ``True`` if the style exists, else ``False``
        """
        return True if self.tk.call('ttk::style', 'configure', self.style) else False

    def customize_widget(self):
        if any([self.background != None, self.foreground != None, self.anchor != None, self.font != None]):
            self.style = 'custom.TButton'
            settings = StylerTTK.style_solid_buttons(
                self.theme, anchor=self.anchor, background=self.background, font=self.font,
                foreground=self.foreground, style=self.style)
            self.update_ttk_style(settings)


if __name__ == '__main__':

    style = Style()
    root = style.master
    root.configure(background=style.colors.bg)

    # smart keyword based style builder
    Button(root, text='Push', bootstyle='btn-primary-outline').pack(padx=1, pady=1)
    Button(root, text='Push', bootstyle='INFO').pack(padx=1, pady=1)
    Button(root, text='Push', bootstyle='link danger').pack(padx=1, pady=1)
    Button(root, text='Push', bootstyle='secondary').pack(padx=1, pady=1)
    Button(root, text='Push', bootstyle='success----label').pack(padx=1, pady=1)

    Button(root, text='Push').pack(padx=1, pady=1, fill='x')

    # backwards compatible with ttk widgets
    ttk.Button(root, text='Push', style='danger.TButton').pack(
        padx=1, pady=1, fill='x')

    # can be customized in the constructor
    Button(root, text='Push', anchor='e', font='helvetica 20', foreground='yellow', background='green',
           underline=1, cursor='pencil', padding=20).pack(padx=1, pady=1, fill='x')

    root.mainloop()

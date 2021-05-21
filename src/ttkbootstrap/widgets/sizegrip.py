"""
    A **ttkbootstrap** styled **Sizegrip** widget.

    Created: 2021-05-21
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK, Style
from ttkbootstrap.widgets import Widget


class Sizegrip(Widget, ttk.Sizegrip):
    """A Sizegrip widget (also known as a grow box) allows the user to resize the containing toplevel window by
    pressing and dragging the grip."""

    def __init__(
        self,
        master=None,
        background=None,
        bootstyle="default",
        cursor=None,
        foreground=None,
        style=None,
        takefocus=True,
        **kw,
    ):

        Widget.__init__(self, "TSizegrip", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.background = background
        self.foreground = foreground
        self.widget_id = None

        self.customized = False
        self.customize_widget()

        ttk.Sizegrip.__init__(
            self,
            master=master,
            cursor=cursor,
            style=self.style,
            takefocus=takefocus,
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
                "foreground": self.foreground or self.themed_color,
                "style": self.style,
            }
            settings = StylerTTK.style_sizegrip(**options)

            self.update_ttk_style(settings)


if __name__ == "__main__":

    style = Style()
    root = style.master
    root.configure(background=style.colors.bg)
    pack_settings = {"fill": "both", "expand": "yes"}

    Sizegrip(root).pack(**pack_settings)
    Sizegrip(root, bootstyle='info', background='light gray').pack(**pack_settings)
    Sizegrip(root, foreground='red').pack(**pack_settings)
    Sizegrip(root, foreground='blue', background='orange').pack(**pack_settings)

    root.mainloop()


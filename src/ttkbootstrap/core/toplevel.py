import tkinter as tk
from tkinter import PhotoImage
from ttkbootstrap.core import ICON
from ttkbootstrap.core import Style, Window

from sys import platform

# TODO implement a grabanywhere functionality so that the window can be moved if the titlebar is removed.

DEFAULT_THEME = "flatly"


class Toplevel(tk.Toplevel):
    """The Toplevel widget is used to create and display the toplevel windows which are directly managed by the window
    manager. The toplevel widget may or may not have the parent window on the top of them. The toplevel widget is used
    when a python application needs to represent some extra information, pop-up, or the group of widgets on the new
    window. The toplevel windows have the title bars, borders, and other window decorations."""

    def __init__(
        self,
        parent=None,
        title="ttkbootstrap",
        theme=DEFAULT_THEME,
        size=(None, None),
        maxsize=(None, None),
        minsize=(None, None),
        resizeable=(True, True),
        offset=(None, None),
        fullscreen=False,
        topmost=False,
        alpha=1.0,
        icon=None,
        removetitlebar=False,
        **kw,
    ):
        """
        Args:
            parent: The parent window; setting this option will make the window transient and will work on behalf of the parent.
            title (str): The application name to appear on the title bar.
            theme (str): The **ttkbootstrap** theme to apply to the window; the toplevel theme CAN be different than the parent.
            size (Tuple[int, int]): The absolute (height, width) of the application window.
            maxsize (Tuple[int, int]): The maximum permissable size of the window (width, height).
            minsize (Tuple[int, int]): The minimum permissable size of the window (width, height).
            resizeable (Tuple[bool, bool]): Indicates whether the screen is resizable on the `horizontal` or `vertical` axis. The tuple represents (`horizontal`, `vertical`).
            offset (Tuple[int, int]): The (x-offset, y-offset) of the application window relative to the 'northwest' corner of the screen.
            fullscreen (bool): Places the window in a mode that takes up the entire screen and has no borders. Default is ``False``.
            topmost (bool): Specifies whether to place this window above all other windows. Default is ``False``.
            alpha (float): The transparency level of the window. Accepts a range between 0.0 (transparent) and 1.0 (opaque).
            icon (str): The filename of an image to use as the application icon.
            removetitlebar (bool): Calls the `overrideredirect` method and removes all native window decoration.
        """
        tk.Toplevel.__init__(self, **kw)
        self.platform = platform
        self.parent = parent

        if parent:
            self.transient(parent)
            parent_style = self.parent.__dict__.get("style")
            parent_theme = parent_style.theme.name
            top_theme = parent_theme if theme == DEFAULT_THEME else theme
            self.style = parent_style if parent_theme == top_theme else Style(master=self.parent, themename=top_theme)
        else:
            self.style = Style(master=self, themename=theme)

        self.attributes("-topmost", topmost)
        self.attributes("-alpha", alpha)
        self.minsize(*minsize)
        self.maxsize(*maxsize)
        self.resizable(*resizeable)
        self.title(title)

        if removetitlebar:
            self.overrideredirect(removetitlebar)
            self.attributes("-topmost", True)
            self.bind("<Escape>", lambda _: self.destroy())

        # user provided icon or default
        if icon:
            self.icon = PhotoImage(file=icon)
        else:
            self.icon = PhotoImage(data=ICON)
        self.iconphoto(False, self.icon)

        # fullscreen is platform dependent
        if platform == "win32":
            self.attributes("-fullscreen", fullscreen)
        else:
            self.attributes("-zoomed", fullscreen)

        # build geometry from parameters
        height, width = size
        geometry = ""
        if all([height, width]):
            geometry = f"{height}x{width}"
        xpos, ypos = offset
        geometry += f"+{xpos or 0}+{ypos or 0}"
        self.geometry(geometry)


if __name__ == "__main__":

    root = Window(theme="minty")
    top = Toplevel(root, title="Testing")
    root.mainloop()

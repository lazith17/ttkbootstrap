import tkinter as tk
from tkinter import PhotoImage
from ttkbootstrap.style import Style
from ttkbootstrap.assets.icon import ICON

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
        title=None,
        theme=DEFAULT_THEME,
        size=(None, None),
        max_size=(None, None),
        min_size=(None, None),
        resizeable=(True, True),
        position=(0, 0, 'relative'),
        fullscreen=False,
        topmost=False,
        alpha=1.0,
        icon=None,
        remove_titlebar=False,
        hide_on_close=False,
        **kw,
    ):
        """
        Args:
            parent: The parent window; setting this option will make the window transient and will work on behalf of the parent.
            title (str): The application name to appear on the title bar.
            theme (str): The **ttkbootstrap** theme to apply to the window; the toplevel theme CAN be different than the parent.
            size (Tuple[int, int]): The absolute (height, width) of the application window.
            max_size (Tuple[int, int]): The maximum permissable size of the window (width, height).
            min_size (Tuple[int, int]): The minimum permissable size of the window (width, height).
            resizeable (Tuple[bool, bool]): Indicates whether the screen is resizable on the `horizontal` or `vertical` axis. The tuple represents (`horizontal`, `vertical`).
            position (Tuple[int, int, str]): A tuple that specifies where to place the topside window. The first two items are x and y position. The last item is the type of position. The position type options include: `absolute`, `relative`, and `offset`. Absolute position uses the absolute values of x and y coordinates starting from the Northwest corner of the screen as (0, 0). Relative position are floating point values between 0 and 1. Finally, offset positions are the number of pixels to offset from the parent or master window's northwest corner.
            fullscreen (bool): Places the window in a mode that takes up the entire screen and has no borders. Default is ``False``.
            topmost (bool): Specifies whether to place this window above all other windows. Default is ``False``.
            alpha (float): The transparency level of the window. Accepts a range between 0.0 (transparent) and 1.0 (opaque).
            icon (str): The filename of an image to use as the application icon.
            remove_titlebar (bool): Calls the `overrideredirect` method and removes all native window decoration.
            hide_on_close (bool): Hide the window on close instead of destroying it.
        """
        tk.Toplevel.__init__(self, **kw)
        self.withdraw()  # remain hidden until using ``show`` or ``deiconify``
        self.protocol("WM_DELETE_WINDOW", self.hide if hide_on_close else self.destroy)
        self.platform = platform
        self.position = position
        if parent:
            self.parent = parent
            self.style = parent.style
        else:
            self.parent = self.master
            self.style = Style(master=self, themename=theme)
        
        # set window options
        self.transient(self.parent)
        self.attributes("-topmost", topmost)
        self.attributes("-alpha", alpha)
        self.minsize(*min_size)
        self.maxsize(*max_size)
        self.resizable(*resizeable)
        self.title(title)

        if remove_titlebar:
            self.overrideredirect(remove_titlebar)
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

    def set_position(self):
        """Set the geometry of the widget"""
        self.update_idletasks()
        w_width = self.winfo_reqwidth()
        w_height = self.winfo_reqheight()
        wx, wy, pos_type = self.position

        p_width = self.parent.winfo_width()
        p_height = self.parent.winfo_height()
        px = self.parent.winfo_x()
        py = self.parent.winfo_y()

        if pos_type == 'relative':
            x = int(px + (p_width - w_width) * wx)
            y = int(py + (p_height - w_height) * wy)
        elif pos_type == 'offset':
            x = int(px + wx)
            y = int(py + wy)
        else:
            x = int(wx)
            y = int(wy)
        self.geometry(f"+{x}+{y}")

    def show(self):
        """Update and display the window"""
        self.update_idletasks()
        self.set_position()
        self.deiconify()

    def hide(self):
        """Hide the window from view"""
        self.withdraw()



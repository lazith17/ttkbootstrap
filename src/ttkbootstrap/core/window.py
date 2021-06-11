from tkinter import Tk, PhotoImage
from ttkbootstrap.core import Style
from ttkbootstrap.core import ICON
from sys import platform

# TODO add a -centerwindow option or method that allows the user to center the window on the screen.


class Window(Tk):
    """The main **ttkbootstrap** application window. The Window has titlebars, borders, and other window decorations
    and is used as a container for widgets that the user interacts with. The window can be themed using built-in
    **ttkbootstrap** themes to change the look and feel of the Window and all its contained widgets.
    """

    def __init__(
        self,
        title="ttkbootstrap",
        theme="flatly",
        size=(None, None),
        maxsize=(None, None),
        minsize=(None, None),
        offset=(0, 0),
        resizeable=(True, True),
        fullscreen=False,
        topmost=False,
        alpha=1.0,
        icon=None,
    ):
        """
        Args:
            title (str): The application name to appear on the title bar.
            theme (str): The name of the ``ttkbootstrap`` theme to apply to the application.
            size (Tuple[int, int]): The absolute (height, width) of the application window.
            maxsize (Tuple[int, int]): The maximum permissable size of the window (width, height).
            minsize (Tuple[int, int]): The minimum permissable size of the window (width, height).
            offset (Tuple[int, int]): The (x-offset, y-offset) of the application window relative to the 'northwest' corner of the screen.
            resizeable (Tuple[bool, bool]): Indicates whether the screen is resizable on the `horizontal` or `vertical` axis. The tuple represents (`horizontal`, `vertical`).
            fullscreen (bool): Places the window in a mode that takes up the entire screen and has no borders. Default is ``False``.
            topmost (bool): Specifies whether to place this window above all other windows. Default is ``False``.
            alpha (float): The transparency level of the window. Accepts a range between 0.0 (transparent) and 1.0 (opaque).
            icon (str): The filename of an image to use as the application icon.
        """
        super().__init__()
        self.withdraw()
        self.platform = platform
        self.style = Style(master=self, themename=theme)
        self.title(title)
        self.resizable(*resizeable)
        self.configure(background=self.style.colors.bg)
        self.minsize(*minsize)
        self.maxsize(*maxsize)

        # user icon or fallback
        if icon:
            self.icon = PhotoImage(file=icon)
        else:
            self.icon = PhotoImage(data=ICON)
        self.iconphoto(True, self.icon)

        # set window attributes
        self.attributes("-topmost", topmost)
        self.attributes("-alpha", alpha)

        if self.platform == "win32":
            self.attributes("-fullscreen", fullscreen)
        else:
            self.attributes("-zoomed", fullscreen)

        # set window geometry
        height, width = size
        geometry = ""
        if all([height, width]):
            geometry = f"{height}x{width}"
        xpos, ypos = offset
        geometry += f"+{xpos}+{ypos}"
        self.geometry(geometry)
        self.update_idletasks()
        self.deiconify()

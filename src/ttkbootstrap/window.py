from sys import platform
from tkinter import Tk, PhotoImage
from ttkbootstrap.style import Style
from ttkbootstrap.constants import *
from ttkbootstrap.assets.icon import ICON

# TODO add a -centerwindow option or method that allows the user to center the window on the screen.
THEME = 'flatly'
POS_NORM = '+'
POS_INV = '-'

class Application(Tk):
    """The main **ttkbootstrap** application window. The Application window has titlebars, borders, and other window 
    decorations and is used as a container for widgets that the user interacts with. The window can be themed using 
    built-in **ttkbootstrap** themes to change the look and feel of the Window and all its contained widgets.
    """

    def __init__(
        self,
        title="ttkbootstrap",
        theme=THEME,
        size=(None, None),
        maxsize=(None, None),
        minsize=(None, None),
        position=(0, -100, CENTER),
        resizeable=(True, True),
        fullscreen=False,
        topmost=False,
        alpha=1.0,
        icon=None,
        build_all_themes=False,
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
            build_all_themes (bool): Build all themes in-memory instead of on-demand (default).
        """
        super().__init__()
        self.withdraw()
        self.platform = platform
        self.style = Style(master=self, themename=theme)
        self.title(title)
        self.resizable(*resizeable)
        self.configure(background=self.style.colors.bg)
        if self.minsize:
            self.minsize(*minsize)
        if self.maxsize:
            self.maxsize(*maxsize)
        self.size = size

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
        self.position = position

    def set_position(self):
        """Set the geometry of the widget"""
        self.update_idletasks()
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        w_width = self.size[0] or self.winfo_reqwidth()
        w_height = self.size[1] or self.winfo_reqheight()
        x, y, anchor = self.position

        if anchor == NW:
            position = f'{POS_NORM}{x}{POS_NORM}{y}'
        elif anchor == SW:
            position = f'{POS_NORM}{x}{POS_INV}{y}'
        elif anchor == NE:
            position = f'{POS_INV}{x}{POS_NORM}{y}'
        elif anchor == SE:
            position = f'{POS_INV}{x}{POS_INV}{y}'
        elif anchor == CENTER:
            position = f'{POS_NORM}{x + (s_width - w_width)//2}{POS_NORM}{y + (s_height - w_height)//2}'
        elif anchor == N:
            position = f'{POS_NORM}{x + (s_width - w_width)//2}{POS_NORM}{y}'
        elif anchor == S:
            position = f'{POS_NORM}{x + (s_width - w_width)//2}{POS_INV}{y}'
        elif anchor == W:
            position = f'{POS_NORM}{x}{POS_NORM}{y + (s_height - w_height)//2}'
        elif anchor == E:
            position = f'{POS_INV}{x}{POS_NORM}{y + (s_height - w_height)//2}'

        size = f'{w_width}x{w_height}' if all(self.size) else ''
        self.geometry(f"{size}{position}")

    def run(self, **kw):
        """Launches the application"""
        self.mainloop(**kw)

    def mainloop(self, **kw):
        """Launches the application"""
        self.set_position()
        self.deiconify()
        super().mainloop(**kw)


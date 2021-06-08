from tkinter import PhotoImage, Tk
import ttkbootstrap as ttk
from ttkbootstrap.core import ICON
from sys import platform

class Window(Tk):

    def __init__(
        self, 
        alpha=1.0,
        fullscreen=False,
        icon=None,
        topmost=False,
        theme="flatly",
        minsize=(None, None),
        maxsize=(None, None),
        offset=(0, 0),
        resizeable = (True, True),
        size=(None, None), 
        title="ttkbootstrap", 
        ):
        """
        Args:
            alpha (float): The transparency level of the window. Accepts a range between 0.0 (transparent) and 1.0 (opaque).
            fullscreen (bool): Places the window in a mode that takes up the entire screen and has no borders. Default is ``False``.
            icon (str): The filename of an image to use as the application icon.
            topmost (bool): Specifies whether to place this window above all other windows. Default is ``False``.
            theme (str): The name of the ``ttkbootstrap`` theme to apply to the application.
            maxsize (Tuple[int, int]): The maximum permissable size of the window (width, height).
            minsize (Tuple[int, int]): The minimum permissable size of the window (width, height).
            offset (Tuple[int, int]): The (x-offset, y-offset) of the application window relative to the 'northwest' corner of the screen.
            resizeable (Tuple[bool, bool]): Indicates whether the screen is resizable on the `horizontal` or `vertical` axis. The tuple represents (`horizontal`, `vertical`).
            size (Tuple[int, int]): The absolute (height, width) of the application window.
            title (str): The application name to appear on the title bar.
        """
        super().__init__()
        self.style = ttk.Style(master=self, themename=theme)
        self.title(title)
        self.resizable(*resizeable)
        self.configure(background=self.style.colors.bg)
        self.minsize(*minsize)
        self.maxsize(*maxsize)
        
        # user icon or fallback
        if icon:
            self._icon = PhotoImage(file=icon)
        else:
            self._icon = PhotoImage(data=ICON)
        self.iconphoto(True, self._icon)
        
        # set window attributes
        self.attributes('-topmost', topmost)
        self.attributes('-alpha', alpha)

        if platform == 'win32':
            self.attributes('-fullscreen', fullscreen)        
        else:
            self.attributes('-zoomed', fullscreen)
        
        # set window geometry
        height, width = size
        geometry = ""
        if all([height, width]):
            geometry = f"{height}x{width}"
        xpos, ypos = offset
        geometry += f"+{xpos}+{ypos}"
        self.geometry(geometry)

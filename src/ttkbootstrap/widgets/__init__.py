# base widget
from .widget import Widget

from .button import Button
from .checkbutton import Checkbutton
from .combobox import Combobox
from .entry import Entry
from .frame import Frame
from .label import Label
from .listbox import Listbox
from .labelframe import LabelFrame
from .menubutton import Menubutton
from .notebook import Notebook
from .panedwindow import PanedWindow
from .progressbar import Progressbar
from .radiobutton import Radiobutton
from .separator import Separator
from .scrollbar import Scrollbar
from .scale import Scale
from .sizegrip import Sizegrip
from .spinbox import Spinbox
from .text import Text
from .treeview import Treeview

# extension widgets
from .floodgauge import Floodgauge
from .meter import Meter
from .optionmenu import OptionMenu
from .scrolledtext import ScrolledText

# backwards compatable
Labelframe = LabelFrame
Panedwindow = PanedWindow

# other tkitner classes imported as-is
from tkinter import StringVar, IntVar, BooleanVar, Variable, DoubleVar
from tkinter import PhotoImage, Menu

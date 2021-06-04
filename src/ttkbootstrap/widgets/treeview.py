"""
    A **ttkbootstrap** styled **Treeview** widget.

    Created: 2021-06-04
    Author: Israel Dryer, israel.dryer@gmail.com

"""
from src.ttkbootstrap.core.themes import DEFAULT_FONT
from uuid import uuid4
from tkinter import ttk
from ttkbootstrap.core import StylerTTK
from ttkbootstrap.widgets import Widget


class Treeview(Widget, ttk.Treeview):
    """The Treeview widget displays a hierarchical collection of items. Each item has a textual label, an optional
image, and an optional list of data values. The data values are displayed in successive columns after the tree label.

The order in which data values are displayed may be controlled by setting the displaycolumns widget option. The tree
widget can also display column headings. Columns may be accessed by number or by symbolic names listed in the columns
widget option.

Each item is identified by a unique name. The widget will generate item IDs if they are not supplied by the caller.
There is a distinguished root item, named {}. The root item itself is not displayed; its children appear at the top
level of the hierarchy.

Each item also has a list of tags, which can be used to associate event bindings with individual items and control the
appearance of the item.

Treeview widgets support horizontal and vertical scrolling with the standard [xy]scrollcommand options and [xy]view
widget commands."""

    def __init__(
        self,

        # widget options
        master=None,
        bootstyle="default",
        columns=None,
        cursor=None,
        displaycolumns='#all',
        height=None,
        padding=None,
        selectmode='extended',
        show='tree headings',
        takefocus=True,
        xscrollcommand=None,
        yscrollcommand=None,
        style=None,

        # custom style options
        headerbackground=None,
        headerfont='helvetica 10 bold',
        headerforeground=None,
        inputbackground=None,
        inputfont='helvetica 10',
        inputforeground=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            columns (List): A list of column identifiers. 
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            displaycolumns (List): A list of column identifiers (either symbolic names or integer indices) specifying which data columns are displayed and the order in which they appear, or the string #all. If set to #all (the default), all columns are shown in the order given. 
            height (int): The number of rows which should be visible.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            selectmode (str): Controls how the built-in class bindings manage the selection. One of `extended`, `browse`, or `none`. If set to extended (the default), multiple items may be selected. If browse, only a single item will be selected at a time. If none, the selection will not be changed. 
            show (str): A list specifying which tree elements to display. Values can include: `tree`, `headings`. Default is `tree headings`.
            takefocus (bool): Determines whether the widget accepts the focus during keyboard traversal.
            style (str): A ttk style api. Use ``bootstyle`` if possible.
            xscrollcommmand (func): A reference to ``xscrollbar.set`` method; used to communicate with horizontal scrollbars. 
            yscrollcommmand (func): A reference to ``yscrollbar.set`` method; used to communicate with vertical scrollbars.
            headerbackground (str): The header background color; setting this option will override theme settings.
            headerfont (str): The font used to render text in the widget.
            headerforeground (str): The header text color; setting this option will override theme settings.
            inputbackground (str): The field background color; setting this option will override theme settings.
            inputfont (str): The field cell font; setting this option will override theme settings.
            inputforeground (str): The field text color; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "Treeview", master=master, bootstyle=bootstyle, style=style)

        self.tk = master.tk
        self.headerbackground = headerbackground
        self.headerfont = headerfont
        self.headerforeground = headerforeground
        self.inputbackground = inputbackground
        self.inputfont = inputfont
        self.inputforeground = inputforeground
        self.widget_id = None

        self.customized = False
        self._customize_widget()

        ttk.Treeview.__init__(
            self,
            master=master,
            columns=columns,
            cursor=cursor,
            displaycolumns=displaycolumns,
            height=height,
            padding=padding,
            selectmode=selectmode,
            show=show,
            style=self.style,
            takefocus=takefocus,
            xscrollcommand=xscrollcommand,
            yscrollcommand=yscrollcommand,
            **kw,
        )

    def _customize_widget(self):

        if any(
            [
                self.headerbackground != None, 
                self.headerforeground != None, 
                self.headerfont != DEFAULT_FONT,
                self.inputbackground != None, 
                self.inputfont != DEFAULT_FONT,
                self.inputforeground != None]):
            
            self.customized = True

            if not self.widget_id:
                self.widget_id = uuid4() if self.widget_id == None else self.widget_id
                self.style = f"{self.widget_id}.{self.style}"

        if self.customized:
            options = {
                "theme": self.theme,
                "headerbackground": self.headerbackground,
                "headerfont": self.headerfont,
                "headerforeground": self.headerforeground,
                "inputbackground": self.inputbackground,
                "inputfont": self.inputfont,
                "inputforeground": self.inputforeground,
                "style": self.style,
            }
            settings = StylerTTK.style_treeview(**options)

            self.update_ttk_style(settings)

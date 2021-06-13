"""
    A **ttkbootstrap** styled **Listbox** widget.
    Created: 2021-06-09
"""

from uuid import uuid4
import tkinter
from ttkbootstrap.themes import DEFAULT_FONT, ThemeColors
from ttkbootstrap.widgets import Widget


class Listbox(Widget, tkinter.Listbox):
    """The Listbox widget displays a list of items from which the user can select.

    This widget is adapted from the original tkinter listbox, so additional keywords for this widget can be passed
    in addition to the ones exposed via the bootstrap api.
    """

    def __init__(
        self,
        # widget options
        master=None,
        activestyle="none",
        bootstyle="default",
        cursor=None,
        exportselection=True,
        height=None,
        justify="left",
        listvariable=None,
        selectmode="browse",
        state="normal",
        style=None,
        takefocus=True,
        values=None,
        width=None,
        xscrollcommand=None,
        yscrollcommand=None,
        # custom style options
        background=None,
        borderwidth=1,
        foreground=None,
        font=None,
        selectbackground=None,
        selectforeground=None,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            activestyle (str): Specifies the style in which to draw the active element. This must be one of dotbox (show a focus ring around the active element), none (no special indication of active element) or underline (underline the active element). The default is underline on Windows, and dotbox elsewhere.
            background (str): The background color of the text input area.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            borderwidth (int): The thickness of the border around the listbox widget.
            cursor (str): The `mouse cursor`_ used for the widget. Names and values will vary according to OS.
            exportselection (bool): Include the selection in the X selection.
            font (str or Font): The font to use when drawing text inside the widget.
            foreground (str): The normal color of the input text.
            height (int): Specifies the desired height for the window, in lines. If zero or less, then the desired height for the window is made just large enough to hold all the elements in the listbox.
            justify (str): When there are multiple lines of text displayed in a widget, this option determines how the lines line up with each other. Must be one of left, center, or right. Left means that the lines' left edges all line up, center means that the lines' centers are aligned, and right means that the lines' right edges line up.
            listvariable (Variable): The variable of a list to be displayed inside the widget; if the variable value changes then the widget will automatically update itself to reflect the new value. If none is provided, it is created by default and can be accessed via the ``value`` property.
            selectmode (str): The style used to manipulate selection. One of `single`, `browse`, `multiple`, `extended`. Default is `extended`.
            state (str): Can be `normal` or `disabled`. If the listbox is disabled then items may not be inserted or deleted.
            takefocus (bool): Adds or removes the widget from focus traversal.
            width (int): The height of the window given in characters for the selected font.
            selectbackground (str): The background color of selected items.
            selectforeground (str): The text color of selected items.
            style (str): This option is NOT USED on the Text widget.
            values (List): A list of values to include in the list widget.
            xscrollcommmand (func): A reference to the ``.set`` method of a scrollbar widget; used to communicate with horizontal scrollbars.
            yscrollcommmand (func): A reference to the ``.set`` method of a scrollbar widget; used to communicate with vertical scrollbars.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        Widget.__init__(self, "Text", master=master, bootstyle=bootstyle, style=style)

        # setup bootstyle
        self.listvariable = listvariable or tkinter.Variable(value=values)
        self._background = background
        self._borderwidth = borderwidth
        self._font = font
        self._foreground = foreground
        self._focuscolor = ThemeColors.normalize(self.get_style_color(), self.colors.primary, self.colors)
        self._selectbackground = selectbackground
        self._selectforeground = selectforeground
        self._bsoptions = ["bootstyle"]
        self._settings = self._create_conf()

        tkinter.Listbox.__init__(
            self,
            master=master,
            activestyle=activestyle,
            cursor=cursor,
            exportselection=exportselection,
            height=height,
            justify=justify,
            listvariable=self.listvariable,
            selectmode=selectmode,
            state=state,
            takefocus=takefocus,
            width=width,
            xscrollcommand=xscrollcommand,
            yscrollcommand=yscrollcommand,
            **self._settings,
            **kw,
        )
        self.register_style()
        self.bind("<Leave>", self._on_leave)
        self.bind("<Enter>", self._on_enter)

        # TODO need to find a way to add more internal padding between border and text.
        # only add effects if the border is expected.
        if self._borderwidth > 0:
            self.bind("<FocusOut>", self._on_focusout)
            self.bind("<FocusIn>", self._on_focusin)

    # hover and press effects
    def _on_focusin(self, event):
        self.configure(highlightthickness=2, borderwidth=0, highlightbackground=self._focuscolor)

    def _on_focusout(self, event):
        self.configure(highlightthickness=1, borderwidth=1, highlightbackground=self.colors.border)

    def _on_enter(self, event):
        self.configure(highlightbackground=self._focuscolor)

    def _on_leave(self, event):
        self.configure(highlightthickness=1, borderwidth=1, highlightbackground=self.colors.border)

    def _create_conf(self):
        self._focuscolor = ThemeColors.normalize(self.get_style_color(), self.colors.primary, self.colors)
        settings = {
            "background": self._background or self.colors.inputbg,
            "borderwidth": self._borderwidth or 1,
            "font": self._font or DEFAULT_FONT,
            "foreground": self._foreground or self.colors.inputfg,
            "highlightbackground": self.colors.border,
            "highlightthickness": 1,
            "highlightcolor": self._focuscolor,
            "selectbackground": self._selectbackground or self.colors.selectbg,
            "selectforeground": self._selectforeground or self.colors.selectfg,
        }
        return settings

    def style_widget(self):
        self.customized = True
        self._widget_id = uuid4() if self._widget_id == None else self._widget_id
        self.style = f"{self._widget_id}"
        self._settings = self._create_conf()
        self.configure(cnf=self._settings)

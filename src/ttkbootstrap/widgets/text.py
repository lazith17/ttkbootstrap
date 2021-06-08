"""
    A **ttkbootstrap** styled **Text** widget.
    Created: 2021-06-07
"""

from src.ttkbootstrap.core.themes import DEFAULT_FONT, ThemeColors
from uuid import uuid4
import tkinter
from ttkbootstrap.widgets import Widget

class Text(Widget, tkinter.Text):
    """A Text widget handles multiple lines of text and can be edited and formatted; it is essentially a full text 
    editor in the window. 
    """
    def __init__(
        self,
        master=None,
        autoseparators=False,
        background=None,
        blockcursor=False,
        borderwidth=1,
        bootstyle="default",
        endline=None,
        exportselection=True,
        font=None,
        foreground=None,
        height=None,
        maxundo=None,
        selectbackground=None,
        selectforeground=None,
        spacing1=None,
        spacing2=None,
        spacing3=None,
        startline=None,
        state='normal',
        style=None,
        tabs=None,  # TODO default this to 4 spaces
        tabstyle='tabular',
        takefocus=True,
        undo=True,
        width=None,
        wrap='word',
        xscrollcommand=None,
        yscrollcommand=None,
        **kw
    ):
        """
        Args:
            master: The parent widget.
            autoseparators (bool): Automatically insert separators in the undo stack. Default is ``True``.
            background (str): The background color of the text input area.
            blockcursor (bool): Turn on a blinking cursor as a character-sized rectangular block. If ``False`` a think vertical line is used for the insertion cursor.
            borderwidth (int): The thickness of the border around the text widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            endline (int or str): The index of the last line of the underlying data that should be included in the data.
            exportselection (bool): Include the selection in the X selection.
            font (str or Font): [description]. The font to use when drawing text inside the widget.
            foreground (str): The normal color of the input text.
            height (int): The height of the window given in units of characters for the font selected. Must be at least one.
            maxundo (int): The maximum number of compound undo actions in the undo stack. A zero or negative imply an unlimited undo stack.
            selectbackground (str): The background color of selected items.
            selectforeground (str): The text color of selected items.
            spacing1 (int): Additional space `above` each text line.
            spacing2 (int): Additional space between lines that wrap.
            spacing3 (int): Additional space below each line.
            startline (int): The index of the first line of the underlying textual data that should be included in the widget.
            state (str): One of `normal` or `disabled`. If `disabled` then characters may not be inserted or deleted and no cursor will be displayed.
            style (str): This option is NOT USED on the Text widget.
            tabs (str): Specifies a set of tab stops for the window.
            tabstyle ([type]): Specifies how to interpret the relationship between the tab stops on a line and the tabs in the text of that line. Legal values include `tabular` or `wordprocessor`.
            takefocus (bool): Adds or removes the widget from focus traversal.
            undo (bool): Turn the undo mechanism off or on. Default is ``True``.
            width (int): The height of the window given in characters for the selected font.
            wrap (str): Specifies how to handle text that is too long to be displayed on a single line of text. Values can be `none`, `char` or `word`. If set to `none`, then the sentences will not overflow, but will be cut-off on the screen. The other options break at either the word or character.
            xscrollcommmand (func): A reference to the ``.set`` method of a scrollbar widget; used to communicate with horizontal scrollbars.
            xscrollcommmand (func): A reference to the ``.set`` method of a scrollbar widget; used to communicate with vertical scrollbars.
        """
        Widget.__init__(self, "Text", master=master, bootstyle=bootstyle, style=style)
 
        # setup bootstyle
        self._background = background
        self._borderwidth = borderwidth
        self._font = font
        self._foreground = foreground
        self._focuscolor = ThemeColors.normalize(self.get_style_color(), self.colors.primary, self.colors)
        self._selectbackground = selectbackground
        self._selectforeground = selectforeground
        self._bsoptions = ['bootstyle']
        self._settings = self._create_conf()

        tkinter.Text.__init__(self,
            master=master,
            autoseparators=autoseparators,
            blockcursor=blockcursor,
            endline=endline,
            exportselection=exportselection,
            height=height,
            maxundo=maxundo,
            spacing1=spacing1,
            spacing2=spacing2,
            spacing3=spacing3,
            startline=startline,
            state=state,
            tabs=tabs,
            tabstyle=tabstyle,
            takefocus=takefocus,
            undo=undo,
            width=width,
            wrap=wrap,
            xscrollcommand=xscrollcommand,
            yscrollcommand=yscrollcommand,
            **self._settings,
            **kw
        )
        self._customize_widget()
        self.bind("<Leave>", self._on_leave)
        self.bind("<Enter>", self._on_enter)
        
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
            'background': self._background or self.colors.inputbg,
            'borderwidth': self._borderwidth or 1,
            'font': self._font or DEFAULT_FONT,
            'foreground': self._foreground or self.colors.inputfg,
            'highlightbackground': self.colors.border,
            'highlightthickness': 1,
            'highlightcolor': self._focuscolor,
            'selectbackground': self._selectbackground or self.colors.selectbg,
            'selectforeground': self._selectforeground or self.colors.selectfg
        }
        return settings

    def _customize_widget(self):
        self.customized = True
        self._widget_id = uuid4() if self._widget_id == None else self._widget_id
        self.style = f"{self._widget_id}"
        self._settings = self._create_conf()
        self.configure(cnf=self._settings)


if __name__ == '__main__':
    import ttkbootstrap as ttk
    from itertools import cycle
    style = ttk.Style('cyborg')

    themes = cycle(style.themes)

    def change_theme():
        theme = next(themes)
        print(theme)
        style.theme_use(theme)
        print(text.colors)

    ttk.Entry().pack(padx=10, pady=10, fill='x')
    text = Text(bootstyle='info')
    text.pack(padx=10, pady=10)
    change = ttk.Button(text="Change Theme")
    change.pack(fill='x', padx=10, pady=10)
    change.configure(command=lambda: change_theme())
    text.mainloop()

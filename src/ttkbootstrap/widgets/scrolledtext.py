"""
    A **ttkbootstrap** styled **ScrolledText** widget.
    Created: 2021-06-08
"""
from ttkbootstrap.widgets import Text, Frame, Scrollbar 
from tkinter import Pack, Grid, Place

class ScrolledText(Text):
    """A ScrolledText widget feels like a text widget but also has a vertical scroll bar on its right.  
    Configuration options are passed to the Text widget. A Frame widget is inserted between the master and the text, 
    to hold the Scrollbar widget. Most methods calls are inherited from the Text widget; Pack, Grid and Place methods 
    are redirected to the Frame widget however.
    """
    def __init__(self, 
        master=None, 
        bootstyle="default",
        scrollbarshape='rounded',
        showarrows=True,
        padding=None,
        style=None,
        **kw
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            padding (Any): Sets the internal frame padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            scrollbarshape (str): Specifies the shape of the scrollbar; The default is `rounded`, but you may also pass an empty string or ``None`` to set the shape to squared.
            showarrows (bool): Specifies whether to show or hide the arrows. Default is ``True``.
            style ([type], optional): [description]. Defaults to None.
            **kw: Other options passed to the ``Text`` widget.
        """
        self.frame = Frame(master, bootstyle=bootstyle, padding=padding)
        self.vbar = Scrollbar(self.frame, showarrows=showarrows, bootstyle=f'{scrollbarshape} {bootstyle}', style=style)
        self.vbar.pack(side='right', fill='y')

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, bootstyle=bootstyle, **kw)
        self.pack(side='left', fill='both', expand='yes')
        self.vbar.configure(command=self.yview)

        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

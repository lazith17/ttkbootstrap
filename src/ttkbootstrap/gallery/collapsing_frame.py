"""
    Author: Israel Dryer
    Modified: 2021-06-08
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Application(ttk.Application):

    def __init__(self):
        super().__init__(title="Collapsing Frame", minsize=(400, 0))

        cf = CollapsingFrame(self)
        cf.pack(fill=BOTH)

        # option group 1
        group1 = ttk.Frame(cf, padding=10)
        for x in range(5):
            ttk.Checkbutton(group1, text=f"Option {x + 1}", default=True).pack(fill=X)
        cf.add(group1, title="Option Group 1")

        # option group 2
        group2 = ttk.Frame(cf, padding=10)
        for x in range(5):
            ttk.Checkbutton(group2, text=f"Option {x + 1}", default=True).pack(fill=X)
        cf.add(group2, title="Option Group 2", bootstyle=DANGER)

        # option group 3
        group3 = ttk.Frame(cf, padding=10)
        for x in range(5):
            ttk.Checkbutton(group3, text=f"Option {x + 1}", default=True).pack(fill=X)
        cf.add(group3, title="Option Group 3", bootstyle=SUCCESS)


class CollapsingFrame(ttk.Frame):
    """A collapsible frame widget that opens and closes with a button click."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        up_path = "src/ttkbootstrap/gallery/assets/icons8_double_up_24px.png"
        right_path = "src/ttkbootstrap/gallery/assets/icons8_double_right_24px.png"
        self.images = [
            ttk.PhotoImage(name="open", file=up_path),
            ttk.PhotoImage(name="closed", file=right_path)
        ]

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        Args:
            child (Frame): The parent widget.
            title (str): Header title.
            bootstyle (str): Style keywords.
        """
        if child.winfo_class() != "TFrame":  # must be a frame
            return
        frm = ttk.Frame(self, bootstyle=bootstyle)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        lbl = ttk.Label(frm, text=title, bootstyle = bootstyle + ' inverse')
        if kwargs.get("textvariable"):
            lbl.configure(textvariable=kwargs.get("textvariable"))
        lbl.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        btn = ttk.Button(frm, image="open", bootstyle=bootstyle)
        btn.configure(command=lambda c=child: self._toggle_open_close(child))
        btn.pack(side=RIGHT)

        # assign toggle button to child so that it's accesible when toggling (need to change image)
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky="news")

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """
        Open or close the section and change the toggle button image accordingly

        :param ttk.Frame child: the child element to add or remove from grid manager
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image="closed")
        else:
            child.grid()
            child.btn.configure(image="open")


if __name__ == "__main__":
    Application().run()

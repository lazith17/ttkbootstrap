"""
    Author: Israel Dryer
    Modified: 2021-06-07
"""
from random import randint
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Application(ttk.Application):
    def __init__(self):
        super().__init__(title="Equalizer")
        self.eq = Equalizer(self)
        self.eq.pack(fill=BOTH, expand=YES)


class Equalizer(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=20)
        controls = ["VOL", "31.25", "62.5", "125", "250", "500", "1K", "2K", "4K", "8K", "16K", "GAIN"]

        # create band widgets
        for c in controls:
            # starting random value
            value = randint(1, 99)
            self.setvar(c, value)

            # container
            frame = ttk.Frame(self, padding=5)
            frame.pack(side=LEFT, fill=Y, padx=10)

            # header
            ttk.Label(frame, text=c, anchor=CENTER, font=("Helvetica 10 bold")).pack(side=TOP, fill=X, pady=10)

            # slider
            scale = ttk.Scale(frame, orient=VERTICAL, from_=99, to=1, defaultvalue=value)
            scale.pack(fill=Y)
            scale.configure(command=lambda val, name=c: self.setvar(name, f"{float(val):.0f}"))

            # set slider style
            scale.configure(bootstyle=SUCCESS if c in ["VOL", "GAIN"] else INFO)

            # slider value label
            ttk.Label(frame, textvariable=c).pack(pady=10)


if __name__ == "__main__":
    Application().run()

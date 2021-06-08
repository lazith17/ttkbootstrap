"""
    Author: Israe Dryer
    Modified: 2021-06-08
    Adapted for ttkbootstrap from: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Desktop_Widget_Timer.py
"""
import ttkbootstrap as ttk


class Application(ttk.Window):
    def __init__(self):
        super().__init__(title="Timer")
        self.timer = TimerWidget(self)
        self.timer.pack(fill="both", expand="yes")


class TimerWidget(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # variables
        self.setvar('running', False)
        self.setvar('time-elapsed', 0)
        self.setvar('after-id', '')

        # timer label
        self.timer_lbl = ttk.Label(self, font="-size 32", anchor="center", text="00:00:00")
        self.timer_lbl.pack(side="top", fill="x", padx=60, pady=20)

        # control buttons
        self.toggle_btn = ttk.Button(self, text="Start", width=10, bootstyle="info", command=self.toggle)
        self.toggle_btn.pack(side="left", fill="x", expand="yes", padx=10, pady=10)

        self.reset_btn = ttk.Button(self, text="Reset", width=10, bootstyle="success", command=self.reset)
        self.reset_btn.pack(side="left", fill="x", expand="yes", pady=10)

        self.quit_btn = ttk.Button(self, text="Quit", width=10, bootstyle="danger", command=self.quit)
        self.quit_btn.pack(side="left", fill="x", expand="yes", padx=10, pady=10)

    def toggle(self):
        if self.getvar('running'):
            self.pause()
            self.setvar('running', False)
            self.toggle_btn.configure(text="Start", bootstyle="info")
        else:
            self.start()
            self.setvar('running', True)
            self.toggle_btn.configure(text="Pause", bootstyle="info outline")

    def pause(self):
        self.after_cancel(self.getvar('after-id'))

    def start(self):
        self.setvar('after-id', self.after(1, self.increment))

    def increment(self):
        current = self.getvar('time-elapsed') + 1
        self.setvar('time-elapsed', current)
        time_str = "{:02d}:{:02d}:{:02d}".format((current // 100) // 60, (current // 100) % 60, current % 100)
        self.timer_lbl.text = time_str
        self.setvar('after-id', self.after(100, self.increment))

    def reset(self):
        self.setvar('time-elapsed', 0)
        self.timer_lbl.text = "00:00:00"


if __name__ == "__main__":
    Application().mainloop()

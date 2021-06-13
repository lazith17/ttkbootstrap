"""
    Author: Israel Dryer
    Modified: 2021-06-07
"""
import ttkbootstrap as ttk


class Application(ttk.Application):
    def __init__(self):
        super().__init__(title="Calculator", theme="flatly")
        self.style.configure(".", font="TkFixedFont 16")
        self.calc = Calculator(self)
        self.calc.pack(fill=ttk.BOTH, expand=ttk.YES)


class Calculator(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=1)

        # number display
        self.display = ttk.Label(self, text=0, font="TkFixedFont 20", anchor=ttk.E)
        self.display.grid(row=0, column=0, columnspan=4, sticky=ttk.EW, pady=15, padx=10)

        # button layout
        button_matrix = [("%", "C", "CE", "/"), (7, 8, 9, "*"), (4, 5, 6, "-"), (1, 2, 3, "+"), ("±", 0, ".", "=")]

        # create buttons with various styling
        for i, row in enumerate(button_matrix):
            for j, lbl in enumerate(row):
                if isinstance(lbl, int):
                    btn = ttk.Button(self, text=lbl, width=2, bootstyle="primary")
                elif lbl == "=":
                    btn = ttk.Button(self, text=lbl, width=2, bootstyle="success")
                else:
                    btn = ttk.Button(self, text=lbl, width=2, bootstyle="secondary")
                btn.grid(row=i + 1, column=j, sticky=ttk.NSEW, padx=1, pady=1, ipadx=10, ipady=10)

                # bind button press
                btn.bind("<Button-1>", self.press_button)

        # variables used for collecting button input
        self.position_left = ""
        self.position_right = "0"
        self.position_is_left = True
        self.running_total = 0.0

    def press_button(self, event):
        value = event.widget.text

        if isinstance(value, int):
            if self.position_is_left:
                self.position_left = f"{self.position_left}{value}"
            else:
                self.position_right = str(value) if self.position_right == "0" else f"{self.position_right}{value}"
        elif value == ".":
            self.position_is_left = False
        elif value in ["/", "-", "+", "*"]:
            self.operator = value
            self.running_total = float(self.display.text)
            self.reset_variables()
        elif value == "=":
            operation = f"{self.running_total}{self.operator}{self.display.text}"
            result = eval(operation)
            self.display.text = result
            return
        elif value in ["CE", "C"]:
            self.reset_variables()
            self.operator = None
            self.running_total = 0
            return

        # update the number display
        self.display.text = ".".join([self.position_left, self.position_right])

    def reset_variables(self):
        self.display.text = 0
        self.position_is_left = True
        self.position_left = ""
        self.position_right = "0"


if __name__ == "__main__":
    Application().mainloop()

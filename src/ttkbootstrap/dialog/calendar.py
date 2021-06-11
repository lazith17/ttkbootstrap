"""
    A collection of **ttkbootstrap** themed calendar widgets.

    Created: 2021-06-10
    Author: Israel Dryer, israel.dryer@gmail.com
"""
import calendar
from datetime import datetime
from ttkbootstrap.dialog import Dialog
from ttkbootstrap.widgets import Frame
from ttkbootstrap import Window, Button, StringVar, IntVar, Label, Radiobutton


class DateChooserDialog(Dialog):
    """A custom **ttkbootstrap** widget that displays a calendar and allows the user to select a date which is returned
    as a ``datetime`` object for the date selected.

    The widget displays the current date by default unless a ``startdate`` is provided. The month can be changed by
    clicking on the chevrons to the right and left of the month-year title which is displayed on the top-center of
    the widget. A "left-click" will move the calendar `one month`. A "right-click" will move the calendar
    `one year`.

    A "right-click" on the `month-year` title will reset the calendar widget to the starting date.

    The starting weekday can be changed with the ``firstweekday`` parameter for geographies that do not start the
    week on `Sunday`, which is the widget default.

    The widget grabs focus and all screen events until released. If you want to cancel a date selection, you must
    click on the "X" button at the top-right hand corner of the widget.

    Styles can be applied to the widget by using the `TCalendar` style with the optional colors: 'primary',
    'secondary', 'success', 'info', 'warning', and 'danger'. By default, the `primary.TCalendar` style is applied.
    """

    def __init__(
        self,
        parent,
        title="Calendar",
        firstweekday=6,
        startdate=None,
        bootstyle="primary",
    ):
        """
        Args:
            parent (Widget): The parent widget; the popup is displayed to the bottom-right of the parent widget.
            startdate (datetime): The date to be in focus when the calendar is displayed. Current date is default.
            firstweekday (int): Specifies the first day of the week. ``0`` is Monday, ``6`` is Sunday (the default).
            style (str): The ``ttk`` style used to render the widget.
            **kw:
        """
        self.parent = parent
        self.bootstyle = bootstyle
        self.firstweekday = firstweekday
        self.startdate = startdate or datetime.today()
        self.date_selected = self.startdate
        self.date = self.startdate or self.date_selected
        self.calendar = calendar.Calendar(firstweekday=self.firstweekday)
        self.styles = {"calendar": "TCalendar"}
        self.generate_widget_styles()
        super().__init__(parent, title=title)

    def body(self, master):
        self.calendar_frame = Frame(master, padding=0, borderwidth=1, relief="raised", style=self.styles["frame"])
        self.title_frame = Frame(self.calendar_frame, style=self.styles["frame"])
        self.week_frame = Frame(self.calendar_frame)
        self.day_frame = None

        self.title_var = StringVar(value=f'{self.date.strftime("%B %Y")}')
        self.date_var = IntVar()

        # remove all padding and expand the toplevel main body
        self.main_body.configure(padding=0)
        self.main_body.pack_configure(padx=0, pady=0, fill="both", expand="yes")

        # setup the calendar widgets
        self.setup()
        self.grab_set()

    def button_box(self, master):
        pass

    def draw_calendar(self):
        """Create the days of the week elements"""
        self.title_var.set(f'{self.date.strftime("%B %Y")}')
        self.monthdays = self.calendar.monthdayscalendar(self.date.year, self.date.month)
        self.monthdates = self.calendar.monthdatescalendar(self.date.year, self.date.month)

        self.day_frame = Frame(self.calendar_frame)
        self.day_frame.pack(fill="both", expand="yes")
        # self.set_geometry()
        self.minsize(226, 255)

        # calendar days
        for row, wk in enumerate(self.monthdays):
            for col, day in enumerate(wk):
                self.day_frame.columnconfigure(col, weight=1)
                if day == 0:
                    lbl = Label(self.day_frame, text=self.monthdates[row][col].day, anchor="center")
                    lbl.configure(style="secondary.TLabel", padding=(0, 0, 0, 10))
                    lbl.grid(row=row, column=col, sticky="nswe")
                else:
                    if all(
                        [
                            day == self.date_selected.day,
                            self.date.month == self.date_selected.month,
                            self.date.year == self.date_selected.year,
                        ]
                    ):
                        day_style = self.styles["selected"]
                    else:
                        day_style = self.styles["calendar"]

                    rb = Radiobutton(self.day_frame, variable=self.date_var, value=day, text=day, style=day_style)
                    rb.configure(padding=(0, 0, 0, 10), command=lambda x=row, y=col: self.on_date_selected([x, y]))
                    rb.grid(row=row, column=col, sticky="nswe")

    def draw_titlebar(self):
        """Create the title bar"""
        # previous month button
        self.btn_prev = Button(self.title_frame, text="«", style=self.styles["chevron"], command=self.on_prev_month)
        self.btn_prev.bind("<Button-3>", self.on_prev_year, "+")
        self.btn_prev.pack(side="left")

        # month and year title
        self.title_label = Label(
            self.title_frame,
            textvariable=self.title_var,
            anchor="center",
        )
        self.title_label.configure(style=self.styles["title"], font="helvetica 11")
        self.title_label.pack(side="left", fill="x", expand="yes")
        self.title_label.bind("<Button-1>", self.on_reset_date)

        # next month button
        self.btn_next = Button(self.title_frame, text="»", command=self.on_next_month, style=self.styles["chevron"])
        self.btn_next.bind("<Button-3>", self.on_next_year, "+")
        self.btn_next.pack(side="left")

        # days of the week header
        for wd in self.weekday_header():
            wd_lbl = Label(
                self.week_frame, text=wd, anchor="center", padding=(0, 5, 0, 10), bootstyle="secondary inverse"
            )
            wd_lbl.pack(side="left", fill="x", expand="yes")

    def generate_widget_styles(self):
        """Generate all the styles required for this widget from the ``base_style``."""
        self.styles.update(
            {
                "calendar": "TCalendar",
                "chevron": f"chevron.{self.bootstyle}.TButton",
                "title": f"title.{self.bootstyle}.Inverse.TLabel",
                "frame": f"{self.bootstyle}.TFrame",
                "selected": f"{self.bootstyle}.Toolbutton",
            }
        )

    def on_date_selected(self, index):
        """Callback for selecting a date.

        Assign the selected date to the ``date_selected`` property and then destroy the toplevel widget.

        Args:
            index (Tuple[int]): a tuple containing the row and column index of the date selected to be found in the
                ``monthdates`` property.
        """
        row, col = index
        self.result = self.monthdates[row][col]
        self.destroy()

    def on_next_month(self):
        """Callback for changing calendar to next month"""
        year, month = calendar._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self.day_frame.destroy()
        self.draw_calendar()

    def on_next_year(self, *args):
        """Callback for changing calendar to next year"""
        year = self.date.year + 1
        self.date = datetime(year=year, month=self.date.month, day=1).date()
        self.day_frame.destroy()
        self.draw_calendar()

    def on_prev_month(self):
        """Callback for changing calendar to previous month"""
        year, month = calendar._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self.day_frame.destroy()
        self.draw_calendar()

    def on_prev_year(self, *args):
        """Callback for changing calendar to previous year"""
        year = self.date.year - 1
        self.date = datetime(year=year, month=self.date.month, day=1).date()
        self.day_frame.destroy()
        self.draw_calendar()

    def on_reset_date(self, *args):
        """Callback for clicking the month-year title; reset the date to the start date"""
        self.date = self.startdate
        self.day_frame.destroy()
        self.draw_calendar()

    def set_geometry(self):
        """Adjust the window size based on the number of weeks in the month"""
        w = 226
        h = 255 if len(self.monthdates) == 5 else 285  # this needs to be adjusted if I change the font size.
        if self.parent:
            xpos = self.parent.winfo_rootx() + self.parent.winfo_width()
            ypos = self.parent.winfo_rooty() + self.parent.winfo_height()
            self.geometry(f"{w}x{h}+{xpos}+{ypos}")
        else:
            xpos = self.winfo_screenwidth() // 2 - w
            ypos = self.winfo_screenheight() // 2 - h
            self.geometry(f"{w}x{h}+{xpos}+{ypos}")

    def setup(self):
        """Setup the calendar widget"""
        self.calendar_frame.pack(fill="both", expand="yes")
        self.title_frame.pack(fill="x")
        self.week_frame.pack(fill="x")

        # setup the top level window
        self.update_idletasks()  # actualize the geometry
        self.draw_titlebar()
        self.draw_calendar()

    def weekday_header(self):
        """Creates and returns a list of weekdays to be used as a header in the calendar based on the firstweekday. The
        order of the weekdays is based on the ``firstweekday`` property.

        Returns:
            List: a list of weekday headers
        """
        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        return weekdays[self.firstweekday :] + weekdays[: self.firstweekday]


if __name__ == "__main__":

    root = Window()

    d = DateChooserDialog(parent=root)
    print(d.result)

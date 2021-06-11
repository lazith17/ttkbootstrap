import calendar
from abc import abstractmethod
from datetime import datetime
from ttkbootstrap import Frame, Button, PhotoImage, Label, Radiobutton
from ttkbootstrap import StringVar, IntVar
from ttkbootstrap.core import DialogImages, Toplevel
from ttkbootstrap.core.themes import ThemeColors


class Dialog(Toplevel):
    """A class to open dialogs.

    This class is intended as a base class for custom dialogs. See ``Toplevel`` for additional keyword options.
    """

    def __init__(self, parent=None, title=None, **kw):
        """Initialize a dialog

        Args:
            parent: The parent widget.
            title (str): The dialog title.
        """
        Toplevel.__init__(self, parent=parent, **kw)
        self.withdraw()
        self.parent = parent or self.master
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.result = None

        if self.platform == "x11":
            self.attributes("-type", "dialog")

        # add body
        self.main_body = Frame(self)
        self.main_body.pack(padx=5, pady=5)
        self.themedcolor = self.main_body.themed_color

        # set focus
        self.initial_focus = self.body(self.main_body)
        if not self.initial_focus:
            self.initial_focus = self

        # add buttons
        self.button_box(self)

        ## get the geometry of the master widget
        self.update_idletasks()
        if self.parent.winfo_ismapped():
            m_width = self.parent.winfo_width()
            m_height = self.parent.winfo_height()
            m_x = self.parent.winfo_rootx()
            m_y = self.parent.winfo_rooty()
        else:
            m_width = self.parent.winfo_screenwidth()
            m_height = self.parent.winfo_screenheight()
            m_x = m_y = 0

        # get the geometry of the toplevel widget
        w_width = self.winfo_reqwidth()
        w_height = self.winfo_reqheight()
        x = int(min(max(m_x + (m_width - w_width) * 0.5, 0), self.parent.winfo_screenwidth()))
        y = int(min(max(m_y + (m_height - w_height) * 0.3, 0), self.parent.winfo_screenheight()))
        self.geometry(f"+{x}+{y}")

        # show window
        self.update_idletasks()
        self.deiconify()
        self.initial_focus.focus_set()
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    @abstractmethod
    def body(self, master):
        """Create a dialog body"""
        pass

    def button_box(self, master):
        """Add standard button box.

        Override if you do not want the standard buttons.
        """
        box = Frame(self)
        Button(box, text="OK", width=10, command=self.ok).pack(side="right", padx=5, pady=5)
        Button(box, text="Cancel", width=10, command=self.cancel).pack(side="right", padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def destroy(self):
        """Destroy the window"""
        self.initial_focus = None
        Toplevel.destroy(self)

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self):
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    @abstractmethod
    def validate(self):
        """Validate the data

        This method is called automatically to validate the data `before` the dialog is destroyed. By default, it
        always validates OK.
        """
        return True

    @abstractmethod
    def apply(self):
        """Process the data

        This method is called automatically to process the data, `after` the dialog is destroyed. By default, it does
        nothing.
        """
        pass


class SimpleDialog(Dialog):
    """Pops up a window message box and waits for user input"""

    def __init__(self, parent, title, message, buttons=[], icon=None, default=None, cancel=None, **kw):
        """
        Args:
            master: The parent widget.
            title (str): Text to appear in the title bar.
            message (str): Text to appear in the widget.
            buttons (List[str]): A list of button names to appear below the message text.
            icon (str): The name of the icon to appear on the left side of the message text. Legal values include: `info`, `warning`, `question`, `error`.
            default (int): The index of the default button from the ``buttons`` option. The ``<<Return>>`` event is bound to the default button.
        """
        self.action = None
        self._buttons = buttons
        self._cancel = cancel
        self._default = default
        self._icon = icon
        self._message = message

        super().__init__(parent, title=title, **kw)
        if self._default:
            self.bind("<Return>", self.ok)

    def body(self, master):
        """Create a message body; override superclass method"""
        # message container
        self.msg_frame = Frame(master, padding=15)
        self.msg_frame.pack(side="top", fill="x", expand="yes")

        # message icon
        img = DialogImages.__dict__.get(self._icon)
        if img:
            self.icon = PhotoImage(data=img)
            self.icon_lbl = Label(self.msg_frame, image=self.icon)
            self.icon_lbl.pack(side="left", padx=5, pady=5)

        # message text
        self.colors = self.msg_frame.colors
        self.message = Label(self.msg_frame, text=self._message, justify="left", wraplength=350)
        self.message.pack(padx=5, pady=5)

    def button_box(self, master):
        """Create a button box; override superclass method"""
        btn_bg_color = ThemeColors.update_hsv(self.colors.bg, vd=-0.2)
        self.btn_frame = Frame(master, padding=(10, 5), background=btn_bg_color)
        self.btn_frame.pack(fill="x")
        for index, btn in enumerate(self._buttons):
            btn_text = self._buttons[index]
            command = lambda x=index: self.done(x if index != self._cancel else None)
            btn = Button(self.btn_frame, text=btn_text, command=command)
            btn.pack(side="right", padx=2, pady=2)

    def done(self, action):
        """Collect the action number when an action is completed, and close the window."""
        self.action = action
        self.cancel()


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
        parent=None,
        title="Calendar",
        firstweekday=6,
        startdate=None,
        bootstyle="primary",
        **kw
    ):
        """
        Args:
            parent: The parent widget.
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
        self._generate_widget_styles()
        super().__init__(parent, title=title, minsize=(226, 225), **kw)

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
        self._setup()

        self.grab_set()

    def button_box(self, master):
        # overriding method to prevent default buttons from drawing...
        # consider adding a `-hidebuttons` option to the base class.
        pass

    def on_date_selected(self, index):
        """Callback for selecting a date.

        Assign the selected date to the ``date_selected`` property and then destroy the toplevel widget.

        Args:
            index (Tuple[int]): a tuple containing the row and column index of the date selected to be found in the
                ``monthdates`` property.
        """
        row, col = index
        self.date_selected = self.monthdates[row][col]
        self.destroy()

    def on_next_month(self):
        """Callback for changing calendar to next month"""
        year, month = calendar._nextmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self.day_frame.destroy()
        self._draw_calendar()

    def on_next_year(self, *args):
        """Callback for changing calendar to next year"""
        year = self.date.year + 1
        self.date = datetime(year=year, month=self.date.month, day=1).date()
        self.day_frame.destroy()
        self._draw_calendar()

    def on_prev_month(self):
        """Callback for changing calendar to previous month"""
        year, month = calendar._prevmonth(self.date.year, self.date.month)
        self.date = datetime(year=year, month=month, day=1).date()
        self.day_frame.destroy()
        self._draw_calendar()

    def on_prev_year(self, *args):
        """Callback for changing calendar to previous year"""
        year = self.date.year - 1
        self.date = datetime(year=year, month=self.date.month, day=1).date()
        self.day_frame.destroy()
        self._draw_calendar()

    def on_reset_date(self, *args):
        """Callback for clicking the month-year title; reset the date to the start date"""
        self.date = self.startdate
        self.day_frame.destroy()
        self._draw_calendar()

    def _draw_calendar(self):
        """Create the days of the week elements"""
        self.title_var.set(f'{self.date.strftime("%B %Y")}')
        self.monthdays = self.calendar.monthdayscalendar(self.date.year, self.date.month)
        self.monthdates = self.calendar.monthdatescalendar(self.date.year, self.date.month)

        self.day_frame = Frame(self.calendar_frame)
        self.day_frame.pack(fill="both", expand="yes")

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

    def _draw_titlebar(self):
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
        for wd in self._weekday_header():
            wd_lbl = Label(
                self.week_frame, text=wd, anchor="center", padding=(0, 5, 0, 10), bootstyle="secondary inverse"
            )
            wd_lbl.pack(side="left", fill="x", expand="yes")

    def _generate_widget_styles(self):
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

    def _setup(self):
        """Setup the calendar widget"""
        self.calendar_frame.pack(fill="both", expand="yes")
        self.title_frame.pack(fill="x")
        self.week_frame.pack(fill="x")

        # setup the top level window
        self.update_idletasks()  # actualize the geometry
        self._draw_titlebar()
        self._draw_calendar()

    def _weekday_header(self):
        """Creates and returns a list of weekdays to be used as a header in the calendar based on the firstweekday. The
        order of the weekdays is based on the ``firstweekday`` property.

        Returns:
            List: a list of weekday headers
        """
        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        return weekdays[self.firstweekday :] + weekdays[: self.firstweekday]

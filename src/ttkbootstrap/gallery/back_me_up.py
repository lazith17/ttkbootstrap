"""
    Author: Israel Dryer
    Modified: 2021-06-13
    Adapted for ttkbootstrap from: http://www.leo-backup.com/screenshots.shtml
"""
from pathlib import Path
from datetime import datetime
from random import choices
import ttkbootstrap as ttk
from ttkbootstrap.dialog import messagebox, filedialog
from ttkbootstrap.constants import *

# TODO fix the "unknown color name error"


class Application(ttk.Application):
    def __init__(self):
        super().__init__(title="Back Me Up")
        self.bmu = BackMeUp(self, padding=2)
        self.bmu.pack(fill=BOTH, expand=YES)


class BackMeUp(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        filepath = Path("./src/ttkbootstrap/gallery/assets")

        # images
        self.img_properties_d = ttk.PhotoImage(name="prop-dark", file=filepath / "icons8_settings_24px.png")
        self.img_properties_l = ttk.PhotoImage(name="prop-light", file=filepath / "icons8_settings_24px_2.png")
        self.img_addtobackup_d = ttk.PhotoImage(name="add-backup-dark", file=filepath / "icons8_add_folder_24px.png")
        self.img_addtobackup_l = ttk.PhotoImage(name="add-backup-light", file=filepath / "icons8_add_book_24px.png")
        self.img_stopbackup_d = ttk.PhotoImage(name="stop-backup-dark", file=filepath / "icons8_cancel_24px.png")
        self.img_stopbackup_l = ttk.PhotoImage(name="stop-backup-light", file=filepath / "icons8_cancel_24px_1.png")
        self.img_play = ttk.PhotoImage(name="play", file=filepath / "icons8_play_24px_1.png")
        self.img_refresh = ttk.PhotoImage(name="refresh", file=filepath / "icons8_refresh_24px_1.png")
        self.img_stop_d = ttk.PhotoImage(name="stop-dark", file=filepath / "icons8_stop_24px.png")
        self.img_stop_l = ttk.PhotoImage(name="stop-light", file=filepath / "icons8_stop_24px_1.png")
        self.img_opened_folder = ttk.PhotoImage(name="opened-folder", file=filepath / "icons8_opened_folder_24px.png")
        self.img_logo = ttk.PhotoImage(name="logo", file=filepath / "backup.png")

        # ----- buttonbar
        buttonbar = ttk.Frame(self, bootstyle=PRIMARY)
        buttonbar.pack(fill=X, pady=1, side=TOP)

        ## new backup
        bb_new_backup_btn = ttk.Button(buttonbar, text="New backup set", image="add-backup-light", compound=LEFT)
        bb_new_backup_btn.configure(command=lambda: messagebox.showinfo(message="Adding new backup"))
        bb_new_backup_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        ## backup
        bb_backup_btn = ttk.Button(buttonbar, text="Backup", image="play", compound=LEFT)
        bb_backup_btn.configure(command=lambda: messagebox.showinfo(message="Backing up..."))
        bb_backup_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## refresh
        bb_refresh_btn = ttk.Button(buttonbar, text="Refresh", image="refresh", compound=LEFT)
        bb_refresh_btn.configure(command=lambda: messagebox.showinfo(message="Refreshing..."))
        bb_refresh_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## stop
        bb_stop_btn = ttk.Button(buttonbar, text="Stop", image="stop-light", compound=LEFT)
        bb_stop_btn.configure(command=lambda: messagebox.showwarning(message="Stopping backup."))
        bb_stop_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        ## settings
        bb_settings_btn = ttk.Button(buttonbar, text="Settings", image="prop-light", compound=LEFT)
        bb_settings_btn.configure(command=lambda: messagebox.showinfo(message="Changing settings"))
        bb_settings_btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

        # ----- left panel
        left_panel = ttk.Frame(self, background=self.colors.inputbg)
        left_panel.pack(side=LEFT, fill="y")

        ## ----- backup summary (collapsible)
        bus_cf = CollapsingFrame(left_panel)
        bus_cf.pack(fill=X, pady=1)

        ## container
        bus_frm = ttk.Frame(bus_cf, padding=5)
        bus_frm.columnconfigure(1, weight=1)
        bus_cf.add(bus_frm, title="Backup Summary", bootstyle=SECONDARY)

        ## destination
        ttk.Label(bus_frm, text="Destination:").grid(row=0, column=0, sticky=W, pady=2)
        ttk.Label(bus_frm, text="d:/text/").grid(row=0, column=1, sticky=EW, padx=5, pady=2)

        ## last run
        ttk.Label(bus_frm, text="Last Run:").grid(row=1, column=0, sticky=W, pady=2)
        ttk.Label(bus_frm, text="14.06.2021 19:34:43").grid(row=1, column=1, sticky=EW, padx=5, pady=2)

        ## files Identical
        ttk.Label(bus_frm, text="Files Identical:").grid(row=2, column=0, sticky=W, pady=2)
        ttk.Label(bus_frm, text="15%").grid(row=2, column=1, sticky=EW, padx=5, pady=2)

        ## section separator
        bus_sep = ttk.Separator(bus_frm, bootstyle=SECONDARY)
        bus_sep.grid(row=3, column=0, columnspan=2, pady=10, sticky=EW)

        ## properties button
        bus_prop_btn = ttk.Button(bus_frm, text="Properties", image="prop-dark", compound=LEFT, bootstyle=LINK)
        bus_prop_btn.configure(command=lambda: messagebox.showinfo(parent=self, message="Changing properties"))
        bus_prop_btn.grid(row=4, column=0, columnspan=2, sticky=W)

        ## add to backup button
        bus_add_btn = ttk.Button(bus_frm, text="Add to backup", image="add-backup-dark", compound=LEFT, bootstyle=LINK)
        bus_add_btn.configure(command=lambda: messagebox.showinfo(parent=self, message="Adding to backup"))
        bus_add_btn.grid(row=5, column=0, columnspan=2, sticky=W)

        # ----- backup status (collapsible)
        status_cf = CollapsingFrame(left_panel)
        status_cf.pack(fill=X, pady=1)

        ## container
        status_frm = ttk.Frame(status_cf, padding=10)
        status_frm.columnconfigure(1, weight=1)
        status_cf.add(status_frm, title="Backup Status", bootstyle=SECONDARY)

        ## progress message
        status_prog_lbl = ttk.Label(status_frm, textvariable="Backing up...", font="Helvetica 10 bold")
        status_prog_lbl.grid(row=0, column=0, columnspan=2, sticky=W)

        ## progress bar
        status_prog = ttk.Progressbar(status_frm, value=71, bootstyle=INFO + STRIPED)
        status_prog.grid(row=1, column=0, columnspan=2, sticky=EW, pady=(10, 5))

        ## time started
        ttk.Label(status_frm, text="Started at: 14.06.2021 19:34:56").grid(
            row=2, column=0, columnspan=2, sticky=EW, pady=2
        )

        ## time elapsed
        ttk.Label(status_frm, text="Elapsed: 1 sec").grid(row=3, column=0, columnspan=2, sticky=EW, pady=2)

        ## time remaining
        ttk.Label(status_frm, text="Left: 0 sec").grid(row=4, column=0, columnspan=2, sticky=EW, pady=2)

        ## section separator
        status_sep = ttk.Separator(status_frm, bootstyle=SECONDARY)
        status_sep.grid(row=5, column=0, columnspan=2, pady=10, sticky=EW)

        ## stop button
        status_stop_btn = ttk.Button(status_frm, text="Stop", image="stop-backup-dark", compound=LEFT, bootstyle=LINK)
        status_stop_btn.configure(command=lambda: messagebox.showwarning(message="Stopping backup"))
        status_stop_btn.grid(row=6, column=0, columnspan=2, sticky=W)

        ## section separator
        status_sep = ttk.Separator(status_frm, bootstyle=SECONDARY)
        status_sep.grid(row=7, column=0, columnspan=2, pady=10, sticky=EW)

        # current file message
        ttk.Label(status_frm, text="Uploading file: d:/test/settings.txt").grid(
            row=8, column=0, columnspan=2, pady=2, sticky=EW
        )

        # logo
        ttk.Label(left_panel, image="logo", background=self.colors.inputbg).pack(side=BOTTOM)

        # ---- right panel
        right_panel = ttk.Frame(self, padding=(2, 1))
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        ## file input
        browse_frm = ttk.Frame(right_panel)
        browse_frm.pack(side=TOP, fill=X, padx=2, pady=1)
        file_entry = ttk.Entry(browse_frm, textvariable="folder-path")
        file_entry.pack(side=LEFT, fill=X, expand=YES)
        open_btn = ttk.Button(browse_frm, image="opened-folder", bootstyle=SECONDARY + LINK, command=self.get_directory)
        open_btn.pack(side=RIGHT)

        ## Treeview
        tv = ttk.Treeview(right_panel, show=HEADINGS)
        tv["columns"] = ("name", "state", "last-modified", "last-run-time", "size")
        tv.column("name", width=150, stretch=True)
        for col in ["last-modified", "last-run-time", "size"]:
            tv.column(col, stretch=False)
        for col in tv["columns"]:
            tv.heading(col, text=col.title(), anchor=W)
        tv.pack(fill=X, pady=1)

        ## scrolling text output
        scroll_cf = CollapsingFrame(right_panel)
        scroll_cf.pack(fill=BOTH, pady=1)
        output_container = ttk.Frame(scroll_cf, padding=1)
        st = ttk.ScrolledText(output_container, bootstyle=ROUNDED)
        st.pack(fill=BOTH, expand=YES)
        scroll_cf.add(output_container, title="Log: Backing up... [Uploading file: D:/sample_file_35.txt]")

        # ----- seed with some sample data -----------------------------------------------------------------------------

        ## starting sample directory
        file_entry.insert(END, "D:/text/myfiles/top-secret/samples/")

        ## treeview and backup logs
        for x in range(20, 35):
            result = choices(["Backup Up", "Missed in Destination"])[0]
            st.insert(END, f"19:34:{x}\t\t Uploading file: D:/text/myfiles/top-secret/samples/sample_file_{x}.txt\n")
            st.insert(END, f"19:34:{x}\t\t Upload {result}.\n")
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            tv.insert("", END, x, values=(f"sample_file_{x}.txt", result, timestamp, timestamp, f"{int(x // 3)} MB"))
        tv.selection_set(20)

    def get_directory(self):
        """Open dialogue to get directory and update directory variable"""
        self.update_idletasks()
        d = filedialog.askdirectory()
        if d:
            self.setvar("folder-path", d)


class CollapsingFrame(ttk.Frame):
    """
    A collapsible frame widget that opens and closes with a button click.
    """

    def __init__(self, *args, **kwargs):
        filepath = Path("./src/ttkbootstrap/gallery/assets")

        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        self.images = [
            ttk.PhotoImage(name="open", file=filepath / "icons8_double_up_24px.png"),
            ttk.PhotoImage(name="closed", file=filepath / "icons8_double_right_24px.png"),
        ]

    def add(self, child, title="", bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        :param ttk.Frame child: the child frame to add to the widget
        :param str title: the title appearing on the collapsible section header
        :param str style: the ttk style to apply to the collapsible section header
        """
        if child.winfo_class() != "TFrame":  # must be a frame
            return
        frm = ttk.Frame(self, bootstyle=bootstyle)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        lbl = ttk.Label(frm, text=title, bootstyle=bootstyle + INVERSE)
        if kwargs.get("textvariable"):
            lbl.configure(textvariable=kwargs.get("textvariable"))
        lbl.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        btn = ttk.Button(frm, image="open", bootstyle=bootstyle, command=lambda c=child: self._toggle_open_close(child))
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

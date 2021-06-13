"""
    Author: Israel Dryer
    Modified: 2021-06-08
    Adapted from: https://images.idgesg.net/images/article/2018/08/cw_win10_utilities_ss_02-100769136-orig.jpg
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pathlib import Path

class Application(ttk.Application):
    def __init__(self):
        super().__init__(title="PC Cleaner", theme="journal", resizeable=(False, False))
        self.cleaner = Cleaner(self)
        self.cleaner.pack(fill=BOTH, expand=YES)

class Cleaner(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # application images
        im_path = Path("src/ttkbootstrap/gallery/assets/")
        self.logo_img = ttk.PhotoImage(name="logo", file=im_path / "icons8_broom_64px_1.png")
        self.brush_img = ttk.PhotoImage(name="cleaner", file=im_path / "icons8_broom_64px.png")
        self.registry_img = ttk.PhotoImage(name="registry", file=im_path / "icons8_registry_editor_64px.png")
        self.tools_img = ttk.PhotoImage(name="tools", file=im_path / "icons8_wrench_64px.png")
        self.options_img = ttk.PhotoImage(name="options", file=im_path / "icons8_settings_64px.png")
        self.privacy_img = ttk.PhotoImage(name="privacy", file=im_path / "icons8_spy_80px.png")
        self.junk_img = ttk.PhotoImage(name="junk", file=im_path / "icons8_trash_can_80px.png")
        self.protect_img = ttk.PhotoImage(name="protect", file=im_path / "icons8_protect_40px.png")

        # header
        header_frame = ttk.Frame(self, padding=20, bootstyle=SECONDARY)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=EW)
        ttk.Label(header_frame, image="logo", background=SECONDARY).pack(side=LEFT)
        logo_text = ttk.Label(header_frame, text="pc cleaner", font=("TkDefaultFixed", 30))
        logo_text.configure(background=SECONDARY, foreground=INFO)
        logo_text.pack(side=LEFT, padx=10)

        # action buttons
        action_frame = ttk.Frame(self)
        action_frame.grid(row=1, column=0, sticky=NSEW)
        cleaner_btn = ttk.Button(action_frame, image="cleaner", text="cleaner", compound=TOP, bootstyle=INFO)
        cleaner_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)
        registry_btn = ttk.Button(action_frame, image="registry", text="registry", compound=TOP, bootstyle=INFO)
        registry_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)
        tools_btn = ttk.Button(action_frame, image="tools", text="tools", compound=TOP, bootstyle=INFO)
        tools_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)
        options_btn = ttk.Button(action_frame, image="options", text="options", compound=TOP, bootstyle=INFO)
        options_btn.pack(side=TOP, fill=BOTH, ipadx=10, ipady=10)

        # option notebook
        notebook = ttk.Notebook(self)
        notebook.grid(row=1, column=1, sticky=NSEW, pady=(25, 0))

        ## windows tab
        windows_tab = ttk.Frame(notebook, padding=(10, 0, 0, 0))
        wt_scrollbar = ttk.Scrollbar(windows_tab, bootstyle=ROUNDED + INFO)
        wt_scrollbar.pack(side=RIGHT, fill=Y)
        wt_canvas = ttk.Canvas(windows_tab, border=0, highlightthickness=0, yscrollcommand=wt_scrollbar.set)
        wt_canvas.pack(side=LEFT, fill=BOTH)

        ### adjust the scrollregion when the size of the canvas changes
        wt_canvas.bind("<Configure>", lambda e: wt_canvas.configure(scrollregion=wt_canvas.bbox(ALL)))
        wt_scrollbar.configure(command=wt_canvas.yview)
        scroll_frame = ttk.Frame(wt_canvas)
        wt_canvas.create_window((0, 0), window=scroll_frame, anchor=NW)

        radio_options = [
            "Internet Cache",
            "Internet History",
            "Cookies",
            "Download History",
            "Last Download Location",
            "Session",
            "Set Aside Tabs",
            "Recently Typed URLs",
            "Saved Form Information",
            "Saved Password",
        ]

        edge = ttk.Labelframe(scroll_frame, text="Microsoft Edge", padding=(20, 5))
        edge.pack(fill=BOTH, pady=(10, 0))

        explorer = ttk.Labelframe(scroll_frame, text="Internet Explorer", padding=(20, 5))
        explorer.pack(fill=BOTH, pady=10)

        ### add radio buttons to each label frame section
        for section in [edge, explorer]:
            for opt in radio_options:
                cb = ttk.Checkbutton(section, text=opt, default=True)
                cb.pack(side=TOP, pady=2, fill=X)
        notebook.add(windows_tab, text="windows")

        ## empty tab for looks
        notebook.add(ttk.Frame(notebook), text="applications")

        # results frame
        results_frame = ttk.Frame(self)
        results_frame.grid(row=1, column=2, sticky=NSEW)

        ## progressbar with text indicator
        pb_frame = ttk.Frame(results_frame, padding=(0, 10, 10, 10))
        pb_frame.pack(side=TOP, fill=X, expand=YES)
        pb = ttk.Progressbar(pb_frame, bootstyle=STRIPED + SUCCESS, value=78)
        pb.pack(side=LEFT, fill=X, expand=YES, padx=(15, 10))
        ttk.Label(pb_frame, text="%").pack(side=RIGHT)
        ttk.Label(pb_frame, textvariable=pb.variable).pack(side=RIGHT)

        ## result cards
        cards_frame = ttk.Frame(results_frame, name="cards-frame", bootstyle=SECONDARY)
        cards_frame.pack(fill=BOTH, expand=YES)

        ### privacy card
        priv_card = ttk.Frame(cards_frame, padding=1, bootstyle=SECONDARY)
        priv_card.pack(side=LEFT, fill=BOTH, padx=(10, 5), pady=10)
        priv_container = ttk.Frame(priv_card, padding=40)
        priv_container.pack(fill=BOTH, expand=YES)
        priv_lbl = ttk.Label(priv_container, image="privacy", text="PRIVACY", compound=TOP, anchor=CENTER)
        priv_lbl.pack(fill=BOTH, padx=20, pady=(40, 0))
        ttk.Label(priv_container, text="6025 tracking file(s) removed", bootstyle='primary').pack(pady=(0, 20))

        ### junk card
        junk_card = ttk.Frame(cards_frame, padding=1, style="secondary.TButton")
        junk_card.pack(side=LEFT, fill=BOTH, padx=(5, 10), pady=10)
        junk_container = ttk.Frame(junk_card, padding=40)
        junk_container.pack(fill=BOTH, expand=YES)
        junk_lbl = ttk.Label(junk_container, image="junk", text="PRIVACY", compound=TOP, anchor=CENTER)
        junk_lbl.pack(fill=BOTH, padx=20, pady=(40, 0))
        junk_info = ttk.Label(junk_container, bootstyle='primary', justify=CENTER)
        junk_info.text="1,150 MB of unneccesary file(s)\nremoved"
        junk_info.pack(pady=(0, 20))

        ## user notification
        note_frame = ttk.Frame(results_frame, bootstyle=SECONDARY, padding=40)
        note_frame.pack(fill=BOTH)
        note_msg = ttk.Label(
            note_frame,
            text="We recommend that you better protect your data",
            anchor=CENTER,
            background=SECONDARY,
            foreground=INFO,
            font=("Helvetica", 12, "italic"),
        )
        note_msg.pack(fill=BOTH)


if __name__ == "__main__":
    Application().run()

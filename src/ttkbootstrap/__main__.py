"""
Author: Israel Dryer
License: MIT
Copyright (c) 2021 Israel Dryer
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# for taking screenshots
from PIL import ImageGrab


class Demo(ttk.Application):
    """An application class for demonstrating styles"""

    def __init__(self):
        super().__init__(title="TTK Bootstrap", theme="solar", size=(500, 695))
        self.style.build_all_themes()
        self.theme_name = ttk.StringVar()
        self.theme_name.set(self.style.current_theme.name)
        self.setup()
        self.bind("<Insert>", self.get_bounding_box)

    def __repr__(self):
        return "Demo Application"

    def setup(self):
        sb = ttk.Scrollbar(self, bootstyle=ROUNDED)
        sb.set(0.1, 0.55)

        sb.pack(side=RIGHT, fill=Y, padx=1)
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill=BOTH, expand=YES)
        self.tab = self.create_themed_tab()
        self.nb.add(self.tab, text="Tab 1")
        self.nb.add(ttk.Frame(self.nb), text="Tab 2")
        self.nb.add(ttk.Frame(self.nb), text="Tab 3")

    def change_theme(self, new_theme):
        """Destroying the widget isn't strictly necessary with pure TTK widgets. However, for this demo, I'm explicitly
        allowing the changing of colors, etc... and because I want the styles to be consistent on underlying standard
        tk widgets, I've choosing to redraw all the widgets in the main tab. You can use other methods or avoid this
        altogether if you're not switch between light and dark themes.
        """
        self.tab.destroy()
        self.style.theme_use(new_theme)
        self.tab = self.create_themed_tab()
        self.nb.insert(0, self.tab, text="Tab 1")
        self.nb.select(self.nb.tabs()[0])
        self.theme_name.set(new_theme)

    def create_themed_tab(self):
        """Create a return a frame containing themed widgets"""
        tab = ttk.Frame(self.nb, padding=10)
        colors = ["Primary", "Secondary", "Success", "Info", "Warning", "Danger"]

        header_frame = ttk.Frame(tab, padding=10)
        header = ttk.Label(header_frame, textvariable=self.theme_name, font="-size 30")
        header.pack(side=LEFT, fill=X, pady=5)
        header_frame.pack(fill=X)

        # Menubutton (select a theme)
        mb = ttk.Menubutton(header_frame, text="Select a theme to preview")
        mb.pack(side=RIGHT, fill=X, pady=5)
        mb.menu = ttk.Menu(mb)
        mb["menu"] = mb.menu
        for t in sorted(self.style.themes):
            mb.menu.add_command(label=t, command=lambda theme_name=t: self.change_theme(theme_name))

        # Separator
        ttk.Separator(tab).pack(fill=X, pady=(10, 15))

        # Paned Window
        pw = ttk.PanedWindow(tab)
        pw.pack(fill=X)

        # Available Colors
        color_frame = ttk.LabelFrame(pw, text="Colors available in this theme", padding=(5, 15))
        for color in colors:
            btn = ttk.Button(color_frame, text=color.title(), bootstyle=color)
            btn.pack(side=LEFT, fill=X, expand=YES, padx=2, pady=5)

        pw.add(color_frame)

        # This outer frame will provide an internal buffer between the widget images and the window pane,
        # there is no other way to add internal padding
        widget_outer_frame = ttk.Frame(pw, padding=(0, 10))
        pw.add(widget_outer_frame)

        # Widget images
        widget_frame = ttk.LabelFrame(widget_outer_frame, text="Styled Widgets", padding=10)
        widget_frame.pack(fill=X)

        # Label
        ttk.Label(widget_frame, text="This is a label").pack(side=TOP, fill=X)

        entry_spin_frame = ttk.Frame(widget_frame)
        entry_spin_frame.pack(fill=X, pady=5)

        # Entry
        entry = ttk.Entry(entry_spin_frame, text="An entry field")
        entry.pack(side=LEFT, fill=X, expand=YES)
        entry.text = "An entry field with focus ring"

        # Spinbox
        spinner_options = ["Spinner option 1", "Spinner option 2", "Spinner option 3"]
        spinner = ttk.Spinbox(entry_spin_frame, values=spinner_options, wrap=True, defaultindex=0)
        spinner.pack(side=RIGHT, fill=X, expand=YES, padx=(5, 0))

        # Button
        btn_frame = ttk.Frame(widget_frame)
        b1 = ttk.Button(btn_frame, text="Solid Button")
        b1.pack(side=LEFT, fill=X, expand=YES, padx=(0, 5))

        b2 = ttk.Button(btn_frame, text="Outline Button", bootstyle='outline')
        b2.pack(side=LEFT, fill=X, expand=YES)
        btn_frame.pack(fill=X, pady=5)

        # Option Menu
        om = ttk.OptionMenu(btn_frame, defaultvalue="Choose a theme", values=self.style.themes)
        om.pack(side=RIGHT, fill=X, padx=(5, 0), pady=5)

        # Labelframe
        options_frame = ttk.Frame(widget_frame, padding=(0, 10))
        options_frame.pack(fill=X, pady=5)

        # Radio
        r1 = ttk.Radiobutton(options_frame, value=1, group='radio-options', default=True, text="Radio one")
        r1.pack(side=LEFT, fill=X, expand=YES)
        r2 = ttk.Radiobutton(options_frame, value=2, group='radio-options', text="Radio two")
        r2.pack(side=LEFT, fill=X, expand=YES)

        # Checkbutton
        cb1 = ttk.Checkbutton(options_frame, text="Option 1", default=True)
        cb1.pack(side=LEFT, fill=X, expand=YES)

        cb2 = ttk.Checkbutton(options_frame, text="Option 2")
        cb2.pack(side=LEFT, fill=X, expand=YES)

        # Treeview
        tv = ttk.Treeview(widget_frame, height=3)
        tv.pack(fill=X, pady=5)
        tv.heading("#0", text="Example heading")
        tv.insert("", "end", "example1", text="Example 1")
        tv.insert("", "end", "example2", text="Example 2")
        tv.insert("example2", "end", text="Example 2 Child 1")
        tv.insert("example2", "end", text="Example 2 Child 2")
        tv.selection_set("example1")

        # Scale
        scale_frame = ttk.Frame(widget_frame)
        scale = ttk.Scale(scale_frame, defaultvalue=25)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=(0, 2))
        scale_frame.pack(side=TOP, fill=X, pady=5)
        entry = ttk.Entry(scale_frame, textvariable=scale.variable, width=4)
        entry.pack(side=RIGHT)

        # Combobox
        cbo = ttk.Combobox(widget_frame, values=colors, defaultvalue=PRIMARY)
        cbo.pack(fill=X, pady=5)

        # Progressbar
        ttk.Progressbar(widget_frame, variable=scale.variable, bootstyle=STRIPED).pack(fill=X, pady=10)
        return tab

    def get_bounding_box(self, event):
        """Take a screenshot of the current demo window and save to images"""
        # bounding box
        titlebar = 31
        x1 = self.winfo_rootx() - 1
        y1 = self.winfo_rooty() - titlebar
        x2 = x1 + self.winfo_width() + 2
        y2 = y1 + self.winfo_height() + titlebar + 1

        self.after_idle(self.save_screenshot, [x1, y1, x2, y2])

    def save_screenshot(self, bbox):
        """Save a screenshot"""
        # screenshot
        img = ImageGrab.grab(bbox=bbox)

        # image name
        filename = f"../../docs/images/{self.theme_name.get()}.png"
        img.save(filename, "png")
        print(filename)  # print for confirmation


if __name__ == "__main__":
    Demo().run()

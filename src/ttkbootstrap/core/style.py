import colorsys
import importlib.resources
from tkinter import ttk
from uuid import uuid4
from PIL import ImageTk, Image, ImageDraw, ImageFont

from ttkbootstrap.core.themes import DEFAULT_FONT, ThemeColors
from ttkbootstrap.core.themes import ThemeDefinition


class Style(ttk.Style):
    """A class for setting the application style.

    Sets the theme of the ``tkinter.Tk`` instance and supports all ttkbootstrap and ttk themes provided. This class is
    meant to be a drop-in replacement for ``ttk.Style`` and inherits all of it's methods and properties. Creating a
    ``Style`` object will instantiate the ``tkinter.Tk`` instance in the ``Style.master`` property, and so it is not
    necessary to explicitly create an instance of ``tkinter.Tk``. For more details on the ``ttk.Style`` class, see the
    python documentation_.

    .. code-block:: python

        # instantiate the style with default theme *flatly*
        style = Style()

        # instantiate the style with another theme
        style = Style(theme='superhero')

        # instantiate the style with a theme from a specific themes file
        style = Style(theme='custom_name',
                      themes_file='C:/example/my_themes.json')

        # available themes
        for theme in style.theme_names():
            print(theme)

    .. _documentation: https://docs.python.org/3.9/library/tkinter.ttk.html#tkinter.ttk.Style
    """

    def __init__(self, themename="flatly", themes_file=None, master=None):
        super().__init__(master=master)

        self.styler = None
        self.theme_definitions = ThemeDefinition.load_themes(themes_file=themes_file)
        self.themes = set(self.theme_names())
        self.theme_objects = dict()
        self.register_themes()
        self.theme_use(themename=themename)

    @property
    def colors(self):
        return self.theme.colors

    def register_themes(self):
        """Registers all themes loaded into the ``theme_definitions`` property"""
        for theme in self.theme_definitions:
            self.themes.add(theme)

    def theme_use(self, themename=None):
        """Changes the theme used in rendering the application widgets.

        If themename is None, returns the theme in use, otherwise, set the current theme to themename, refreshes all
        widgets and emits a ``<<ThemeChanged>>`` event.

        Only use this method if you are changing the theme *during* runtime. Otherwise, pass the theme name into the
        Style constructor to instantiate the style with a theme.

        Keyword Args:
            themename (str): the theme to apply when creating new widgets
        """
        self.theme = self.theme_definitions.get(themename)

        if not themename:
            return super().theme_use()

        if all([themename, themename not in self.themes]):
            print(f"{themename} is not a valid theme name. Please try one of the following:")
            print(list(self.themes))
            return

        if themename not in self.theme_names():
            self.theme_objects[themename] = StylerTTK(self, self.theme)

        super().theme_use(themename)
        self.theme_objects[themename].styler_tk.style_tkinter_widgets()

        return


class StylerTK:
    """A class for styling tkinter widgets (not ttk).

    Several ttk widgets utilize tkinter widgets in some capacity, such as the `popdownlist` on the ``ttk.Combobox``. To
    create a consistent user experience, standard tkinter widgets are themed as much as possible with the look and feel
    of the **ttkbootstrap** theme applied. Tkinter widgets are not the primary target of this project; however, they can
    be used without looking entirely out-of-place in most cases.

    Attributes:
        master (Tk): the root window.
        theme (ThemeDefinition): the color settings defined in the `themes.json` file.
    """

    def __init__(self, styler_ttk):
        """
        Args:
            styler_ttk (StylerTTK): an instance of the ``StylerTTK`` class.
        """
        self.master = styler_ttk.style.master
        self.theme = styler_ttk.theme

    def style_tkinter_widgets(self):
        """A wrapper on all widget style methods. Applies current theme to all standard tkinter widgets"""
        self._style_spinbox()
        self._style_textwidget()
        self._style_button()
        self._style_label()
        self._style_checkbutton()
        self._style_radiobutton()
        self._style_entry()
        self._style_scale()
        self._style_listbox()
        self._style_menu()
        self._style_menubutton()
        self._style_labelframe()
        self._style_canvas()
        self._style_window()

    def _set_option(self, *args):
        """A convenience wrapper method to shorten the call to ``option_add``. *Laziness is next to godliness*.

        Args:
            *args (Tuple[str]): (pattern, value, priority=80)
        """
        self.master.option_add(*args)

    def _style_window(self):
        """Apply global options to all matching ``tkinter`` widgets"""
        self.master.configure(background=self.theme.colors.bg)
        self._set_option("*background", self.theme.colors.bg, 60)
        self._set_option("*font", self.theme.font, 60)
        self._set_option("*activeBackground", self.theme.colors.selectbg, 60)
        self._set_option("*activeForeground", self.theme.colors.selectfg, 60)
        self._set_option("*selectBackground", self.theme.colors.selectbg, 60)
        self._set_option("*selectForeground", self.theme.colors.selectfg, 60)

    def _style_canvas(self):
        """Apply style to ``tkinter.Canvas``"""
        self._set_option("*Canvas.highlightThickness", 1)
        self._set_option("*Canvas.highlightBackground", self.theme.colors.border)
        self._set_option("*Canvas.background", self.theme.colors.bg)

    def _style_button(self):
        """Apply style to ``tkinter.Button``"""
        active_bg = ThemeColors.update_hsv(self.theme.colors.primary, vd=-0.2)
        self._set_option("*Button.relief", "flat")
        self._set_option("*Button.borderWidth", 0)
        self._set_option("*Button.activeBackground", active_bg)
        self._set_option("*Button.foreground", self.theme.colors.selectfg)
        self._set_option("*Button.background", self.theme.colors.primary)

    def _style_label(self):
        """Apply style to ``tkinter.Label``"""
        self._set_option("*Label.foreground", self.theme.colors.fg)
        self._set_option("*Label.background", self.theme.colors.bg)

    def _style_checkbutton(self):
        """Apply style to ``tkinter.Checkbutton``"""
        self._set_option("*Checkbutton.activeBackground", self.theme.colors.bg)
        self._set_option("*Checkbutton.activeForeground", self.theme.colors.primary)
        self._set_option("*Checkbutton.background", self.theme.colors.bg)
        self._set_option("*Checkbutton.foreground", self.theme.colors.fg)
        self._set_option(
            "*Checkbutton.selectColor", self.theme.colors.primary if self.theme.type == "dark" else "white"
        )

    def _style_radiobutton(self):
        """Apply style to ``tkinter.Radiobutton``"""
        self._set_option("*Radiobutton.activeBackground", self.theme.colors.bg)
        self._set_option("*Radiobutton.activeForeground", self.theme.colors.primary)
        self._set_option("*Radiobutton.background", self.theme.colors.bg)
        self._set_option("*Radiobutton.foreground", self.theme.colors.fg)
        self._set_option(
            "*Radiobutton.selectColor", self.theme.colors.primary if self.theme.type == "dark" else "white"
        )

    def _style_entry(self):
        """Apply style to ``tkinter.Entry``"""
        self._set_option("*Entry.relief", "flat")
        self._set_option(
            "*Entry.background",
            (
                self.theme.colors.inputbg
                if self.theme.type == "light"
                else ThemeColors.update_hsv(self.theme.colors.inputbg, vd=-0.1)
            ),
        )
        self._set_option("*Entry.foreground", self.theme.colors.inputfg)
        self._set_option("*Entry.highlightThickness", 1)
        self._set_option("*Entry.highlightBackground", self.theme.colors.border)
        self._set_option("*Entry.highlightColor", self.theme.colors.primary)

    def _style_scale(self):
        """Apply style to ``tkinter.Scale``"""
        active_color = ThemeColors.update_hsv(self.theme.colors.primary, vd=-0.2)

        self._set_option("*Scale.background", self.theme.colors.primary)
        self._set_option("*Scale.showValue", False)
        self._set_option("*Scale.sliderRelief", "flat")
        self._set_option("*Scale.borderWidth", 0)
        self._set_option("*Scale.activeBackground", active_color)
        self._set_option("*Scale.highlightThickness", 1)
        self._set_option("*Scale.highlightColor", self.theme.colors.border)
        self._set_option("*Scale.highlightBackground", self.theme.colors.border)
        self._set_option("*Scale.troughColor", self.theme.colors.inputbg)

    def _style_spinbox(self):
        """Apply style to `tkinter.Spinbox``"""
        self._set_option("*Spinbox.foreground", self.theme.colors.inputfg)
        self._set_option("*Spinbox.relief", "flat")
        self._set_option(
            "*Spinbox.background",
            (
                self.theme.colors.inputbg
                if self.theme.type == "light"
                else ThemeColors.update_hsv(self.theme.colors.inputbg, vd=-0.1)
            ),
        )
        self._set_option("*Spinbox.highlightThickness", 1)
        self._set_option("*Spinbox.highlightColor", self.theme.colors.primary)
        self._set_option("*Spinbox.highlightBackground", self.theme.colors.border)

    def _style_listbox(self):
        """Apply style to ``tkinter.Listbox``"""
        self._set_option("*Listbox.foreground", self.theme.colors.inputfg)
        self._set_option("*Listbox.background", self.theme.colors.inputbg)
        self._set_option("*Listbox.selectBackground", self.theme.colors.selectbg)
        self._set_option("*Listbox.selectForeground", self.theme.colors.selectfg)
        self._set_option("*Listbox.relief", "flat")
        self._set_option("*Listbox.activeStyle", "none")
        self._set_option("*Listbox.highlightThickness", 1)
        self._set_option("*Listbox.highlightColor", self.theme.colors.primary)
        self._set_option("*Listbox.highlightBackground", self.theme.colors.border)

    def _style_menubutton(self):
        """Apply style to ``tkinter.Menubutton``"""
        hover_color = ThemeColors.update_hsv(self.theme.colors.primary, vd=-0.2)
        self._set_option("*Menubutton.activeBackground", hover_color)
        self._set_option("*Menubutton.background", self.theme.colors.primary)
        self._set_option("*Menubutton.foreground", self.theme.colors.selectfg)
        self._set_option("*Menubutton.borderWidth", 0)

    def _style_menu(self):
        """Apply style to ``tkinter.Menu``"""
        self._set_option("*Menu.tearOff", 0)
        self._set_option("*Menu.foreground", self.theme.colors.fg)
        self._set_option("*Menu.selectColor", self.theme.colors.primary)
        self._set_option("*Menu.font", self.theme.font)
        self._set_option(
            "*Menu.background",
            (self.theme.colors.inputbg if self.theme.type == "light" else self.theme.colors.bg),
        )
        self._set_option("*Menu.activeBackground", self.theme.colors.selectbg)
        self._set_option("*Menu.activeForeground", self.theme.colors.selectfg)

    def _style_labelframe(self):
        """Apply style to ``tkinter.Labelframe``"""
        self._set_option("*Labelframe.font", self.theme.font)
        self._set_option("*Labelframe.foreground", self.theme.colors.fg)
        self._set_option("*Labelframe.highlightColor", self.theme.colors.border)
        self._set_option("*Labelframe.borderWidth", 1)
        self._set_option("*Labelframe.highlightThickness", 0)

    def _style_textwidget(self):
        """Apply style to ``tkinter.Text``"""
        self._set_option("*Text.background", self.theme.colors.inputbg)
        self._set_option("*Text.foreground", self.theme.colors.inputfg)
        self._set_option("*Text.highlightColor", self.theme.colors.primary)
        self._set_option("*Text.highlightBackground", self.theme.colors.border)
        self._set_option("*Text.borderColor", self.theme.colors.border)
        self._set_option("*Text.highlightThickness", 1)
        self._set_option("*Text.relief", "flat")
        self._set_option("*Text.font", self.theme.font)
        self._set_option("*Text.padX", 5)
        self._set_option("*Text.padY", 5)


class StylerTTK:
    """A class to create a new ttk theme.

    Create a new ttk theme by using a combination of built-in themes and some image-based elements using ``pillow``. A
    theme is generated at runtime and is available to use with the ``Style`` class methods. The base theme of all
    **ttkbootstrap** themes is *clam*. In many cases, widget layouts are re-created using an assortment of elements from
    various styles such as *clam*, *alt*, *default*, etc...

    Attributes:
        theme_images (dict): theme assets used for various widgets.
        settings (dict): settings used to build the actual theme using the ``theme_create`` method.
        styler_tk (StylerTk): an object used to style tkinter widgets (not ttk).
        theme (ThemeDefinition): the theme settings defined in the `themes.json` file.
    """

    theme_images = dict()

    def __init__(self, style, definition):
        """
        Args:
            style (Style): an instance of ``ttk.Style``.
            definition (ThemeDefinition): an instance of ``ThemeDefinition``; used to create the theme settings.
        """
        self.style = style
        self.theme = definition
        self.theme_images = StylerTTK.theme_images
        self.settings = {}
        self.styler_tk = StylerTK(self)
        self.create_theme()

    def create_theme(self):
        """Create and style a new ttk theme. A wrapper around internal style methods."""
        self.update_ttk_theme_settings()
        self.style.theme_create(self.theme.name, "clam", self.settings)

    def update_ttk_theme_settings(self):
        """Update the settings dictionary that is used to create a theme. This is a wrapper on all the `_style_widget`
        methods which define the layout, configuration, and styling mapping for each ttk widget.
        """
        self._style_exit_button()
        self._style_calendar()
        self._style_meter()

        # default style
        self.settings.update(self.style_treeitem())
        self.settings.update(self.style_treeview(self.theme, style="Treeview"))
        self.settings.update(self.style_progressbar(self.theme, style="Horizontal.TProgressbar"))
        self.settings.update(self.style_progressbar(self.theme, orient="vertical", style="Vertical.TProgressbar"))
        self.settings.update(self.style_floodgauge(self.theme, style="Horizontal.TFloodgauge"))
        self.settings.update(self.style_floodgauge(self.theme, orient="vertical", style="Vertical.TFloodgauge"))
        self.settings.update(self.style_progressbar(self.theme, style="Striped.Horizontal.TProgressbar"))
        self.settings.update(
            self.style_progressbar(self.theme, orient="vertical", style="Striped.Vertical.TProgressbar")
        )
        self.settings.update(self.style_button(self.theme, style="TButton"))
        self.settings.update(self.style_scrollbar(self.theme, style="Vertical.TScrollbar"))
        self.settings.update(self.style_scrollbar(self.theme, style="Rounded.Vertical.TScrollbar"))
        self.settings.update(self.style_outline_button(self.theme, style="Outline.TButton"))
        self.settings.update(self.style_link_button(self.theme, style="Link.TButton"))
        self.settings.update(self.style_sizegrip(self.theme, style="TSizegrip"))
        self.settings.update(self.style_scale(self.theme, orient="vertical", style="Vertical.TScale"))
        self.settings.update(self.style_scale(self.theme, orient="horizontal", style="Horizontal.TScale"))
        self.settings.update(self.style_separator(self.theme, orient="vertical", style="Vertical.TSeparator"))
        self.settings.update(self.style_separator(self.theme, style="Horizontal.TSeparator"))
        self.settings.update(self.style_checkbutton(self.theme, style="TCheckbutton"))
        self.settings.update(self.style_radiobutton(self.theme, style="TRadiobutton"))
        self.settings.update(self.style_toolbutton(self.theme, style="Toolbutton"))
        self.settings.update(self.style_outline_toolbutton(self.theme, style="Outline.Toolbutton"))
        self.settings.update(self.style_roundtoggle(self.theme, style="Roundtoggle.Toolbutton"))
        self.settings.update(self.style_squaretoggle(self.theme, style="Squaretoggle.Toolbutton"))
        self.settings.update(self.style_frame(self.theme, style="TFrame"))
        self.settings.update(self.style_combobox(self.theme, style="TCombobox"))
        self.settings.update(self.style_entry(self.theme, style="TEntry"))
        self.settings.update(self.style_label(self.theme, style="TLabel"))
        self.settings.update(self.style_label(self.theme, background=self.theme.colors.fg, style="Inverse.TLabel"))
        self.settings.update(self.style_labelframe(self.theme, foreground=self.theme.colors.fg, style="TLabelframe"))
        self.settings.update(self.style_menubutton(self.theme, style="TMenubutton"))
        self.settings.update(self.style_outline_menubutton(self.theme, style="Outline.TMenubutton"))
        self.settings.update(self.style_panedwindow(self.theme, style="TPanedwindow"))
        self.settings.update(self.style_notebook(self.theme, style="TNotebook"))
        self.settings.update(self.style_spinbox(self.theme, style="TSpinbox"))
        self.settings.update(self.style_scrollbar(self.theme, orient="horizontal", style="Horizontal.TScrollbar"))
        self.settings.update(
            self.style_scrollbar(self.theme, orient="horizontal", style="Rounded.Horizontal.TScrollbar")
        )

        # themed style
        for color in self.theme.colors:
            self.settings.update(self.style_treeview(self.theme, headerbackground=color, style=f"{color}.Treeview"))
            self.settings.update(self.style_button(self.theme, background=color, style=f"{color}.TButton"))
            self.settings.update(self.style_link_button(self.theme, foreground=color, style=f"{color}.Link.TButton"))
            self.settings.update(self.style_sizegrip(self.theme, foreground=color, style=f"{color}.TSizegrip"))
            self.settings.update(self.style_frame(self.theme, background=color, style=f"{color}.TFrame"))
            self.settings.update(self.style_toolbutton(self.theme, indicatorcolor=color, style=f"{color}.Toolbutton"))
            self.settings.update(self.style_combobox(self.theme, focuscolor=color, style=f"{color}.TCombobox"))
            self.settings.update(self.style_spinbox(self.theme, focuscolor=color, style=f"{color}.TSpinbox"))
            self.settings.update(self.style_entry(self.theme, focuscolor=color, style=f"{color}.TEntry"))
            self.settings.update(self.style_label(self.theme, foreground=color, style=f"{color}.TLabel"))
            self.settings.update(self.style_label(self.theme, background=color, style=f"{color}.Inverse.TLabel"))
            self.settings.update(self.style_labelframe(self.theme, background=color, style=f"{color}.TLabelframe"))
            self.settings.update(self.style_panedwindow(self.theme, sashcolor=color, style=f"{color}.TPanedwindow"))
            self.settings.update(self.style_menubutton(self.theme, background=color, style=f"{color}.TMenubutton"))
            self.settings.update(self.style_notebook(self.theme, background=color, style=f"{color}.TNotebook"))
            self.settings.update(self.style_floodgauge(self.theme, barcolor=color, style=f"{color}.Horizontal.TFloodgauge"))
            self.settings.update(self.style_floodgauge(self.theme, barcolor=color, orient="vertical", style=f"{color}.Vertical.TFloodgauge"))

            self.settings.update(
                self.style_progressbar(self.theme, barcolor=color, style=f"{color}.Horizontal.TProgressbar")
            )
            self.settings.update(
                self.style_progressbar(self.theme, barcolor=color, style=f"{color}.Striped.Horizontal.TProgressbar")
            )
            self.settings.update(
                self.style_progressbar(
                    self.theme, orient="vertical", barcolor=color, style=f"{color}.Vertical.TProgressbar"
                )
            )
            self.settings.update(
                self.style_progressbar(
                    self.theme, orient="vertical", barcolor=color, style=f"{color}.Striped.Vertical.TProgressbar"
                )
            )
            self.settings.update(
                self.style_scrollbar(self.theme, thumbcolor=color, style=f"{color}.Vertical.TScrollbar")
            )
            self.settings.update(
                self.style_scrollbar(
                    self.theme, thumbcolor=color, orient="horizontal", style=f"{color}.Horizontal.TScrollbar"
                )
            )
            self.settings.update(
                self.style_scrollbar(self.theme, thumbcolor=color, style=f"{color}.Rounded.Vertical.TScrollbar")
            )
            self.settings.update(
                self.style_scrollbar(
                    self.theme, thumbcolor=color, orient="horizontal", style=f"{color}.Rounded.Horizontal.TScrollbar"
                )
            )
            self.settings.update(
                self.style_scale(self.theme, slidercolor=color, orient="vertical", style=f"{color}.Vertical.TScale")
            )
            self.settings.update(
                self.style_scale(self.theme, slidercolor=color, orient="horizontal", style=f"{color}.Horizontal.TScale")
            )
            self.settings.update(
                self.style_outline_menubutton(self.theme, foreground=color, style=f"{color}.Outline.TMenubutton")
            )
            self.settings.update(
                self.style_outline_toolbutton(self.theme, indicatorcolor=color, style=f"{color}.Outline.Toolbutton")
            )
            self.settings.update(
                self.style_roundtoggle(self.theme, indicatorcolor=color, style=f"{color}.Roundtoggle.Toolbutton")
            )
            self.settings.update(
                self.style_squaretoggle(self.theme, indicatorcolor=color, style=f"{color}.Squaretoggle.Toolbutton")
            )
            self.settings.update(
                self.style_checkbutton(self.theme, indicatorcolor=color, style=f"{color}.TCheckbutton")
            )
            self.settings.update(
                self.style_radiobutton(self.theme, indicatorcolor=color, style=f"{color}.TRadiobutton")
            )
            self.settings.update(
                self.style_separator(self.theme, sashcolor=color, style=f"{color}.Horizontal.TSeparator")
            )
            self.settings.update(
                self.style_separator(
                    self.theme, sashcolor=color, orient="vertical", style=f"{color}.Vertical.TSeparator"
                )
            )
            self.settings.update(
                self.style_outline_button(self.theme, foreground=color, style=f"{color}.Outline.TButton")
            )

        self._style_defaults()

    def _style_defaults(self):
        """Setup the default ``ttk.Style`` configuration. These defaults are applied to any widget that contains these
        element options. This method should be called *first* before any other style is applied during theme creation.
        """
        self.settings.update(
            {
                ".": {
                    "configure": {
                        "background": self.theme.colors.bg,
                        "darkcolor": self.theme.colors.border,
                        "foreground": self.theme.colors.fg,
                        "troughcolor": self.theme.colors.bg,
                        "selectbg": self.theme.colors.selectbg,
                        "selectfg": self.theme.colors.selectfg,
                        "selectforeground": self.theme.colors.selectfg,
                        "selectbackground": self.theme.colors.selectbg,
                        "fieldbg": "white",
                        "font": self.theme.font,
                        "borderwidth": 1,
                        "focuscolor": "",
                    }
                }
            }
        )

    @staticmethod
    def style_combobox(theme, background=None, font=DEFAULT_FONT, foreground=None, focuscolor=None, style=None):
        """Create a combobox style.

        Args:
            theme (str): The theme name.
            background (str, optional): The color of the combobox background.
            focuscolor (str, optional): The color of the focus ring when the widget has focus.
            font (str, optional): The font used to render the widget text.
            foreground (str, optional): The color of the widget text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.inputbg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.inputfg, theme.colors)
        focuscolor = ThemeColors.normalize(focuscolor, theme.colors.primary, theme.colors)
        disabled_fg = ThemeColors.update_hsv(foreground, vd=-0.2 if theme.type == "light" else -0.3)

        # style settings
        settings = dict()
        element = uuid4()

        if theme.type == "dark":  # prevents corners from shining through on clam theme.
            settings.update({"combo.Spinbox.field": {"element create": ("from", "default")}})

        settings.update(
            {
                f"{element}.Combobox.downarrow": {"element create": ("from", "default")},
                style: {
                    "layout": [
                        (
                            "combo.Spinbox.field",
                            {
                                "side": "top",
                                "sticky": "we",
                                "children": [
                                    (f"{element}.Combobox.downarrow", {"side": "right", "sticky": "ns"}),
                                    (
                                        "Combobox.padding",
                                        {
                                            "expand": "1",
                                            "sticky": "nswe",
                                            "children": [("Combobox.textarea", {"sticky": "nswe"})],
                                        },
                                    ),
                                ],
                            },
                        )
                    ],
                    "configure": {
                        "bordercolor": theme.colors.border,
                        "darkcolor": background,
                        "lightcolor": background,
                        "arrowcolor": foreground,
                        "foreground": foreground,
                        "font": font,
                        "fieldbackground ": background,
                        "background ": background,
                        "relief": "flat",
                        "borderwidth ": 0,  # only applies to dark theme border
                        "padding": 5,
                        "arrowsize ": 14,
                    },
                    "map": {
                        "foreground": [("disabled", disabled_fg)],
                        "bordercolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", focuscolor),
                        ],
                        "lightcolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", background),
                        ],
                        "darkcolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", background),
                        ],
                        "arrowcolor": [
                            ("disabled", disabled_fg),
                            ("pressed !disabled", background),
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", focuscolor),
                        ],
                    },
                },
            }
        )
        return settings

    @staticmethod
    def style_separator(theme, orient="horizontal", sashcolor=None, sashthickness=1, style=None):
        """Create a separator style.

        Args:
            theme (str): The color theme.
            orient (str, optional): One of 'horizontal' or 'vertical'
            sashcolor (str, optional): The color of the separator.
            sashthickness (int, optional): The thickness of the separator.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        fallback = theme.colors.border if theme.type == "light" else theme.colors.selectbg
        sashcolor = ThemeColors.normalize(sashcolor, fallback, theme.colors)

        # separator images
        element = uuid4()
        hs_im = ImageTk.PhotoImage(Image.new("RGB", (40, sashthickness), sashcolor))
        StylerTTK.theme_images[f"{element}.h.separator"] = hs_im

        vs_im = ImageTk.PhotoImage(Image.new("RGB", (sashthickness, 40), sashcolor))
        StylerTTK.theme_images[f"{element}.v.separator"] = vs_im

        # style settings
        settings = dict()

        if orient.lower() == "horizontal":
            settings.update(
                {
                    f"{element}.Horizontal.Separator.separator": {
                        "element create": ("image", StylerTTK.theme_images[f"{element}.h.separator"])
                    },
                    f"{style}": {"layout": [(f"{element}.Horizontal.Separator.separator", {"sticky": "we"})]},
                }
            )
        else:
            settings.update(
                {
                    f"{element}.Vertical.Separator.separator": {
                        "element create": ("image", StylerTTK.theme_images[f"{element}.v.separator"])
                    },
                    f"{style}": {"layout": [(f"{element}.Vertical.Separator.separator", {"sticky": "ns"})]},
                }
            )
        return settings

    @staticmethod
    def style_progressbar(theme, barcolor=None, troughcolor=None, orient="horizontal", style=None):
        """Create a default progressbar style.

        Args:
            theme (str): The theme name.
            troughcolor (str): The color of the trough.
            orient (str): One of 'horizontal' or 'vertical'
            slidercolor (str): The color of the round slider.
            style (str): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        barcolor = ThemeColors.normalize(barcolor, theme.colors.primary, theme.colors)
        bordercolor = theme.colors.border if theme.type == "light" else theme.colors.inputbg
        troughcolor = ThemeColors.normalize(troughcolor, theme.colors.inputbg, theme.colors)

        # style settings
        settings = dict()
        element = style.replace("TProgressbar", "Progressbar")

        if "stripe" in style.lower():
            StylerTTK.style_striped_progressbar_images(barcolor, orient, element)
        else:
            StylerTTK.style_default_progressbar_images(barcolor, orient, element)

        ## horizontal progressbar
        if orient.lower() == "horizontal":
            settings.update(
                {
                    f"{element}.pbar": {
                        "element create": (
                            "image",
                            StylerTTK.theme_images[f"{element}.hbar"],
                            {"width": 20, "sticky": "ew"},
                        )
                    },
                    style: {
                        "layout": [
                            (
                                "Horizontal.Progressbar.trough",
                                {
                                    "sticky": "nswe",
                                    "children": [(f"{element}.pbar", {"side": "left", "sticky": "ns"})],
                                },
                            )
                        ],
                        "configure": {
                            "troughcolor": troughcolor,
                            "thickness": 20,
                            "borderwidth": 1,
                            "bordercolor": bordercolor,
                        },
                    },
                }
            )

        ## vertical progressbar
        else:
            settings.update(
                {
                    f"{element}.pbar": {
                        "element create": (
                            "image",
                            StylerTTK.theme_images[f"{element}.vbar"],
                            {"width": 20, "sticky": "ns"},
                        )
                    },
                    style: {
                        "layout": [
                            (
                                "Vertical.Progressbar.trough",
                                {
                                    "sticky": "nswe",
                                    "children": [(f"{element}.pbar", {"side": "bottom", "sticky": "we"})],
                                },
                            )
                        ],
                        "configure": {
                            "troughcolor": troughcolor,
                            "thickness": 20,
                            "borderwidth": 1,
                            "lightcolor": bordercolor,
                        },
                    },
                }
            )
        return settings

    @staticmethod
    def style_default_progressbar_images(barcolor, orient, element):
        """Create images for default progressbar

        Args:
            barcolor (str): The color of the progressbar.
            orient (str): One of 'horizontal' or 'vertical'.
            element (str): A unique widget id to associate with the images.
        """
        im = Image.new("RGBA", (22, 22), barcolor)
        pbar_image = ImageTk.PhotoImage(im)
        StylerTTK.theme_images[f"{element}.{orient[0].lower()}bar"] = pbar_image

    @staticmethod
    def style_striped_progressbar_images(barcolor, orient, element):
        """Create images for the striped progressbar

        Args:
            barcolor (str): The color of the progressbar.
            orient (str): One of 'horizontal' or 'vertical'.
            element (str): A unique widget id to associate with the images.
        """
        # calculate the light color value
        b = colorsys.rgb_to_hsv(*ThemeColors.hex_to_rgb(barcolor))[2]
        if b < 0.4:
            vd = 0.3
        elif b > 0.9:
            vd = 0
        else:
            vd = 0.1
        lightcolor = ThemeColors.update_hsv(barcolor, sd=-0.2, vd=vd)

        im = Image.new("RGBA", (100, 100), lightcolor)
        draw = ImageDraw.Draw(im)
        draw.polygon([(0, 0), (48, 0), (100, 52), (100, 100), (100, 100)], fill=barcolor)
        draw.polygon([(0, 52), (48, 100), (0, 100)], fill=barcolor)
        pbar_image = ImageTk.PhotoImage(im.resize((22, 22), Image.LANCZOS))
        StylerTTK.theme_images[f"{element}.{orient[0].lower()}bar"] = pbar_image

    @staticmethod
    def style_scale(theme, troughcolor=None, slidercolor=None, orient="horizontal", style=None):
        """Create a scale style.

        Args:
            theme (str): The theme name.
            troughcolor (str, optional): The color of the trough.
            orient (str, optional): One of 'horizontal' or 'vertical'
            slidercolor (str, optional): The color of the round slider.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        slidercolor = ThemeColors.normalize(slidercolor, theme.colors.primary, theme.colors)
        troughcolor = ThemeColors.normalize(troughcolor, theme.colors.inputbg, theme.colors)
        disabled = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # images
        element = style.replace("TScale", "Scale")
        StylerTTK.style_scale_images(slidercolor, troughcolor, disabled, orient, element, theme)

        img_disabled = StylerTTK.theme_images[f"{element}.disabled"]
        img_normal = StylerTTK.theme_images[f"{element}.normal"]
        img_pressed = StylerTTK.theme_images[f"{element}.pressed"]
        img_hover = StylerTTK.theme_images[f"{element}.hover"]
        img_trough = StylerTTK.theme_images[f"{element}.trough"]

        # style settings
        settings = dict()
        if orient.lower() == "horizontal":
            settings.update(
                {
                    f"{element}.Horizontal.Scale.track": {"element create": ("image", img_trough, {"border": 5})},
                    f"{element}.Horizontal.Scale.slider": {
                        "element create": (
                            "image",
                            img_normal,
                            ("disabled", img_disabled),
                            ("pressed", img_pressed),
                            ("hover", img_hover),
                        )
                    },
                    style: {
                        "layout": [
                            (
                                "Scale.focus",
                                {
                                    "expand": "1",
                                    "sticky": "nswe",
                                    "children": [
                                        (f"{element}.Horizontal.Scale.track", {"sticky": "we"}),
                                        (f"{element}.Horizontal.Scale.slider", {"side": "left", "sticky": ""}),
                                    ],
                                },
                            )
                        ]
                    },
                }
            )

        else:
            settings.update(
                {
                    f"{element}.Vertical.Scale.track": {"element create": ("image", img_trough, {"border": 5})},
                    f"{element}.Vertical.Scale.slider": {
                        "element create": (
                            "image",
                            img_normal,
                            ("disabled", img_disabled),
                            ("pressed", img_pressed),
                            ("hover", img_hover),
                        )
                    },
                    style: {
                        "layout": [
                            (
                                "Scale.focus",
                                {
                                    "expand": "1",
                                    "sticky": "nswe",
                                    "children": [
                                        (f"{element}.Vertical.Scale.track", {"sticky": "ns"}),
                                        (f"{element}.Vertical.Scale.slider", {"side": "top", "sticky": ""}),
                                    ],
                                },
                            )
                        ]
                    },
                }
            )

        return settings

    @staticmethod
    def style_scale_images(slidercolor, troughcolor, disabled, orient, element, theme):
        """Create images for the scale widget image layout

        Args:
            slidercolor (str): The color used on the round slider.
            disabled (str): The slider color when disabled.
            troughcolor (str): The color used on the trough.
            orient (str): One of 'horizontal' or 'vertical'.
            element (str): A unique widget id to associate with the images.
            theme (str): The current theme.
        """
        outline = ThemeColors.update_hsv(troughcolor, vd=-0.10)
        pressed = ThemeColors.update_hsv(slidercolor, vd=-0.20 if theme.type == "light" else 0.35)
        hover = ThemeColors.update_hsv(slidercolor, vd=-0.10 if theme.type == "light" else 0.25)
        size = (16, 16)

        im = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=slidercolor)
        StylerTTK.theme_images[f"{element}.normal"] = ImageTk.PhotoImage(im.resize(size, Image.CUBIC))

        im = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=pressed)
        StylerTTK.theme_images[f"{element}.pressed"] = ImageTk.PhotoImage(im.resize(size, Image.CUBIC))

        im = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=disabled)
        StylerTTK.theme_images[f"{element}.disabled"] = ImageTk.PhotoImage(im.resize(size, Image.CUBIC))

        im = Image.new("RGBA", (100, 100))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, 95, 95), fill=hover)
        StylerTTK.theme_images[f"{element}.hover"] = ImageTk.PhotoImage(im.resize(size, Image.CUBIC))

        if orient.lower() == "horizontal":
            im = Image.new("RGBA", (400, 80))
            draw = ImageDraw.Draw(im)
            draw.rounded_rectangle([1, 20, 399, 60], radius=78, fill=troughcolor, outline=outline, width=5)
            StylerTTK.theme_images[f"{element}.trough"] = ImageTk.PhotoImage(im.resize([40, 8], Image.CUBIC))
        else:
            im = Image.new("RGBA", (80, 400))
            draw = ImageDraw.Draw(im)
            draw.rounded_rectangle([20, 1, 60, 399], radius=78, fill=troughcolor, outline=outline, width=5)
            StylerTTK.theme_images[f"{element}.trough"] = ImageTk.PhotoImage(im.resize([8, 40], Image.CUBIC))

    @staticmethod
    def style_floodgauge(theme, barcolor=None, font="helvetica 24 bold", foreground=None, troughcolor=None, orient="horizontal", style=None, thickness=200):
        """Create a default floodgauge style.

        Args:
            theme (str): The theme name.
            troughcolor (str): The color of the trough.
            font (str): The font used to render the widget text.
            foreground (str): The color of the widget text.
            orient (str): One of 'horizontal' or 'vertical'
            style (str): The style used to render the widget.
            thickness (int): The thickness of the progressbar along the short side.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        barcolor = ThemeColors.normalize(barcolor, theme.colors.primary, theme.colors)
        fb_troughcolor = ThemeColors.update_hsv(barcolor, sd=-0.3, vd=0.8)
        troughcolor = ThemeColors.normalize(troughcolor, fb_troughcolor, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.selectfg, theme.colors)

        # style settings
        settings = dict()
        element = style.replace("TFloodgauge", "Floodgauge")
        sticky = "ns" if orient.lower() == "horizontal" else "we"
        settings.update(
            {
                f"{element}.Floodgauge.trough": {"element create": ("from", "clam")},
                f"{element}.Floodgauge.pbar": {"element create": ("from", "default")},
                style: {
                    "layout": [
                    (
                        f"{element}.Floodgauge.trough",
                        {
                            "children": [
                                (f"{element}.Floodgauge.pbar", {"sticky": sticky}),
                                ("Floodgauge.label", {"sticky": ""}),
                            ],
                            "sticky": "nswe",
                        },
                    )
                ],
                    "configure": {
                        "thickness": thickness,
                        "borderwidth": 1,
                        "bordercolor": barcolor,
                        "lightcolor": barcolor,
                        "pbarrelief": "flat",
                        "troughcolor": troughcolor,
                        "background": barcolor,
                        "foreground": foreground,
                        "justify": "center",
                        "anchor": "center",
                        "font": font
                    },
                },
            }
        )

        return settings
    
    @staticmethod
    def style_scrollbar(theme, style=None, thumbcolor=None, troughcolor=None, orient="vertical", showarrows=True):
        """Create a default scrollbar style.

        Args:
            theme (str): The theme name.
            style (str, optional): The style used to render the widget.
            thumbcolor (str, optional): The color of the scrollbar thumb.
            troughcolor (str, optional): The color of the scrollbar trough.
            orient (str, optional): The orientation of the scrollbar; either 'horizontal' or 'vertical'.
            showarrows (bool, optional): Whether to include or exclude arrow buttons. Ignored for rounded styles.

        Returns:
            dict: A dictionary of theme settings.
        """
        settings = dict()

        # fallback colors
        if theme.type == "light":
            fallback = ThemeColors.update_hsv(theme.colors.bg, vd=-0.25)
            thumbcolor = ThemeColors.normalize(thumbcolor, fallback, theme.colors)
        else:
            fallback = ThemeColors.update_hsv(theme.colors.selectbg, vd=0.35, sd=-0.1)
            thumbcolor = ThemeColors.normalize(thumbcolor, fallback, theme.colors)
        troughcolor = ThemeColors.normalize(troughcolor, ThemeColors.update_hsv(theme.colors.bg, vd=0.2), theme.colors)

        # images
        element = style.replace("TScrollbar", "Scrollbar")

        if "rounded" in style.lower():
            arrows = False  # no arrows on a rounded scrollbar
            StylerTTK.style_rounded_scrollbar_images(thumbcolor, troughcolor, 12, element, theme)
        else:
            StylerTTK.style_default_scrollbar_images(thumbcolor, troughcolor, 16, element, theme)

        thumb_normal = StylerTTK.theme_images[f"{element}.normal"]
        thumb_pressed = StylerTTK.theme_images[f"{element}.pressed"]
        thumb_active = StylerTTK.theme_images[f"{element}.active"]
        trough = StylerTTK.theme_images[f"{element}.trough"]

        # create style settings
        settings.update(
            {
                f"{element}.thumb": {
                    "element create": (
                        "image",
                        thumb_normal,
                        ("pressed", thumb_pressed),
                        ("active", thumb_active),
                        {"border": 5, "padding": 0},
                    )
                },
                f"{element}.trough": {"element create": ("image", trough, {"border": (5, 5, 5, 5), "padding": (1, 0, 1, 0)})},
            }
        )

        ## horizontal orientation
        if orient.lower() == "horizontal":
            ### without arrow buttons
            if not showarrows:
                settings.update(
                    {
                        style: {
                            "layout": [
                                (
                                    f"{element}.trough",
                                    {
                                        "sticky": "we",
                                        "children": [(f"{element}.thumb", {"expand": "1", "sticky": "nswe"})],
                                    },
                                )
                            ]
                        }
                    }
                )
            ### with arrow buttons
            else:
                StylerTTK.style_arrows(thumbcolor, "horizontal", element)
                leftarrow = StylerTTK.theme_images[f"{element}.leftarrow"]
                rightarrow = StylerTTK.theme_images[f"{element}.rightarrow"]
                settings.update(
                    {
                        f"{element}.leftarrow": {"element create": ("image", leftarrow)},
                        f"{element}.rightarrow": {"element create": ("image", rightarrow)},
                        style: {
                            "layout": [
                                (
                                    f"{element}.trough",
                                    {
                                        "sticky": "we",
                                        "children": [
                                            (f"{element}.leftarrow", {"side": "left", "sticky": ""}),
                                            (f"{element}.rightarrow", {"side": "right", "sticky": ""}),
                                            (f"{element}.thumb", {"expand": "1", "sticky": "nswe"}),
                                        ],
                                    },
                                )
                            ]
                        },
                    }
                )

        ## vertical orientation
        else:
            ### without arrow buttons
            if not showarrows:
                settings.update(
                    {
                        style: {
                            "layout": [
                                (
                                    f"{element}.trough",
                                    {
                                        "sticky": "ns",
                                        "children": [(f"{element}.thumb", {"expand": "1", "sticky": "nswe"})],
                                    },
                                )
                            ]
                        }
                    }
                )
            ### with arrow buttons
            else:
                StylerTTK.style_arrows(thumbcolor, "vertical", element)
                uparrow = StylerTTK.theme_images[f"{element}.uparrow"]
                downarrow = StylerTTK.theme_images[f"{element}.downarrow"]
                settings.update(
                    {
                        f"{element}.uparrow": {"element create": ("image", uparrow)},
                        f"{element}.downarrow": {"element create": ("image", downarrow)},
                        style: {
                            "layout": [
                                (
                                    f"{element}.trough",
                                    {
                                        "sticky": "ns",
                                        "children": [
                                            (f"{element}.uparrow", {"side": "top", "sticky": ""}),
                                            (f"{element}.downarrow", {"side": "bottom", "sticky": ""}),
                                            (f"{element}.thumb", {"expand": "1", "sticky": "nswe"}),
                                        ],
                                    },
                                )
                            ]
                        },
                    }
                )

        return settings

    @staticmethod
    def style_default_scrollbar_images(thumbcolor, troughcolor, thickness, element, theme):
        """Create image assets for squared scrollbar widget

        Args:
            thumbcolor (str): The color of the scrollbar thumb.
            troughcolor (str): The color of the scrollbar trough.
            thickness (int): The thickness of the short side in pixels.
            element (str): A unique style element identifier.
        """
        pressed = ThemeColors.update_hsv(thumbcolor, vd=-0.35 if theme.type == "light" else 0.35)
        active = ThemeColors.update_hsv(thumbcolor, vd=-0.25 if theme.type == "light" else 0.25)
        w = thickness
        h = thickness * 2

        if "vertical" in element.lower():
            img_normal = ImageTk.PhotoImage(Image.new("RGB", (w, h), thumbcolor))
            StylerTTK.theme_images[f"{element}.normal"] = img_normal

            img_pressed = ImageTk.PhotoImage(Image.new("RGB", (w, h), pressed))
            StylerTTK.theme_images[f"{element}.pressed"] = img_pressed

            img_active = ImageTk.PhotoImage(Image.new("RGB", (w, h), active))
            StylerTTK.theme_images[f"{element}.active"] = img_active

            img_trough = ImageTk.PhotoImage(Image.new("RGB", (w+1, h+1), troughcolor))
            StylerTTK.theme_images[f"{element}.trough"] = img_trough

        else:
            img_normal = ImageTk.PhotoImage(Image.new("RGB", (h, w), thumbcolor))
            StylerTTK.theme_images[f"{element}.normal"] = img_normal

            img_pressed = ImageTk.PhotoImage(Image.new("RGB", (h, w), pressed))
            StylerTTK.theme_images[f"{element}.pressed"] = img_pressed

            img_active = ImageTk.PhotoImage(Image.new("RGB", (h, w), active))
            StylerTTK.theme_images[f"{element}.active"] = img_active

            img_trough = ImageTk.PhotoImage(Image.new("RGB", (h+1, w+1), troughcolor))
            StylerTTK.theme_images[f"{element}.trough"] = img_trough

    @staticmethod
    def style_rounded_scrollbar_images(thumbcolor, troughcolor, thickness, element, theme):
        """Create image assets for rounded scrollbar widget

        Args:
            thumbcolor (str): The color of the scrollbar thumb.
            troughcolor (str): The color of the scrollbar trough.
            thickness (int): The thickness of the short side in pixels.
            element (str): A unique style element identifier.
        """
        pressed = ThemeColors.update_hsv(thumbcolor, vd=-0.35 if theme.type == "light" else 0.35)
        active = ThemeColors.update_hsv(thumbcolor, vd=-0.25 if theme.type == "light" else 0.25)
        troughoutline = ThemeColors.update_hsv(troughcolor, vd=-0.25)
        thumboutline = ThemeColors.update_hsv(thumbcolor, vd=-0.25)

        w = thickness
        h = thickness * 2

        if "vertical" in element.lower():
            img = Image.new("RGBA", (500, 1000))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((3, 3, 497, 997), radius=498, fill=thumbcolor, outline=thumboutline, width=10)
            StylerTTK.theme_images[f"{element}.normal"] = ImageTk.PhotoImage(img.resize((w, h), Image.CUBIC))

            img = Image.new("RGBA", (500, 1000))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((3, 3, 497, 997), radius=498, fill=pressed)
            StylerTTK.theme_images[f"{element}.pressed"] = ImageTk.PhotoImage(img.resize((w, h), Image.CUBIC))

            img = Image.new("RGBA", (500, 1000))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((1, 1, 497, 997), radius=498, fill=active)
            StylerTTK.theme_images[f"{element}.active"] = ImageTk.PhotoImage(img.resize((w, h), Image.CUBIC))

            img = Image.new("RGBA", (500, 1000))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((1, 1, 499, 999), radius=498, fill=troughcolor, outline=troughoutline, width=10)
            StylerTTK.theme_images[f"{element}.trough"] = ImageTk.PhotoImage(img.resize((w+1, h+1), Image.CUBIC))

        else:
            img = Image.new("RGBA", (1000, 500))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((1, 1, 999, 499), radius=498, fill=thumbcolor, outline=thumboutline, width=10)
            StylerTTK.theme_images[f"{element}.normal"] = ImageTk.PhotoImage(img.resize((h, w), Image.CUBIC))

            img = Image.new("RGBA", (1000, 500))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((1, 1, 999, 499), radius=498, fill=pressed)
            StylerTTK.theme_images[f"{element}.pressed"] = ImageTk.PhotoImage(img.resize((h, w), Image.CUBIC))

            img = Image.new("RGBA", (1000, 500))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((1, 1, 999, 499), radius=498, fill=active)
            StylerTTK.theme_images[f"{element}.active"] = ImageTk.PhotoImage(img.resize((h, w), Image.CUBIC))

            img = Image.new("RGBA", (1000, 500))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((1, 1, 999, 499), radius=498, fill=troughcolor, outline=troughoutline, width=10)
            StylerTTK.theme_images[f"{element}.trough"] = ImageTk.PhotoImage(img.resize((h+1, w+1), Image.CUBIC))

    @staticmethod
    def style_arrows(arrowcolor, orient, element):
        """Create horizontal or vertical arrow images to be used for buttons

        Args:
            arrowcolor (str): The color of the arrow.
            orient (str): One of 'horizontal' or 'vertical'.
            element (str): A unique element identifier to associate with the images.
        """
        img = Image.new("RGBA", (16, 16))
        draw = ImageDraw.Draw(img)

        draw.line([5, 8, 5, 11], fill=arrowcolor)
        draw.line([6, 7, 6, 10], fill=arrowcolor)
        draw.line([7, 6, 7, 9], fill=arrowcolor)
        draw.line([8, 5, 8, 8], fill=arrowcolor)
        draw.line([9, 6, 9, 9], fill=arrowcolor)
        draw.line([10, 7, 10, 10], fill=arrowcolor)
        draw.line([11, 8, 11, 11], fill=arrowcolor)

        if orient.lower() == "vertical":
            StylerTTK.theme_images[f"{element}.uparrow"] = ImageTk.PhotoImage(img)
            StylerTTK.theme_images[f"{element}.downarrow"] = ImageTk.PhotoImage(img.rotate(180))
        else:
            StylerTTK.theme_images[f"{element}.leftarrow"] = ImageTk.PhotoImage(img.rotate(90))
            StylerTTK.theme_images[f"{element}.rightarrow"] = ImageTk.PhotoImage(img.rotate(-90))

    @staticmethod
    def style_spinbox(theme, background=None, font=DEFAULT_FONT, foreground=None, focuscolor=None, style=None):
        """Create a spinbox style.

        Args:
            theme (str): The theme name.
            background (str, optional): The color of the entry background.
            focuscolor (str, optional): The color of the focus ring when the widget has focus.
            font (str, optional): The font used to render the widget text.
            foreground (str, optional): The color of the widget text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.inputbg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.inputfg, theme.colors)
        focuscolor = ThemeColors.normalize(focuscolor, theme.colors.primary, theme.colors)
        disabled_fg = ThemeColors.update_hsv(foreground, vd=-0.2 if theme.type == "light" else -0.3)

        # style settings
        settings = dict()
        element = uuid4()
        if theme.type == "dark":  # prevent corners from shining through on dark theme
            settings.update({f"{element}.Spinbox.field": {"element create": ("from", "default")}})

        # use the arrows from the default theme ... they just look better.
        settings.update({f"{element}.Spinbox.uparrow": {"element create": ("from", "default")}})
        settings.update({f"{element}.Spinbox.downarrow": {"element create": ("from", "default")}})

        settings.update(
            {
                style: {
                    "layout": [
                        (
                            f"{element}.Spinbox.field",
                            {
                                "side": "top",
                                "sticky": "we",
                                "children": [
                                    (
                                        "null",
                                        {
                                            "side": "right",
                                            "sticky": "",
                                            "children": [
                                                (f"{element}.Spinbox.uparrow", {"side": "top", "sticky": "e"}),
                                                (f"{element}.Spinbox.downarrow", {"side": "bottom", "sticky": "e"}),
                                            ],
                                        },
                                    ),
                                    (
                                        "Spinbox.padding",
                                        {
                                            "sticky": "nswe",
                                            "children": [("Spinbox.textarea", {"sticky": "nswe"})],
                                        },
                                    ),
                                ],
                            },
                        )
                    ],
                    "configure": {
                        "arrowsize": 14,
                        "arrowcolor": foreground,
                        "bordercolor": theme.colors.border,
                        "darkcolor": background,
                        "lightcolor": background,
                        "foreground": foreground,
                        "font": font,
                        "fieldbackground ": background,
                        "background ": background,
                        "relief": "flat",
                        "borderwidth ": 0,  # only applies to dark theme border
                        "padding": 5,
                    },
                    "map": {
                        "arrowcolor": [
                            ("disabled", disabled_fg),
                            ("pressed", focuscolor),
                            ("focus", foreground),
                            ("hover", focuscolor),
                        ],
                        "bordercolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", focuscolor),
                        ],
                        "darkcolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", background),
                        ],
                        "foreground": [("disabled", disabled_fg)],
                        "lightcolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", background),
                        ],
                    },
                },
            }
        )
        return settings

    @staticmethod
    def style_treeitem():
        """Create a global adjustment for the tree item indicator. This widget is only created once per theme."""
        return {"Treeitem.indicator": {"element create": ("from", "alt")}}

    @staticmethod
    def style_treeview(theme, headerbackground=None, headerfont='helvetica 10 bold', headerforeground=None, inputbackground=None, inputfont=DEFAULT_FONT, inputforeground=None,  style=None):
        """Create at treeview style.

        Args:
            theme (str): The theme name.
            headerbackground (str): The header background color.
            headerfont (str): The font used to render the widget text.
            headerforeground (str): The header text color.
            inputbackground (str): The field background color.
            inputfont (str): The field cell font.
            inputforeground (str): The field text color.
            style (str): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        headerbackground = ThemeColors.normalize(headerbackground, theme.colors.primary, theme.colors)
        headerforeground = ThemeColors.normalize(headerforeground, theme.colors.selectfg, theme.colors)
        inputbackground = ThemeColors.normalize(inputbackground, theme.colors.inputbg, theme.colors)
        inputforeground = ThemeColors.normalize(inputforeground, theme.colors.inputfg, theme.colors)
        disabled_fg = ThemeColors.update_hsv(inputforeground, vd=-0.2 if theme.type == "light" else -0.3)

        # style settings
        settings = dict()
        settings.update({
            style: {
                "layout": [
                    ("Button.border", {"sticky": "nswe", "border": "1", "children": [
                            ("Treeview.padding", {"sticky": "nswe", "children": [
                                    ("Treeview.treearea", {"sticky": "nswe"})],
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                    "configure": {
                        "background": inputbackground,
                        "foreground": inputforeground,
                        "font": inputfont,
                        "borderwidth": 0,
                        "padding": 0,
                    },
                    "map": {
                        "background": [("selected", theme.colors.selectbg)],
                        "foreground": [("disabled", disabled_fg), ("selected", theme.colors.selectfg)],
                    },
                },
                f"{style}.Heading": {
                    "configure": {
                        "background": headerbackground,
                        "foreground": headerforeground,
                        "padding": (0, 5),
                        "font": headerfont,
                    }
                },
            }
        )
        return settings

    @staticmethod
    def style_frame(theme, background=None, style=None):
        """Create a frame style.

        Args:
            theme (str): The theme name.
            background (str, optional): The color of the frame background.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        settings = dict()
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        settings.update({style: {"configure": {"background": background}}})
        return settings

    @staticmethod
    def style_button(theme, anchor="center", background=None, font=DEFAULT_FONT, foreground=None, style=None):
        """Create a solid button style.

        Args:
            theme (str): The theme name.
            anchor (str, optional): The position of the text inside of the button.
            background (str, optional): The color of the button background.
            font (str, optional): The font used to render the button text.
            foreground (str, optional): The color of the button text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        foreground = ThemeColors.normalize(foreground, theme.colors.selectfg, theme.colors)
        background = ThemeColors.normalize(background, theme.colors.primary, theme.colors)
        pressed = ThemeColors.update_hsv(background, vd=-0.2 if theme.type == "light" else 0.2)
        hover = ThemeColors.update_hsv(background, vd=-0.1 if theme.type == "light" else 0.1)
        disabled_bg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)
        disabled_fg = theme.colors.inputfg

        # style settings
        settings = dict()
        settings.update(
            {
                f"{style}": {
                    "configure": {
                        "anchor": anchor,
                        "foreground": foreground,
                        "background": background,
                        "bordercolor": background,
                        "darkcolor": background,
                        "lightcolor": background,
                        "relief": "raised",
                        "font": font,
                        "focusthickness": 0,
                        "focuscolor": "",
                        "padding": (10, 5),
                    },
                    "map": {
                        "foreground": [("disabled", disabled_fg)],
                        "background": [
                            ("disabled", disabled_bg),
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                        "bordercolor": [
                            ("disabled", disabled_bg),
                            ("hover !disabled", hover),
                        ],
                        "darkcolor": [
                            ("disabled", disabled_bg),
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                        "lightcolor": [
                            ("disabled", disabled_bg),
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                    },
                }
            }
        )
        return settings

    @staticmethod
    def style_outline_button(theme, anchor='center', background=None, font=DEFAULT_FONT, foreground=None, style=None):
        """Create an outline button style.

        Args:
            theme (str): The theme name.
            anchor (str, optional): The position of the text inside of the button.
            background (str, optional): The color of the button background.
            font (str, optional): The font used to render the button text.
            foreground (str, optional): The color of the outline and button text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.primary, theme.colors)
        pressed = ThemeColors.update_hsv(foreground, vd=-0.1 if theme.type == "light" else 0.1)
        select_fg = theme.colors.selectfg
        disabled_fg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # style settings
        settings = dict()
        settings.update(
            {
                f"{style}": {
                    "configure": {
                        "anchor": anchor,
                        "foreground": foreground,
                        "background": background,
                        "bordercolor": foreground,
                        "darkcolor": background,
                        "lightcolor": background,
                        "relief": "raised",
                        "font": font,
                        "focusthickness": 0,
                        "focuscolor": "",
                        "padding": (10, 5),
                    },
                    "map": {
                        "foreground": [("disabled", disabled_fg), ("pressed", select_fg), ("hover", select_fg)],
                        "background": [
                            ("pressed !disabled", pressed),
                            ("hover !disabled", foreground),
                        ],
                        "bordercolor": [
                            ("pressed !disabled", pressed),
                            ("hover !disabled", foreground),
                        ],
                        "darkcolor": [
                            ("pressed !disabled", pressed),
                            ("hover !disabled", foreground),
                        ],
                        "lightcolor": [
                            ("pressed !disabled", pressed),
                            ("hover !disabled", foreground),
                        ],
                    },
                }
            }
        )
        return settings

    @staticmethod
    def style_link_button(theme, anchor="center", background=None, font=DEFAULT_FONT, foreground=None, style=None):
        """Apply a hyperlink style to ttk button: *ttk.Button*

        Args:
            theme (str): The theme name.
            anchor (str, optional): The position of the text inside of the button.
            background (str, optional): The color of the button background.
            font (str, optional): The font used to render the button text.
            foreground (str, optional): The color of the button text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.fg, theme.colors)
        disabled_fg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # style settings
        settings = dict()
        settings.update(
            {
                f"{style}": {
                    "configure": {
                        "anchor": anchor,
                        "foreground": foreground,
                        "background": background,
                        "bordercolor": background,
                        "darkcolor": background,
                        "lightcolor": background,
                        "relief": "raised",
                        "font": font,
                        "focusthickness": 0,
                        "focuscolor": "",
                        "padding": (10, 5),
                    },
                    "map": {
                        "foreground": [
                            ("disabled", disabled_fg),
                            ("pressed !disabled", theme.colors.info),
                            ("hover !disabled", theme.colors.info),
                        ],
                        "shiftrelief": [("pressed !disabled", -1)],
                        "background": [],
                        "bordercolor": [],
                        "darkcolor": [],
                        "lightcolor": [],
                    },
                }
            }
        )
        return settings

    @staticmethod
    def style_toolbutton(theme, anchor="center", font=DEFAULT_FONT, foreground=None, indicatorcolor=None, style=None):
        """Apply a solid color style to ttk widgets that use the Toolbutton style (for example, a checkbutton:
        *ttk.Checkbutton*)

        Args:
            theme (str): The theme name.
            anchor (str, optional): The position of the text inside of the button.
            indicatorcolor (str, optional): Corresponds to the color of the button background when selected.
            font (str, optional): The font used to render the button text.
            foreground (str, optional): The color of the button text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background_on = ThemeColors.normalize(indicatorcolor, theme.colors.primary, theme.colors)
        background_off = ThemeColors.update_hsv(background_on, sd=-0.5, vd=0.1)
        foreground = ThemeColors.normalize(foreground, theme.colors.selectfg, theme.colors)
        disabled_bg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)
        disabled_fg = theme.colors.inputfg

        # style settings
        settings = dict()
        settings.update(
            {
                f"{style}": {
                    "configure": {
                        "anchor": anchor or "center",
                        "foreground": foreground,
                        "background": background_off,
                        "bordercolor": background_off,
                        "darkcolor": background_off,
                        "lightcolor": background_off,
                        "relief": "raised",
                        "font": font,
                        "focusthickness": 0,
                        "focuscolor": "",
                        "padding": (10, 5),
                    },
                    "map": {
                        "foreground": [("disabled", disabled_fg)],
                        "background": [
                            ("disabled", disabled_bg),
                            ("pressed", background_on),
                            ("selected", background_on),
                            ("hover", background_on),
                        ],
                        "bordercolor": [
                            ("disabled", disabled_bg),
                            ("pressed", background_on),
                            ("selected", background_on),
                            ("hover", background_on),
                        ],
                        "darkcolor": [
                            ("disabled", disabled_bg),
                            ("pressed", background_on),
                            ("selected", background_on),
                            ("hover", background_on),
                        ],
                        "lightcolor": [
                            ("disabled", disabled_bg),
                            ("pressed", background_on),
                            ("selected", background_on),
                            ("hover", background_on),
                        ],
                    },
                }
            }
        )
        return settings

    @staticmethod
    def style_outline_toolbutton(
        theme, anchor="center", background=None, font=DEFAULT_FONT, indicatorcolor=None, style=None
    ):
        """Apply an outline style to widgets that use the Toolbutton style (radiobutton, checkbutton)

        Args:
            theme (str): The theme name.
            anchor (str, optional): The position of the text inside of the button.
            background (str, optional): The inner fill of the button when not selected.
            indicatorcolor (str, optional): The outline and foreground color when selected.
            font (str, optional): The font used to render the button text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background_on = ThemeColors.normalize(indicatorcolor, theme.colors.primary, theme.colors)
        background_off = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        background_over = ThemeColors.update_hsv(background_on, vd=-0.1)
        foreground_off = ThemeColors.normalize(indicatorcolor, theme.colors.selectfg, theme.colors)
        foreground_on = background_off
        disabled_fg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # style settings
        settings = dict()
        settings.update(
            {
                f"{style}": {
                    "configure": {
                        "anchor": anchor or "center",
                        "foreground": foreground_off,
                        "background": background_off,
                        "bordercolor": theme.colors.border,
                        "darkcolor": background_off,
                        "lightcolor": background_off,
                        "relief": "raised",
                        "font": font,
                        "focusthickness": 0,
                        "focuscolor": "",
                        "padding": (10, 5),
                    },
                    "map": {
                        "foreground": [
                            ("disabled", disabled_fg),
                            ("pressed", foreground_on),
                            ("selected", foreground_on),
                            ("hover", foreground_on),
                        ],
                        "background": [
                            ("pressed", background_over),
                            ("selected", background_over),
                            ("hover", background_on),
                        ],
                        "bordercolor": [
                            ("disabled", disabled_fg),
                            ("pressed", background_over),
                            ("selected", background_over),
                            ("hover", background_on),
                        ],
                        "darkcolor": [
                            ("pressed", background_over),
                            ("selected", background_over),
                            ("hover", background_on),
                        ],
                        "lightcolor": [
                            ("pressed", background_over),
                            ("selected", background_over),
                            ("hover", background_on),
                        ],
                    },
                }
            }
        )
        return settings

    @staticmethod
    def style_entry(theme, background=None, font=DEFAULT_FONT, foreground=None, focuscolor=None, style=None):
        """Create an entry style.

        Args:
            theme (str): The theme name.
            background (str, optional): The color of the entry background.
            focuscolor (str, optional): The color of the focus ring when the widget has focus.
            font (str, optional): The font used to render the widget text.
            foreground (str, optional): The color of the widget text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.inputbg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.inputfg, theme.colors)
        focuscolor = ThemeColors.normalize(focuscolor, theme.colors.primary, theme.colors)
        disabled_fg = ThemeColors.update_hsv(foreground, vd=-0.2 if theme.type == "light" else -0.3)

        # style settings
        settings = dict()
        if theme.type == "dark":  # use Entry field from dark theme to prevent corners from shining through
            settings.update({"Entry.field": {"element create": ("from", "default")}})

        settings.update(
            {
                style: {
                    "configure": {
                        "bordercolor": theme.colors.border,
                        "darkcolor": background,
                        "lightcolor": background,
                        "foreground": foreground,
                        "font": font,
                        "fieldbackground ": background,
                        "background ": background,
                        "relief": "flat",
                        "borderwidth ": 0,  # only applies to dark theme border
                        "padding": 5,
                    },
                    "map": {
                        "foreground": [("disabled", disabled_fg)],
                        "bordercolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", focuscolor),
                        ],
                        "lightcolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", background),
                        ],
                        "darkcolor": [
                            ("focus !disabled", focuscolor),
                            ("hover !disabled", background),
                        ],
                    },
                },
            }
        )
        return settings

    @staticmethod
    def style_radiobutton(theme, background=None, font=DEFAULT_FONT, foreground=None, indicatorcolor=None, style=None):
        """Create an image-based radiobutton style.

        Args:
            theme (ThemeSettings): The current theme.
            background (str, optional): The normal color of the widget background.
            font (str, optional): The font used to render the button text.
            foreground (str, optional): The text color.
            indicatorcolor (str, optional): The color of the widget indicator.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.fg, theme.colors)
        indicatorcolor = ThemeColors.normalize(indicatorcolor, theme.colors.primary, theme.colors)
        disabled = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # images
        element = uuid4()
        StylerTTK.style_radiobutton_images(theme, indicatorcolor, element)
        radio_off = StylerTTK.theme_images[f"{element}_radio_off"]
        radio_on = StylerTTK.theme_images[f"{element}_radio_on"]
        radio_disabled = StylerTTK.theme_images[f"{element}_radio_disabled"]

        # style settings
        settings = dict()
        settings.update(
            {
                f"{element}.Radiobutton.indicator": {
                    "element create": (
                        "image",
                        radio_on,
                        ("disabled", radio_disabled),
                        ("!selected", radio_off),
                        {"width": 20, "border": 4, "sticky": "w"},
                    )
                },
                style: {
                    "configure": {
                        "background": background,
                        "foreground": foreground,
                        "focuscolor": "",
                        "font": font or DEFAULT_FONT,
                    },
                    "layout": [
                        (
                            "Radiobutton.padding",
                            {
                                "children": [
                                    (f"{element}.Radiobutton.indicator", {"side": "left", "sticky": ""}),
                                    (
                                        "Radiobutton.focus",
                                        {
                                            "children": [("Radiobutton.label", {"sticky": "nswe"})],
                                            "side": "left",
                                            "sticky": "",
                                        },
                                    ),
                                ],
                                "sticky": "nswe",
                            },
                        )
                    ],
                    "map": {
                        "foreground": [
                            ("disabled", disabled),
                            ("active", ThemeColors.update_hsv(indicatorcolor, vd=-0.2)),
                        ]
                    },
                },
            }
        )
        return settings

    @staticmethod
    def style_radiobutton_images(theme, indicatorcolor, element):
        """ "Create assets for radiobutton layout

        Args:
            theme (ThemeSettings): The current theme.
            indicator_color (str): The indicator color.
            element (UUID): A unique element identification number.
        """
        outline = theme.colors.selectbg
        fill = theme.colors.inputbg if theme.type == "light" else theme.colors.selectfg
        disabled_fg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)
        disabled_bg = theme.colors.inputbg if theme.type == "light" else disabled_fg

        # radiobutton off
        radio_off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(radio_off)
        draw.ellipse([2, 2, 132, 132], outline=outline, width=3, fill=fill)

        # radiobutton on
        radio_on = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(radio_on)
        if theme.type == "light":
            draw.ellipse([2, 2, 132, 132], outline=indicatorcolor, width=3, fill=indicatorcolor)
            draw.ellipse([40, 40, 94, 94], fill=fill)
        else:
            draw.ellipse([2, 2, 132, 132], outline=indicatorcolor, width=3, fill=fill)
            draw.ellipse([30, 30, 104, 104], fill=indicatorcolor)

        # radiobutton disabled
        radio_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(radio_disabled)
        draw.ellipse([2, 2, 132, 132], outline=disabled_fg, width=3, fill=disabled_bg)

        # save images
        StylerTTK.theme_images.update(
            {
                f"{element}_radio_off": ImageTk.PhotoImage(radio_off.resize((14, 14)), Image.LANCZOS),
                f"{element}_radio_on": ImageTk.PhotoImage(radio_on.resize((14, 14)), Image.LANCZOS),
                f"{element}_radio_disabled": ImageTk.PhotoImage(radio_disabled.resize((14, 14)), Image.LANCZOS),
            }
        )

    def _style_calendar(self):
        """Create style configuration for the ttkbootstrap.widgets.datechooser

        The options available in this widget include:

            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        # disabled settings
        disabled_fg = (
            ThemeColors.update_hsv(self.theme.colors.inputbg, vd=-0.2)
            if self.theme.type == "light"
            else ThemeColors.update_hsv(self.theme.colors.inputbg, vd=-0.3)
        )

        # pressed and hover settings
        pressed_vd = -0.10

        self.settings.update(
            {
                "TCalendar": {
                    "layout": [
                        (
                            "Toolbutton.border",
                            {
                                "sticky": "nswe",
                                "children": [
                                    (
                                        "Toolbutton.padding",
                                        {
                                            "sticky": "nswe",
                                            "children": [("Toolbutton.label", {"sticky": "nswe"})],
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                    "configure": {
                        "foreground": self.theme.colors.fg,
                        "background": self.theme.colors.bg,
                        "bordercolor": self.theme.colors.bg,
                        "darkcolor": self.theme.colors.bg,
                        "lightcolor": self.theme.colors.bg,
                        "relief": "raised",
                        "font": self.theme.font,
                        "focusthickness": 0,
                        "focuscolor": "",
                        "borderwidth": 1,
                        "anchor": "center",
                        "padding": (10, 5),
                    },
                    "map": {
                        "foreground": [
                            ("disabled", disabled_fg),
                            ("pressed !disabled", self.theme.colors.selectfg),
                            ("selected !disabled", self.theme.colors.selectfg),
                            ("hover !disabled", self.theme.colors.selectfg),
                        ],
                        "background": [
                            (
                                "pressed !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            (
                                "selected !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            ("hover !disabled", self.theme.colors.primary),
                        ],
                        "bordercolor": [
                            ("disabled", disabled_fg),
                            (
                                "pressed !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            (
                                "selected !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            ("hover !disabled", self.theme.colors.primary),
                        ],
                        "darkcolor": [
                            (
                                "pressed !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            (
                                "selected !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            ("hover !disabled", self.theme.colors.primary),
                        ],
                        "lightcolor": [
                            (
                                "pressed !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            (
                                "selected !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            ("hover !disabled", self.theme.colors.primary),
                        ],
                    },
                },
                "chevron.TButton": {"configure": {"font": "helvetica 14"}},
            }
        )

        for color in self.theme.colors:
            self.settings.update(
                {
                    f"{color}.TCalendar": {
                        "configure": {
                            "foreground": self.theme.colors.fg,
                            "background": self.theme.colors.bg,
                            "bordercolor": self.theme.colors.bg,
                            "darkcolor": self.theme.colors.bg,
                            "lightcolor": self.theme.colors.bg,
                            "relief": "raised",
                            "focusthickness": 0,
                            "focuscolor": "",
                            "borderwidth": 1,
                            "padding": (10, 5),
                        },
                        "map": {
                            "foreground": [
                                ("disabled", disabled_fg),
                                ("pressed !disabled", self.theme.colors.selectfg),
                                ("selected !disabled", self.theme.colors.selectfg),
                                ("hover !disabled", self.theme.colors.selectfg),
                            ],
                            "background": [
                                (
                                    "pressed !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                (
                                    "selected !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                ("hover !disabled", self.theme.colors.get(color)),
                            ],
                            "bordercolor": [
                                ("disabled", disabled_fg),
                                (
                                    "pressed !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                (
                                    "selected !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                ("hover !disabled", self.theme.colors.get(color)),
                            ],
                            "darkcolor": [
                                (
                                    "pressed !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                (
                                    "selected !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                ("hover !disabled", self.theme.colors.get(color)),
                            ],
                            "lightcolor": [
                                (
                                    "pressed !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                (
                                    "selected !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                ("hover !disabled", self.theme.colors.get(color)),
                            ],
                        },
                    },
                    f"chevron.{color}.TButton": {"configure": {"font": "helvetica 14"}},
                }
            )

    def _style_exit_button(self):
        """Create style configuration for the toolbutton exit button"""
        disabled_bg = (
            ThemeColors.update_hsv(self.theme.colors.inputbg, vd=-0.2)
            if self.theme.type == "light"
            else ThemeColors.update_hsv(self.theme.colors.inputbg, vd=-0.3)
        )
        pressed_vd = -0.2

        self.settings.update(
            {
                "exit.TButton": {
                    "configure": {"relief": "flat", "font": "helvetica 12"},
                    "map": {
                        "background": [
                            ("disabled", disabled_bg),
                            (
                                "pressed !disabled",
                                ThemeColors.update_hsv(self.theme.colors.primary, vd=pressed_vd),
                            ),
                            ("hover !disabled", self.theme.colors.danger),
                        ]
                    },
                }
            }
        )

        for color in self.theme.colors:
            self.settings.update(
                {
                    f"exit.{color}.TButton": {
                        "configure": {"relief": "flat", "font": "helvetica 12"},
                        "map": {
                            "background": [
                                ("disabled", disabled_bg),
                                (
                                    "pressed !disabled",
                                    ThemeColors.update_hsv(self.theme.colors.get(color), vd=pressed_vd),
                                ),
                                ("hover !disabled", self.theme.colors.danger),
                            ]
                        },
                    }
                }
            )

    def _style_meter(self):
        """Create style configuration for the ttkbootstrap.widgets.meter

        The options available in this widget include:

            - Label.border: bordercolor, lightcolor, darkcolor, relief, borderwidth
            - Label.padding: padding, relief, shiftrelief
            - Label.label: compound, space, text, font, foreground, underline, width, anchor, justify, wraplength,
                embossed, image, stipple, background
        """
        self.settings.update(
            {
                "TMeter": {
                    "layout": [
                        (
                            "Label.border",
                            {
                                "sticky": "nswe",
                                "border": "1",
                                "children": [
                                    (
                                        "Label.padding",
                                        {
                                            "sticky": "nswe",
                                            "border": "1",
                                            "children": [("Label.label", {"sticky": "nswe"})],
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                    "configure": {"foreground": self.theme.colors.fg, "background": self.theme.colors.bg},
                }
            }
        )

        for color in self.theme.colors:
            self.settings.update({f"{color}.TMeter": {"configure": {"foreground": self.theme.colors.get(color)}}})

    @staticmethod
    def style_label(theme, background=None, font=DEFAULT_FONT, foreground=None, style=None):
        """Create a label style.

        Args:
            theme (str): The theme name.
            background (str, optional): The color of the label background.
            font (str, optional): The font used to render the label text.
            foreground (str, optional): The color of the text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        fallbackfg = theme.colors.selectfg if "inverse" in style.lower() else theme.colors.fg
        foreground = ThemeColors.normalize(foreground, fallbackfg, theme.colors)

        # style settings
        settings = dict()
        settings.update({style: {"configure": {"foreground": foreground, "background": background, "font": font}}})
        return settings

    @staticmethod
    def style_labelframe(theme, background=None, bordercolor=None, foreground=None, style=None):
        """Create a labelframe style.

        Args:
            theme (str): The theme name.
            background (str, optional): The color of the labelframe background.
            bordercolor (str, optional): The color of the labelframe border.
            foreground (str, optional): The color of the label text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        settings = dict()

        # fallback values
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.selectfg, theme.colors)
        borderfallback = theme.colors.border if theme.type == "light" else theme.colors.selectbg
        bordercolor = ThemeColors.normalize(bordercolor, borderfallback, theme.colors)

        # style settings
        settings.update(
            {
                f"{style}.Label": {"configure": {"foreground": foreground, "background": background}},
                style: {
                    "configure": {
                        "relief": "raised",
                        "borderwidth": 1,
                        "bordercolor": bordercolor,
                        "lightcolor": background,
                        "darkcolor": background,
                        "background": background,
                    }
                },
            }
        )
        return settings

    @staticmethod
    def style_roundtoggle(theme, background=None, font=DEFAULT_FONT, foreground=None, indicatorcolor=None, style=None):
        """Create an image-based round togglebutton style.

        Args:
            theme (ThemeSettings): The current theme.
            background (str, optional): The normal color of the widget background.
            font (str, optional): The font used to render the button text.
            foreground (str, optional): The text color.
            indicatorcolor (str, optional): The color of the widget indicator.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.fg, theme.colors)
        indicatorcolor = ThemeColors.normalize(indicatorcolor, theme.colors.primary, theme.colors)
        disabled = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # create widget images
        element = uuid4()
        StylerTTK.style_roundtoggle_images(theme, indicatorcolor, element)
        toggle_off = StylerTTK.theme_images[f"{element}_toggle_off"]
        toggle_on = StylerTTK.theme_images[f"{element}_toggle_on"]
        toggle_disabled = StylerTTK.theme_images[f"{element}_toggle_disabled"]

        # style settings
        settings = dict()
        settings.update(
            {
                f"{element}.Roundtoggle.Toolbutton.indicator": {
                    "element create": (
                        "image",
                        toggle_on,
                        ("disabled", toggle_disabled),
                        ("!selected", toggle_off),
                        {"width": 28, "border": 4, "sticky": "w"},
                    )
                },
                style: {
                    "configure": {
                        "background": background,
                        "foreground": foreground,
                        "borderwidth": 0,
                        "relief": "flat",
                        "padding": 0,
                        "font": font,
                    },
                    "layout": [
                        (
                            "Toolbutton.border",
                            {
                                "sticky": "nswe",
                                "children": [
                                    (
                                        "Toolbutton.padding",
                                        {
                                            "sticky": "nswe",
                                            "children": [
                                                (f"{element}.Roundtoggle.Toolbutton.indicator", {"side": "left"}),
                                                ("Toolbutton.label", {"side": "left"}),
                                            ],
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                    "map": {
                        "foreground": [
                            ("disabled", disabled),
                            ("hover", indicatorcolor),
                        ],
                        "background": [("selected", background), ("!selected", background)],
                    },
                },
            }
        )
        return settings

    @staticmethod
    def style_roundtoggle_images(theme, indicatorcolor, element):
        """ "Create assets for roundtoggle layout

        Args:
            theme (ThemeSettings): The current theme.
            indicator_color (str): The indicator color.
            element (UUID): A unique element identification number.
        """
        # fallback colors
        outline = theme.colors.selectbg if theme.type == "light" else theme.colors.inputbg
        indicator_on = theme.colors.selectfg
        indicator_off = theme.colors.selectbg if theme.type == "light" else theme.colors.inputbg
        fill = theme.colors.bg
        disabled = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # toggle off
        toggle_off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_off)
        draw.rounded_rectangle([1, 1, 225, 129], radius=64, outline=outline, width=6, fill=fill)
        draw.ellipse([18, 18, 110, 110], fill=indicator_off)

        # toggle on
        toggle_on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        draw.rounded_rectangle([1, 1, 225, 129], radius=64, outline=indicatorcolor, width=6, fill=indicatorcolor)
        draw.ellipse([18, 18, 110, 110], fill=indicator_on)
        toggle_on = toggle_on.transpose(Image.ROTATE_180)

        # toggle disabled
        toggle_disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_disabled)
        draw.rounded_rectangle([1, 1, 225, 129], radius=64, outline=disabled, width=6, fill=fill)
        draw.ellipse([18, 18, 110, 110], fill=disabled)

        # save images
        StylerTTK.theme_images.update(
            {
                f"{element}_toggle_off": ImageTk.PhotoImage(toggle_off.resize((24, 15)), Image.LANCZOS),
                f"{element}_toggle_on": ImageTk.PhotoImage(toggle_on.resize((24, 15)), Image.LANCZOS),
                f"{element}_toggle_disabled": ImageTk.PhotoImage(toggle_disabled.resize((24, 15)), Image.LANCZOS),
            }
        )

    @staticmethod
    def style_squaretoggle(theme, background=None, font=DEFAULT_FONT, foreground=None, indicatorcolor=None, style=None):
        """Create an image-based square togglebutton style.

        Args:
            theme (ThemeSettings): The current theme.
            background (str, optional): The normal color of the widget background.
            font (str, optional): The font used to render the button text.
            foreground (str, optional): The text color.
            indicatorcolor (str, optional): The color of the widget indicator.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.fg, theme.colors)
        indicatorcolor = ThemeColors.normalize(indicatorcolor, theme.colors.primary, theme.colors)
        disabled_fg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # create widget images
        element = uuid4()
        StylerTTK.style_squaretoggle_images(theme, indicatorcolor, element)
        toggle_off = StylerTTK.theme_images[f"{element}_toggle_off"]
        toggle_on = StylerTTK.theme_images[f"{element}_toggle_on"]
        toggle_disabled = StylerTTK.theme_images[f"{element}_toggle_disabled"]

        # style settings
        settings = dict()
        settings.update(
            {
                f"{element}.Squaretoggle.Toolbutton.indicator": {
                    "element create": (
                        "image",
                        toggle_on,
                        ("disabled", toggle_disabled),
                        ("!selected", toggle_off),
                        {"width": 28, "border": 4, "sticky": "w"},
                    )
                },
                style: {
                    "configure": {
                        "background": background,
                        "foreground": foreground,
                        "borderwidth": 0,
                        "relief": "flat",
                        "padding": 0,
                        "font": font,
                    },
                    "layout": [
                        (
                            "Toolbutton.border",
                            {
                                "sticky": "nswe",
                                "children": [
                                    (
                                        "Toolbutton.padding",
                                        {
                                            "sticky": "nswe",
                                            "children": [
                                                (f"{element}.Squaretoggle.Toolbutton.indicator", {"side": "left"}),
                                                ("Toolbutton.label", {"side": "left"}),
                                            ],
                                        },
                                    )
                                ],
                            },
                        )
                    ],
                    "map": {
                        "foreground": [
                            ("disabled", disabled_fg),
                            ("hover", indicatorcolor),
                        ],
                        "background": [("selected", background), ("!selected", background)],
                    },
                },
            }
        )
        return settings

    @staticmethod
    def style_squaretoggle_images(theme, indicatorcolor, element):
        """ "Create assets for squaretoggle layout

        Args:
            theme (ThemeSettings): The current theme.
            indicator_color (str): The indicator color.
            element (UUID): A unique element identification number.
        """
        # fallback colors
        outline = theme.colors.selectbg if theme.type == "light" else theme.colors.inputbg
        indicator_on = theme.colors.selectfg
        indicator_off = theme.colors.selectbg if theme.type == "light" else theme.colors.inputbg
        disabled = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)
        fill = theme.colors.bg

        # toggle off
        toggle_off = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_off)
        draw.rectangle([1, 1, 225, 129], outline=outline, width=6, fill=fill)
        draw.rectangle([18, 18, 110, 110], fill=indicator_off)

        # toggle on
        toggle_on = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_on)
        draw.rectangle([1, 1, 225, 129], outline=indicatorcolor, width=6, fill=indicatorcolor)
        draw.rectangle([18, 18, 110, 110], fill=indicator_on)
        toggle_on = toggle_on.transpose(Image.ROTATE_180)

        # toggle disabled
        toggle_disabled = Image.new("RGBA", (226, 130))
        draw = ImageDraw.Draw(toggle_disabled)
        draw.rectangle([1, 1, 225, 129], outline=disabled, width=6, fill=fill)
        draw.rectangle([18, 18, 110, 110], fill=disabled)

        # save images
        StylerTTK.theme_images.update(
            {
                f"{element}_toggle_off": ImageTk.PhotoImage(toggle_off.resize((24, 15)), Image.LANCZOS),
                f"{element}_toggle_on": ImageTk.PhotoImage(toggle_on.resize((24, 15)), Image.LANCZOS),
                f"{element}_toggle_disabled": ImageTk.PhotoImage(toggle_disabled.resize((24, 15)), Image.LANCZOS),
            }
        )

    @staticmethod
    def style_checkbutton(theme, background=None, font=DEFAULT_FONT, foreground=None, indicatorcolor=None, style=None):
        """Create an image-based checkbutton style.

        Args:
            theme (ThemeSettings): The current theme.
            background (str, optional): The normal color of the widget background.
            font (str, optional): The font used to render the button text.
            foreground (str, optional): The text color.
            indicatorcolor (str, optional): The color of the widget indicator.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.fg, theme.colors)
        indicatorcolor = ThemeColors.normalize(indicatorcolor, theme.colors.primary, theme.colors)
        disabled = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)

        # create widget images
        element = uuid4()
        StylerTTK.style_checkbutton_images(theme, indicatorcolor, element)
        cb_off = StylerTTK.theme_images[f"{element}_cb_off"]
        cb_on = StylerTTK.theme_images[f"{element}_cb_on"]
        cb_disabled = StylerTTK.theme_images[f"{element}_cb_disabled"]

        # create the widget style
        settings = dict()
        settings.update(
            {
                f"{element}.Checkbutton.indicator": {
                    "element create": (
                        "image",
                        cb_on,
                        ("disabled", cb_disabled),
                        ("!selected", cb_off),
                        {"width": 20, "border": 4, "sticky": "w"},
                    )
                },
                style: {
                    "configure": {
                        "background": background,
                        "foreground": foreground,
                        "focuscolor": "",
                        "font": font,
                    },
                    "layout": [
                        (
                            "Checkbutton.padding",
                            {
                                "children": [
                                    (f"{element}.Checkbutton.indicator", {"side": "left", "sticky": ""}),
                                    (
                                        "Checkbutton.focus",
                                        {
                                            "children": [("Checkbutton.label", {"sticky": "nswe"})],
                                            "side": "left",
                                            "sticky": "",
                                        },
                                    ),
                                ],
                                "sticky": "nswe",
                            },
                        )
                    ],
                    "map": {
                        "foreground": [
                            ("disabled", disabled),
                            ("active", ThemeColors.update_hsv(indicatorcolor, vd=-0.2)),
                        ]
                    },
                },
            }
        )
        return settings

    @staticmethod
    def style_checkbutton_images(theme, indicatorcolor, element):
        """ "Create assets for checkbutton layout

        Args:
            theme (ThemeSettings): The current theme.
            indicator_color (str): The indicator color.
            element (str): A unique element identification number.
        """
        outline = theme.colors.selectbg
        fill = theme.colors.inputbg if theme.type == "light" else theme.colors.selectfg
        disabled_fg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)
        disabled_bg = theme.colors.inputbg if theme.type == "light" else disabled_fg

        # checkbutton off
        cb_off = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(cb_off)
        draw.rounded_rectangle([2, 2, 132, 132], radius=16, outline=outline, width=3, fill=fill)

        # checkbutton on
        with importlib.resources.open_binary("ttkbootstrap.core.files", "Symbola.ttf") as fontpath:
            font = ImageFont.truetype(fontpath, 130)
        cb_on = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(cb_on)
        draw.rounded_rectangle([2, 2, 132, 132], radius=16, outline=indicatorcolor, width=3, fill=indicatorcolor)
        draw.text((20, 8), "✓", font=font, fill=theme.colors.selectfg)

        # checkbutton disabled
        cb_disabled = Image.new("RGBA", (134, 134))
        draw = ImageDraw.Draw(cb_disabled)
        draw.rounded_rectangle([2, 2, 132, 132], radius=16, outline=disabled_fg, width=3, fill=disabled_bg)

        # save images
        StylerTTK.theme_images.update(
            {
                f"{element}_cb_off": ImageTk.PhotoImage(cb_off.resize((14, 14)), Image.LANCZOS),
                f"{element}_cb_on": ImageTk.PhotoImage(cb_on.resize((14, 14)), Image.LANCZOS),
                f"{element}_cb_disabled": ImageTk.PhotoImage(cb_disabled.resize((14, 14)), Image.LANCZOS),
            }
        )

    @staticmethod
    def style_outline_menubutton(theme, arrowsize=4, background=None, font=DEFAULT_FONT, foreground=None, style=None):
        """Create a solid menubutton style.

        Args:
            theme (str): The theme name.
            arrowsize (int): The size of the down arrow.
            background (str): The color of the button background.
            font (str): The font used to render the button text.
            foreground (str): The color of the button text.
            style (str): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        pass

    @staticmethod
    def style_menubutton(theme, arrowsize=4, background=None, font=DEFAULT_FONT, foreground=None, style=None):
        """Create a solid menubutton style.

        Args:
            theme (str): The theme name.
            arrowsize (int): The size of the down arrow.
            background (str): The color of the button background.
            font (str): The font used to render the button text.
            foreground (str): The color of the button text.
            style (str): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        disabled_fg = theme.colors.inputfg
        disabled_bg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)
        foreground = ThemeColors.normalize(foreground, theme.colors.selectfg, theme.colors)
        background = ThemeColors.normalize(background, theme.colors.primary, theme.colors)
        pressed = ThemeColors.update_hsv(background, vd=-0.2 if theme.type == "light" else 0.2)
        hover = ThemeColors.update_hsv(background, vd=-0.1 if theme.type == "light" else 0.1)

        # style settings
        settings = dict()
        settings.update(
            {
                f"{style}": {
                    "configure": {
                        "arrowsize": 4,
                        "arrowcolor": foreground,
                        "arrowpadding": (0, 0, 15, 0),
                        "background": background,
                        "bordercolor": background,
                        "darkcolor": background,
                        "foreground": foreground,
                        "lightcolor": background,
                        "font": font,
                        "focusthickness": 0,
                        "focuscolor": "",
                        "padding": (10, 5),
                        "relief": "raised",
                    },
                    "map": {
                        "arrowcolor": [("disabled", disabled_fg)],
                        "foreground": [("disabled", disabled_fg)],
                        "background": [
                            ("disabled", disabled_bg),
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                        "bordercolor": [
                            ("disabled", disabled_bg),
                            ("hover !disabled", hover),
                        ],
                        "darkcolor": [
                            ("disabled", disabled_bg),
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                        "lightcolor": [
                            ("disabled", disabled_bg),
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                    },
                }
            }
        )
        return settings

    @staticmethod
    def style_outline_menubutton(theme, arrowsize=4, background=None, font=DEFAULT_FONT, foreground=None, style=None):
        """Create an outline menubutton style.

        Args:
            theme (str): The theme name.
            arrowsize (int): The size of the down arrow.
            background (str): The color of the button background.
            font (str): The font used to render the button text.
            foreground (str): The color of the button text and outline.
            style (str): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        disabled_fg = ThemeColors.update_hsv(theme.colors.inputbg, vd=-0.2 if theme.type == "light" else -0.3)
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        foreground = ThemeColors.normalize(foreground, theme.colors.primary, theme.colors)
        pressed = ThemeColors.update_hsv(foreground, vd=-0.2 if theme.type == "light" else 0.2)
        hover = ThemeColors.update_hsv(foreground, vd=-0.1 if theme.type == "light" else 0.1)
        selected = theme.colors.selectfg

        # style settings
        settings = dict()
        settings.update(
            {
                f"{style}": {
                    "configure": {
                        "arrowsize": arrowsize,
                        "arrowcolor": foreground,
                        "arrowpadding": (0, 0, 15, 0),
                        "background": background,
                        "bordercolor": foreground,
                        "darkcolor": background,
                        "foreground": foreground,
                        "lightcolor": background,
                        "font": font,
                        "focusthickness": 0,
                        "focuscolor": "",
                        "padding": (10, 5),
                        "relief": "raised",
                    },
                    "map": {
                        "arrowcolor": [("disabled", disabled_fg), ("pressed", selected), ("hover", selected)],
                        "foreground": [("disabled", disabled_fg), ("pressed", selected), ("hover", selected)],
                        "background": [
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                        "bordercolor": [
                            ("hover !disabled", hover),
                        ],
                        "darkcolor": [
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                        "lightcolor": [
                            ("pressed !disabled", pressed),
                            ("hover !disabled", hover),
                        ],
                    },
                }
            }
        )
        return settings

    @staticmethod
    def style_notebook(theme, background=None, foreground=None, style=None):
        """Create a notebook style.

        This doesn't look great with other themes aside from default, but it is possible to use them.

        Args:
            theme (str): The theme name.
            background (str, optional): The color of the notebook background.
            foreground (str, optional): The color of the tab text.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        bordercolor = theme.colors.border if theme.type == "light" else theme.colors.selectbg
        fg_fallback = theme.colors.inputfg if theme.type == "light" else theme.colors.selectfg
        bg_fallback = theme.colors.inputbg if theme.type == "light" else bordercolor
        foreground = ThemeColors.normalize(foreground, fg_fallback, theme.colors)
        background = ThemeColors.normalize(background, bg_fallback, theme.colors)

        # style settings
        settings = dict()
        settings.update(
            {
                style: {
                    "configure": {
                        "bordercolor": bordercolor,
                        "lightcolor": background,
                        "darkcolor": background,
                        "borderwidth": 1,
                    }
                },
                f"{style}.Tab": {
                    "configure": {
                        "bordercolor": bordercolor,
                        "lightcolor": background,
                        "foreground": foreground,
                        "padding": (10, 5),
                    },
                    "map": {
                        "background": [("!selected", background)],
                        "lightcolor": [("!selected", background)],
                        "darkcolor": [("!selected", background)],
                        "bordercolor": [("!selected", bordercolor)],
                        "foreground": [("!selected", foreground)],
                    },
                },
            }
        )
        return settings

    @staticmethod
    def style_panedwindow(theme, sashcolor=None, sashthickness=5, style=None):
        """Create a panedwindows style.

        Args:
            theme (str): The theme name.
            sashcolor (str, optional): The color of the sash.
            sashthickness (int, optional): The thickness of the sash in pixels.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        sashcolor = ThemeColors.normalize(sashcolor, theme.colors.bg, theme.colors)

        # style settings
        settings = dict()
        settings.update(
            {
                style: {"configure": {"background": sashcolor}},
                "Sash": {
                    "configure": {
                        "bordercolor": sashcolor,
                        "lightcolor": sashcolor,
                        "sashthickness": sashthickness,
                        "sashpad": 0,
                        "gripcount": 0,
                    }
                },
            }
        )
        return settings

    @staticmethod
    def style_sizegrip(theme, background=None, foreground=None, style="TSizegrip"):
        """Create an image-based ``Sizegrip`` style.

        Args:
            theme (str): The theme name.
            background (str, optional): The color of the sizegrip background.
            foreground (str, optional): The color of the grip.
            style (str, optional): The style used to render the widget.

        Returns:
            dict: A dictionary of theme settings.
        """
        # fallback colors
        background = ThemeColors.normalize(background, theme.colors.bg, theme.colors)
        fg_fallback = theme.colors.border if theme.type == "light" else theme.colors.inputbg
        foreground = ThemeColors.normalize(foreground, fg_fallback, theme.colors)

        # images
        element_id = uuid4()
        StylerTTK.theme_images.update({element_id: StylerTTK.style_sizegrip_images(foreground)})
        sizegrip_image = StylerTTK.theme_images[element_id]

        # style settings
        settings = dict()
        settings.update(
            {
                f"{style}": {
                    "configure": {"background": background},
                    "layout": [(f"{element_id}.Sizegrip.sizegrip", {"side": "bottom", "sticky": "se"})],
                },
                f"{element_id}.Sizegrip.sizegrip": {"element create": ("image", sizegrip_image)},
            }
        )
        return settings

    def style_sizegrip_images(color):
        """Create assets for sizegrip layout
        Args:
            color (str): The grip color.
        Returns:
            PhotoImage: The tkinter photoimage used for the sizegrip layout.
        """
        im = Image.new("RGBA", (14, 14))
        draw = ImageDraw.Draw(im)

        # top row
        draw.rectangle((9, 3, 10, 4), fill=color)

        # middle row
        draw.rectangle((6, 6, 7, 7), fill=color)  # middle row
        draw.rectangle((9, 6, 10, 7), fill=color)

        # bottom row
        draw.rectangle((3, 9, 4, 10), fill=color)  # bottom row
        draw.rectangle((6, 9, 7, 10), fill=color)
        draw.rectangle((9, 9, 10, 10), fill=color)

        return ImageTk.PhotoImage(im)

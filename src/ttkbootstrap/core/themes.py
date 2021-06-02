import re
from pathlib import Path
import json
import importlib.resources
import colorsys
from PIL import ImageColor

COLOR_PATTERN = re.compile(r"primary|secondary|success|info|warning|danger")
COLORMAP = json.loads(importlib.resources.read_text("ttkbootstrap.core.files", "colormap.json"))


class ThemeColors:
    """A class that contains the theme colors as well as several helper methods for manipulating colors.

    This class is attached to the ``Style`` object at run-time for the selected theme, and so is available to use with
    ``Style.colors``. The colors can be accessed via dot notation or get method:

    .. code-block:: python

        # dot-notation
        Colors.primary

        # get method
        Colors.get('primary')

    This class is an iterator, so you can iterate over the main style color labels (primary, secondary, success, info,
    warning, danger):

    .. code-block:: python

        for color_label in Colors:
            color = Colors.get(color_label)
            print(color_label, color)

    If, for some reason, you need to iterate over all theme color labels, then you can use the ``Colors.label_iter``
    method. This will include all theme colors, including border, fg, bg, etc...

    .. code-block:: python

        for color_label in Colors.label_iter():
            color = Colors.get(color_label)
            print(color_label, color)
    """

    def __init__(
        self,
        primary,
        secondary,
        success,
        info,
        warning,
        danger,
        bg,
        fg,
        selectbg,
        selectfg,
        border,
        inputfg,
        inputbg,
    ):
        """
        Args:
            primary (str): the primary theme color; used by default for all widgets.
            secondary (str): an accent color; commonly of a `grey` hue.
            success (str): an accent color; commonly of a `green` hue.
            info (str): an accent color; commonly of a `blue` hue.
            warning (str): an accent color; commonly of an `orange` hue.
            danger (str): an accent color; commonly of a `red` hue.
            bg (str): background color.
            fg (str): default text color.
            selectfg (str): the color of selected text.
            selectbg (str): the background color of selected text.
            border (str): the color used for widget borders.
            inputfg (str): the text color for input widgets: ie. ``Entry``, ``Combobox``, etc...
            inputbg (str): the text background color for input widgets.
        """
        self.primary = primary
        self.secondary = secondary
        self.success = success
        self.info = info
        self.warning = warning
        self.danger = danger
        self.bg = bg
        self.fg = fg
        self.selectbg = selectbg
        self.selectfg = selectfg
        self.border = border
        self.inputfg = inputfg
        self.inputbg = inputbg

    def get(self, color_label):
        """Lookup a color property

        Args:
            color_label (str): a color label corresponding to a class propery (primary, secondary, success, etc...)

        Returns:
            str: a hexadecimal color value.
        """
        return self.__dict__.get(color_label)

    def set(self, color_label, color_value):
        """Set a color property

        Args:
            color_label (str): the name of the color to be set (key)
            color_value (str): a hexadecimal color value

        Example:

            .. code-block:
                set('primary', '#fafafa')
        """
        self.__dict__[color_label] = color_value

    def __iter__(self):
        return iter(["primary", "secondary", "success", "info", "warning", "danger"])

    def __repr__(self):
        return str((tuple(zip(self.__dict__.keys(), self.__dict__.values()))))

    @staticmethod
    def label_iter():
        """Iterate over all color label properties in the Color class

        Returns:
            iter: an iterator representing the name of the color properties
        """
        return iter(
            [
                "primary",
                "secondary",
                "success",
                "info",
                "warning",
                "danger",
                "bg",
                "fg",
                "selectbg",
                "selectfg",
                "border",
                "inputfg",
                "inputbg",
            ]
        )

    @staticmethod
    def hex_to_rgb(color):
        """Convert hexadecimal color to rgb color value

        Args:
            color (str): param str color: hexadecimal color value

        Returns:
            tuple[int, int, int]: rgb color value.
        """
        if len(color) == 4:
            # 3 digit hexadecimal colors
            r = round(int(color[1], 16) / 255, 2)
            g = round(int(color[2], 16) / 255, 2)
            b = round(int(color[3], 16) / 255, 2)
        else:
            # 6 digit hexadecimal colors
            r = round(int(color[1:3], 16) / 255, 2)
            g = round(int(color[3:5], 16) / 255, 2)
            b = round(int(color[5:], 16) / 255, 2)
        return r, g, b

    @staticmethod
    def rgb_to_hex(r, g, b):
        """Convert rgb to hexadecimal color value

        Args:
            r (int): red
            g (int): green
            b (int): blue

        Returns:
            str: a hexadecimal colorl value
        """
        r_ = max(0, min(int(r * 255), 255))
        g_ = max(0, min(int(g * 255), 255))
        b_ = max(0, min(int(b * 255), 255))
        return "#{:02x}{:02x}{:02x}".format(r_, g_, b_)

    @staticmethod
    def normalize(color, fallback, theme_colors=None):
        """Standard colors by converting named color to hex value.

        Args:
            color (str): The color to normalize.
            fallback (str): The fallback color if the conversion fails.
            theme_colors (dict, optional): The color dictionary for a theme.

        Returns:
            str: a hex color value.
        """
        if not color:
            return fallback

        if '#' in color:
            return color

        bootscolor = re.search(COLOR_PATTERN, color)
        if bootscolor and theme_colors:
            return theme_colors.get(color)
        
        if '#' not in color and color in COLORMAP:
            rgb = ImageColor.getrgb(color)
            return ThemeColors.rgb_to_hex(*rgb)

        return fallback

    @staticmethod
    def update_hsv(color, hd=0, sd=0, vd=0):
        """Modify the hue, saturation, and/or value of a given hex color value.

        Args:
            color (str): the hexadecimal color value that is the target of hsv changes.
            hd (float): % change in hue
            sd (float): % change in saturation
            vd (float): % change in value

        # TODO: There is probably a better way to do this using the ``ImageColor`` module in PIL.

        Returns:
            str: a new hexadecimal color value that results from the hsv arguments passed into the function
        """
        if "#" not in str(color):
            r, g, b = ThemeColors.normalize(color)
        else:
            r, g, b = ThemeColors.hex_to_rgb(color)

        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # hue
        if h * (1 + hd) > 1:
            h = 1
        elif h * (1 + hd) < 0:
            h = 0
        else:
            h *= 1 + hd

        # saturation
        if s * (1 + sd) > 1:
            s = 1
        elif s * (1 + sd) < 0:
            s = 0
        else:
            s *= 1 + sd

        # value
        if v * (1 + vd) > 1:
            v = 0.95
        elif v * (1 + vd) < 0.05:
            v = 0.05
        else:
            v *= 1 + vd

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return ThemeColors.rgb_to_hex(r, g, b)


class ThemeDefinition:
    """A class to provide defined name, colors, and font settings for a ttkbootstrap theme."""

    def __init__(self, name="default", themetype="light", font="helvetica", colors=None):
        """
        Args:
            name (str): the name of the theme; default is 'default'.
            themetype (str): the type of theme: *light* or *dark*; default is 'light'.
            font (str): the default font to use for the application; default is 'helvetica'.
            colors (Colors): an instance of the `Colors` class. One is provided by default.
        """
        self.name = name
        self.type = themetype
        self.font = font
        self.colors = colors if colors else ThemeColors()

    def __repr__(self):
        return f"name={self.name}, type={self.type}, font={self.font}, colors={self.colors}"

    @staticmethod
    def load_themes(themes_file=None):
        """Load all ttkbootstrap defined themes

        Args:
            themes_file (str): the path of the `themes.json` file.

        Returns:
            dict: theme defintions for all ttkbootstrap themes
        """
        # pre-defined themes
        json_data = importlib.resources.read_text("ttkbootstrap.core.files", "themes.json")
        builtin_themes = json.loads(json_data)

        # application-defined or user-defined themes
        if themes_file is None:
            themes_file = builtin_themes["userpath"]
        user_path = Path(themes_file)
        if user_path.exists():
            with user_path.open(encoding="utf-8") as f:
                user_themes = json.load(f)
        else:
            user_themes = {"themes": []}

        # create a theme definition object for each theme, this will be used to generate
        #  the theme in tkinter along with any assets at run-time
        theme_settings = {"themes": builtin_themes["themes"] + user_themes["themes"]}

        # save all theme definitions into a dictionary and return
        theme_definitions = {}
        for theme in theme_settings["themes"]:
            theme_definitions[theme["name"]] = ThemeDefinition(
                name=theme["name"],
                themetype=theme["type"],
                font=theme["font"],
                colors=ThemeColors(**theme["colors"]),
            )
        return theme_definitions


DEFINITIONS = ThemeDefinition.load_themes()
DEFAULT_COLORS = DEFINITIONS["flatly"].colors
DEFAULT_FONT = DEFINITIONS["flatly"].font

"""
    A **ttkbootstrap** styled **Meter** widget.

    Created: 2021-06-10
    Author: Israel Dryer, israel.dryer@gmail.com

"""
import math
from uuid import uuid4
from PIL import Image, ImageDraw
from PIL.ImageTk import PhotoImage
from tkinter import IntVar, StringVar
from ttkbootstrap.style import StylerTTK
from ttkbootstrap.themes import ThemeColors
from ttkbootstrap.widgets import Frame, Label
from ttkbootstrap.constants import *


DEFAULT_TEXT = "helvetica 25 bold"
DEFAULT_LABEL = "helvetica 10 bold"

# TODO the `style_widget` method does not appear to get called here.


class Meter(Frame):
    """A radial meter that can be used to show progress of long running operations or the amount of work completed; can
    also be used as a `Dial` when set to ``interactive=True``.

    !! THIS WIDGET IS EXPERIMENTAL AND MAY CHANGE IN THE FUTURE !!

    This widget is very flexible. There are two primary meter types which can be set with the ``metertype`` parameter:
    'full' and 'semi', which show the arc of the meter in a full or semi-circle. You can also customize the arc of the
    circle with the ``arcrange`` and ``arcoffset`` parameters.

    The progress bar indicator can be displayed as a solid color or with stripes using the ``stripethickness``
    parameter. By default, the ``stripethickness`` is 0, which results in a solid progress bar. A higher
    ``stripethickness`` results in larger wedges around the arc of the meter.

    Various text and label options exist. The center text and progressbar is formatted with the ``meterstyle`` parameter
    and uses the `TMeter` styles. You can prepend or append text to the center text using the ``textappend`` and
    ``textprepend`` parameters. This is most commonly used for '$', '%', or other such symbols.

    The widgets current value can be set and accessed via the ``value`` property. The widget text and be set with the
    ``text`` property. If you set the ``showvalue`` property to `True`, this will override the ``text`` and will
    instead show the widget value in the center of the widget. The ``textappend`` and ``textprepend`` options are still
    available even if the ``text`` option is overridden with the ``showvalue`` option.
    """

    def __init__(
        self,
        master=None,
        bootstyle=DEFAULT,
        amounttotal=100,
        amountused=0,
        arcoffset=None,
        arcrange=None,
        background=None,
        cursor=None,
        foreground=None,
        interactive=False,
        labelfont=None,
        labelcolor=None,
        labeltext=None,
        metersize=200,
        meterthickness=10,
        metertype=FULL,
        padding=None,
        showvalue=True,
        stripethickness=0,
        style=None,
        takefocus=False,
        text=None,
        textappend=None,
        textfont=None,
        textprepend=None,
        textvariable=None,
        variable=None,
        wedgesize=0,
        **kw,
    ):
        """
        Args:
            master: The parent widget.
            bootstyle (str): A string of keywords that controls the widget style; this short-hand API should be preferred over the tkinter ``style`` option, which is still available.
            padding (Any): Sets the internal widget padding: (left, top, right, bottom), (horizontal, vertical), (left, vertical, right), a single number pads all sides.
            takefocus (bool): Determines whether the window accepts the focus during keyboard traversal
            background (str): The frame background color; setting this option will override theme settings.

        .. _`mouse cursor`: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
        """
        # pre-instantiated colors
        self._foreground = foreground
        self._background = background
        self._labelcolor = labelcolor

        Frame.__init__(
            self,
            widgetclass="TMeter",
            master=master,
            bootstyle=bootstyle,
            style=style,
            padding=padding,
            takefocus=takefocus,
            cursor=cursor,
        )
        # fallback colors
        self._foreground = ThemeColors.normalize(foreground or self.themed_color, self.colors.primary, self.colors)
        self._background = ThemeColors.update_hsv(
            ThemeColors.normalize(background, self.colors.selectfg, self.colors), vd=-0.1
        )
        self._labelcolor = ThemeColors.normalize(labelcolor, self.colors.secondary, self.colors)

        self.inner = Frame(self, bootstyle=bootstyle, height=metersize, width=metersize)
        self.inner.pack()

        self._bsoptions = ["background", "foreground", "bootstyle"]
        self._metersize = metersize
        self._bootstyle = bootstyle
        self._amounttotal = amounttotal
        self._interactive = interactive
        self._labelfont = labelfont or DEFAULT_LABEL
        self._labeltext = labeltext
        self._metertype = metertype
        self._meterthickness = meterthickness
        self._padding = padding
        self._showvalue = showvalue
        self._stripethickness = stripethickness
        self._text = text
        self._textappend = textappend
        self._textprepend = textprepend
        self._textfont = textfont or DEFAULT_TEXT
        self._towardsmaximum = True
        self._wedgesize = wedgesize

        # widget variables
        self.variable = variable or IntVar(value=amountused)
        self.textvariable = textvariable or StringVar(value=text) if not showvalue else self.variable
        self.variable.trace_add("write", self._draw_meter)

        if metertype == SEMI:
            self._arcoffset = arcoffset or 135
            self._arcrange = arcrange or 270
        else:  # full
            self._arcoffset = arcoffset or -90
            self._arcrange = arcrange or 360

        # meter image
        self.meter = Label(self.inner)
        self.meter.place(x=0, y=0)
        self._draw_base_image()
        self._draw_meter()

        # set interactive mode
        if self._interactive:
            self.meter.bind("<B1-Motion>", self._on_dial_interact)
            self.meter.bind("<Button-1>", self._on_dial_interact)

        # text and label widgets
        self._textcontainer = Frame(self.inner)
        textprepend = Label(
            self._textcontainer,
            text=self._textprepend,
            bootstyle=SECONDARY,
            foreground=labelcolor,
            font=labelfont,
            padding=(0, 5),
            anchor=S,
        )
        text = Label(
            self._textcontainer,
            textvariable=self.textvariable,
            style=self.style,
            font=self._textfont,
            foreground=self._foreground,
        )
        textappend = Label(
            self._textcontainer,
            text=self._textappend,
            font=self._labelfont,
            foreground=self._labelcolor,
            anchor=S,
            padding=(0, 5),
        )
        supplemental_label = Label(self.inner, text=self._labeltext, bootstyle=SECONDARY, font=self._labelfont)

        # position the text container based on whether or not there is a supplemental label
        if self._labeltext:
            # TODO find a more accurate method for distributing these items inside the widget.
            self._textcontainer.place(relx=0.5, rely=0.43, anchor=CENTER)
        else:
            self._textcontainer.place(relx=0.5, rely=0.5, anchor=CENTER)
        if self._textprepend:
            textprepend.pack(side=LEFT, fill=Y)
        text.pack(side=LEFT, fill=Y)
        if self._textappend:
            textappend.pack(side=LEFT, fill=Y)
        supplemental_label.place(relx=0.5, rely=0.6, anchor=CENTER)

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, value):
        self.variable.set(value)

    def _draw_meter(self, *args):
        """Draw a meter

        Args:
            *args: if triggered by a trace, will be `variable`, `index`, `mode`.
        """
        im = self._base_img.copy()
        draw = ImageDraw.Draw(im)
        if self._stripethickness > 0:
            self._draw_striped_meter(draw)
        else:
            self._draw_solid_meter(draw)
        self._meterimage = PhotoImage(im.resize((self._metersize, self._metersize), Image.CUBIC))
        self.meter.configure(image=self._meterimage)

    def _draw_base_image(self):
        """Draw the base image to be used for subsequent updates"""
        self._base_img = Image.new("RGBA", (self._metersize * 5, self._metersize * 5))
        draw = ImageDraw.Draw(self._base_img)

        # striped meter
        if self._stripethickness > 0:
            for x in range(
                self._arcoffset,
                self._arcrange + self._arcoffset,
                2 if self._stripethickness == 1 else self._stripethickness,
            ):
                draw.arc(
                    (0, 0, self._metersize * 5 - 20, self._metersize * 5 - 20),
                    x,
                    x + self._stripethickness - 1,
                    self._background,
                    self._meterthickness * 5,
                )
        # solid meter
        else:
            draw.arc(
                (0, 0, self._metersize * 5 - 20, self._metersize * 5 - 20),
                self._arcoffset,
                self._arcrange + self._arcoffset,
                self._background,
                self._meterthickness * 5,
            )

    def _draw_solid_meter(self, draw):
        """Draw a solid meter

        Args:
            draw (ImageDraw.Draw): an object used to draw an arc on the meter
        """
        if self._wedgesize > 0:
            meter_value = self._meter_value()
            draw.arc(
                (0, 0, self._metersize * 5 - 20, self._metersize * 5 - 20),
                meter_value - self._wedgesize,
                meter_value + self._wedgesize,
                self._foreground,
                self._meterthickness * 5,
            )
        else:
            draw.arc(
                (0, 0, self._metersize * 5 - 20, self._metersize * 5 - 20),
                self._arcoffset,
                self._meter_value(),
                self._foreground,
                self._meterthickness * 5,
            )

    def _draw_striped_meter(self, draw):
        """Draw a striped meter

        Args:
            draw (ImageDraw.Draw): an object used to draw an arc on the meter
        """
        if self._wedgesize > 0:
            meter_value = self._meter_value()
            draw.arc(
                (0, 0, self._metersize * 5 - 20, self._metersize * 5 - 20),
                meter_value - self._wedgesize,
                meter_value + self._wedgesize,
                self._foreground,
                self._meterthickness * 5,
            )
        else:
            for x in range(self._arcoffset, self._meter_value() - 1, self._stripethickness):
                draw.arc(
                    (0, 0, self._metersize * 5 - 20, self._metersize * 5 - 20),
                    x,
                    x + self._stripethickness - 1,
                    self._foreground,
                    self._meterthickness * 5,
                )

    def _meter_value(self):
        """Calculate the meter value

        Returns:
            int: the value to be used to draw the arc length of the progress meter
        """
        return int((self.value / self._amounttotal) * self._arcrange + self._arcoffset)

    def _on_dial_interact(self, e):
        """Callback for mouse drag motion on indicator

        Args:
            e (Event): event callback for drag motion.
        """
        dx = e.x - self._metersize // 2
        dy = e.y - self._metersize // 2
        rads = math.atan2(dy, dx)
        degs = math.degrees(rads)

        if degs > self._arcoffset:
            factor = degs - self._arcoffset
        else:
            factor = 360 + degs - self._arcoffset

        # clamp value between 0 and ``amounttotal``
        amountused = int(self._amounttotal / self._arcrange * factor)
        if amountused < 0:
            self.value = 0
        elif amountused > self._amounttotal:
            self.value = self._amounttotal
        else:
            self.value = amountused

    def style_widget(self):

        # custom styles
        if any([self._background != None, self._foreground != None, self._labelcolor != None]):
            self.customized = True
            if not self._widget_id:
                self._widget_id = uuid4() if self._widget_id == None else self._widget_id
                self.style = f"{self._widget_id}.{self.style}"

            options = {
                "theme": self.theme,
                "background": self._background,
                "foreground": self._foreground or self.themed_color,
                "style": self.style,
            }
            StylerTTK.style_meter(**options)

        # ttkbootstrap styles
        else:
            options = {
                "theme": self.theme,
                "settings": self.settings,
                "foreground": self.themed_color,
                "style": self.style,
            }
            StylerTTK.style_meter(**options)

    def step(self, delta=1):
        """Increase the indicator value by ``delta``.
        The default increment is 1. The indicator will reverse direction and count down once it reaches the maximum
        value.
        Keyword Args:
            delta (int): the amount to change the indicator.
        """
        if self.value >= self._amounttotal:
            self._towardsmaximum = True
            self.value = self._amountused - delta
        elif self.value <= 0:
            self.towardsmaximum = False
            self.value = self.value + delta
        elif self.towardsmaximum:
            self.value = self.value - delta
        else:
            self.value = self.value + delta

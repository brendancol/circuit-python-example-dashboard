import board
import busio
import time
import digitalio
import displayio
import terminalio

from adafruit_display_text import label
from adafruit_stmpe610 import Adafruit_STMPE610_SPI

WIDTH = 480
HEIGHT = 320

HEADER_HEIGHT = 24
FOOTER_HEIGHT = 72
BODY_HEIGHT = HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT

spi = board.SPI()

tft_cs = board.D9
tft_dc = board.D10

def connect_to_display():

    import adafruit_hx8357
    displayio.release_displays()
    display_bus = displayio.FourWire(spi, command=tft_dc,
                                     chip_select=tft_cs)

    return adafruit_hx8357.HX8357(display_bus, width=WIDTH, height=HEIGHT)


class App(object):

    def __init__(self):

        self.display = connect_to_display()

        self.splash = displayio.Group(max_size=10)

        self.title = label.Label(terminalio.FONT,
                                 text='Example Dashboard',
                                 color=0x333333)

        self.clock = label.Label(terminalio.FONT,
                                 text='00:00:00',
                                 color=0x333333)

    def show(self):
        self.display.show(self.splash)

    def render_background(self):
        color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x333333

        bg_sprite = displayio.TileGrid(color_bitmap,
                                       pixel_shader=color_palette,
                                       x=0, y=0)

        self.splash.append(bg_sprite)

    def render_header(self):
        PADDING = 0

        # background
        inner_bitmap = displayio.Bitmap(WIDTH - (PADDING * 2),
                                        HEADER_HEIGHT, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0xC7C7C7
        inner_sprite = displayio.TileGrid(inner_bitmap,
                                          pixel_shader=inner_palette,
                                          x=0, y=0)
        self.splash.append(inner_sprite)

        # clock
        clock_group = displayio.Group(max_size=10,
                                      scale=2,
                                      x=WIDTH - 100,
                                      y=10)
        clock_group.append(self.clock)  # Subgroup for text scaling
        self.splash.append(clock_group)

        # title
        title_group = displayio.Group(max_size=10,
                                     scale=2,
                                     x=10,
                                     y=10)
        title_group.append(self.title)  # Subgroup for text scaling
        self.splash.append(title_group)

    def render_body(self):
        with open("/sample.bmp", "rb") as f:
            odb = displayio.OnDiskBitmap(f)
            face = displayio.TileGrid(odb,
                                      pixel_shader=displayio.ColorConverter(),
                                      tile_height=195 // 5,
                                      tile_width=774 // 6,
                                      default_tile=9,
                                      x=40,
                                      y=40,
                                      width=1,
                                      height=1)
            self.splash.append(face)
            self.display.wait_for_frame()
        pass

    def render_footer(self):
        PADDING = 0

        # background
        inner_bitmap = displayio.Bitmap(WIDTH - (PADDING * 2),
                                        FOOTER_HEIGHT, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0xC7C7C7
        inner_sprite = displayio.TileGrid(inner_bitmap,
                                          pixel_shader=inner_palette,
                                          x=0, y=HEIGHT - FOOTER_HEIGHT)
        self.splash.append(inner_sprite)

    def render(self):

        self.show()
        self.render_background()
        self.render_header()
        self.render_body()
        self.render_footer()

    def update_clock(self):
        t = time.localtime()
        app.clock.text = "{}:{}:{}".format(t.tm_hour,
                                           t.tm_min,
                                           t.tm_sec)

app = App()
app.render()

while True:
    time.sleep(1)
    app.update_clock()

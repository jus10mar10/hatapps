from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import sys
import time
from gpiozero import Button

from spotify.spotify import now_playing, skip_song, toggle_playback

# Constants
ROTATION_DEFAULT = 0
BRIGHTNESS = 0.1
STARTUP_MESSAGE = 'STARTING UP...'
FONT_PATH = "assets/5x7.ttf"
BUTTON_MAP = {
    5: "A",  # Button A
    6: "B",     # Button B (remapped)
    16: "X",      # Button X
    24: "Y",    # Button Y
}

# Initialize Unicorn HAT Mini
unicornhatmini = UnicornHATMini()
unicornhatmini.set_rotation(ROTATION_DEFAULT)
display_width, display_height = unicornhatmini.get_shape()
unicornhatmini.set_brightness(BRIGHTNESS)


def render_text(text):
    font = ImageFont.truetype(FONT_PATH, 8)
    text_width, text_height = font.getsize(text)
    image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
    draw = ImageDraw.Draw(image)
    draw.text((display_width, -1), text, font=font, fill=255)
    show_text(text_width, image)

def show_text(text_width, image):
    offset_x = 0
    for _ in range(text_width + 17):
        for y in range(display_height):
            for x in range(display_width):
                hue = (time.time() / 10.0) + (x / float(display_width * 2))
                r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
                pixel_color = (r, g, b) if image.getpixel((x + offset_x, y)) == 255 else (0, 0, 0)
                unicornhatmini.set_pixel(x, y, *pixel_color)
        offset_x += 1
        if offset_x + display_width > image.size[0]:
            offset_x = 0
        unicornhatmini.show()
        time.sleep(0.04)
from unicornhatmini import UnicornHATMini
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import sys
import time
from gpiozero import Button

from spotify.spotify import now_playing

# Constants
ROTATION_DEFAULT = 0
BRIGHTNESS = 0.1
STARTUP_MESSAGE = 'STARTING UP...'
FONT_PATH = "assets/5x7.ttf"
BUTTON_MAP = {
    5: "A",
    6: "B",
    16: "X",
    24: "Y"
}

# Global variables
app_running = False

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

def app():
    global app_running
    while app_running:
        render_text(now_playing())
        time.sleep(3)  # Add a small delay to avoid consuming too much CPU

def pressed(button):
    global app_running
    button_name = BUTTON_MAP.get(button.pin.number)
    if button_name == 'A':  # Toggle the app_running flag
        app_running = not app_running
    elif button_name == 'B':  # Quit button
        app_running = False

def setup_buttons():
    button_a = Button(5)
    button_b = Button(6)
    button_a.when_pressed = pressed
    button_b.when_pressed = pressed

def main():
    render_text(STARTUP_MESSAGE)
    setup_buttons()
    try:
        while True:
            if app_running:
                app()
            time.sleep(0.1)
    except KeyboardInterrupt:
        unicornhatmini.clear()
        unicornhatmini.show()
        unicornhatmini.cleanup()

if __name__ == "__main__":
    main()

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

# app selection screen
def home():
    # button functions
    def pressed(button):
        button_name = BUTTON_MAP[button.pin.number]
        if button_name == "A":
            pass
        elif button_name == "B":
            global selected_app
            APPS[selected_app]()
        elif button_name == "X":
            global selected_app
            selected_app = (selected_app - 1) % len(APPS)
            render_text(APP_NAMES[selected_app])
        elif button_name == "Y":
            global selected_app
            selected_app = (selected_app + 1) % len(APPS)
            render_text(APP_NAMES[selected_app])
    def setup_buttons():
        button_a = Button(5)
        button_b = Button(6)
        button_x = Button(16)
        button_y = Button(24)
        button_a.when_pressed = pressed
        button_b.when_pressed = pressed
        button_y.when_pressed = pressed
        button_x.when_pressed = pressed
    setup_buttons()
    # main loop
    while True:
        render_text(APP_NAMES[selected_app])
        time.sleep(3)    

def spotify():
    def pressed(button):
        button_name = BUTTON_MAP.get(button.pin.number)
        if button_name == 'A':  
            pass
        elif button_name == 'B':  # Quit button
            home()
        elif button_name == 'X':
            skip_song()
        elif button_name == 'Y':
            toggle_playback()
    def setup_buttons():
        button_a = Button(5)
        button_b = Button(6)
        button_x = Button(16)
        button_y = Button(24)
        button_a.when_pressed = pressed
        button_b.when_pressed = pressed
        button_x.when_pressed = pressed
        button_y.when_pressed = pressed
    setup_buttons()
    while True:
        render_text(now_playing())
        time.sleep(3)  # Add a small delay to avoid consuming too much CPU

# App Selection Constants
APP_NAMES = ["Home", "Spotify"]
APPS = [home, spotify]
selected_app = 0

def main():
    global selected_app
    render_text(STARTUP_MESSAGE)
    home()

if __name__ == "__main__":
    main()
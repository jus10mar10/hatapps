from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import sys
import time
from gpiozero import Button

from unicornhatmini import UnicornHATMini

from spotify.spotify import now_playing, skip_song, toggle_playback

# Constants
ROTATION_DEFAULT = 0
STARTUP_MESSAGE = 'STARTING UP...'
FONT_PATH = "assets/5x7.ttf"
BUTTON_MAP = {
    5: "A",  # Button A
    6: "B",     # Button B (remapped)
    16: "X",      # Button X
    24: "Y",    # Button Y
}

# configurable settings
brightness = 0.1

# Initialize Unicorn HAT Mini
unicornhatmini = UnicornHATMini()
unicornhatmini.set_rotation(ROTATION_DEFAULT)
display_width, display_height = unicornhatmini.get_shape()
unicornhatmini.set_brightness(brightness)

# App functionality
app_names = ['Home', 'Spotify']
current_app = 0
selected_app = 0
app_running = False

def static_text(image):
    for y in range(display_height):
        for x in range(display_width):
            hue = (time.time() / 10.0) + (x / float(display_width * 2))
            r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
            pixel_color = (r, g, b) if image.getpixel((x, y)) == 255 else (0, 0, 0)
            unicornhatmini.set_pixel(x, y, *pixel_color)
    unicornhatmini.show()
    time.sleep(0.04)

def scrolling_text(text_width, image):
    offset_x = 0
    for _ in range(text_width + 17):
        for y in range(display_height):
            for x in range(display_width):
                hue = (time.time() / 10.0) + (x / float(display_width * 2))
                r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
                pixel_color = (r, g, b) if image.getpixel((x + offset_x, y)) == 255 else (0, 0, 0)
                unicornhatmini.set_pixel(x, y, *pixel_color)
        offset_x += 1
        unicornhatmini.show()
        time.sleep(0.04)

def render_text(text):
    font = ImageFont.truetype(FONT_PATH, 8)
    text_width, text_height = font.getsize(text)
    image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
    draw = ImageDraw.Draw(image)
    draw.text((display_width, -1), text, font=font, fill=255)
    if image.size[0] > display_width:
        scrolling_text(text_width, image)
    else:
        static_text(image)

# Apps
def home():
    render_text('Home')

def spotify():
    global app_running
    while app_running == True:
        try:
            render_text(now_playing())
        except:
            render_text('ERROR OUCH...')
        time.sleep(2.5)

# HOME Button Actions
def app_up():
    global selected_app
    selected_app = (selected_app - 1) % len(app_names)
    render_text(app_names[selected_app])

def app_down():
    global selected_app
    selected_app = (selected_app + 1) % len(app_names)
    render_text(app_names[selected_app])

# App Navigation
def app_select(selected_app=selected_app):
    global current_app
    global app_running
    if selected_app == 0:
        current_app = 0
        home()
    elif selected_app == 1:
        current_app = 1
        spotify()

def pressed(button):
    """ Handles button presses. Changes button action based on context.
    Context is determinded by the current value of selected app."""

    button_name = BUTTON_MAP.get(button.pin.number)
    # HOME
    global current_app
    global selected_app
    if current_app == 0:
        if button_name == 'A':
            global brightness
            brightness += (0.1 % 1) + 0.1
            unicornhatmini.set_brightness(brightness)
        elif button_name == 'B':
            app_select(selected_app=selected_app)
        elif button_name == 'X':
            app_up()
            render_text(app_names[selected_app])
        elif button_name == 'Y':
            app_down()
            render_text(app_names[selected_app])
    # SPOTIFY
    if current_app == 1:
        if button_name == 'B':
            global app_running
            app_running = not app_running
            selected_app = 0
            app_select()
        if button_name == 'X':
            skip_song()
        if button_name == 'Y':
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
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont

def render(text, display_width, display_height):
    # Load a nice 5x7 pixel font
    # Granted it's actually 5x8 for some reason :| but that doesn't matter
    font = ImageFont.truetype("5x7.ttf", 8)

    # Measure the size of our text, we only really care about the width for the moment
    # but we could do line-by-line scroll if we used the height
    text_width, text_height = font.getsize(text)

    # Create a new PIL image big enough to fit the text
    image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
    draw = ImageDraw.Draw(image)

    # Draw the text into the image
    draw.text((display_width, -1), text, font=font, fill=255)
    return text_width, image

def show_text(text_width, image, unicornhatmini):
    offset_x = 0
    for loop in range(text_width + 17):
        for y in range(display_height):
            for x in range(display_width):
                hue = (time.time() / 10.0) + (x / float(display_width * 2))
                r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
                if image.getpixel((x + offset_x, y)) == 255:
                    unicornhatmini.set_pixel(x, y, r, g, b)
                else:
                    unicornhatmini.set_pixel(x, y, 0, 0, 0)

        offset_x += 1
        if offset_x + display_width > image.size[0]:
            offset_x = 0

        unicornhatmini.show()
        time.sleep(0.04)
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
2025 IEEE Rising Stars Conference
Badge Design
TFT Display code

Green LEDs on GP2
Buttons on GP3,4,5,6,7,8 (ACTIVE LOW)
RGB on 20,21,22

Tool for MP4 to GIF: ezgif.com

Memory Leak Fixed by Chad
"""

import time
import board
import busio
import displayio
import fourwire
import terminalio
#import adafruit_il0373
import digitalio
# import pwmio
import adafruit_rgbled
from rainbowio import colorwheel

from adafruit_display_text import label
import adafruit_ili9341

import gc
import os
import struct
import gifio

first_name = "PROGRAM"
last_name = "ME!"
title = "Organizer"
organization = "IEEE Rising Stars Conf."

# --------------- END OF CONFIG --------------
#print("init")

# digital io
green_leds = digitalio.DigitalInOut(board.GP2)
green_leds.direction = digitalio.Direction.OUTPUT

button_s1 = digitalio.DigitalInOut(board.GP3)
button_s2 = digitalio.DigitalInOut(board.GP4)
button_s3 = digitalio.DigitalInOut(board.GP5)
button_s4 = digitalio.DigitalInOut(board.GP6)
button_s5 = digitalio.DigitalInOut(board.GP7)
button_s6 = digitalio.DigitalInOut(board.GP8)
# button_up.value

RED_LED = board.GP20
GREEN_LED = board.GP21
BLUE_LED = board.GP22

rgb_led = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED, invert_pwm=True)
# rgb_led.color = (255, 0, 0)

# Used to ensure the display is free in CircuitPython
displayio.release_displays()

#*** TFT Display ***
# TFT display configuration
spi0 = busio.SPI(clock=board.GP18, MOSI=board.GP19)

tft_cs = board.GP9
tft_dc = board.GP17
tft_rst = board.GP16

# TFT display size
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240

# TFT display init
display_bus = fourwire.FourWire(spi0, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = adafruit_ili9341.ILI9341(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, rotation=180                   )

time.sleep(1)  # Wait a bit

# Create a display group for our screen objects
g = displayio.Group()
mtt = displayio.Group()


font = terminalio.FONT
color = 0xFFFFFF
color_black = 0x000000

# Font assistance parameters
FONT_X_SIZE = 6                 # number of x-pixels per character, 5 + 1
FONT_Y_SIZE = 8                 # number of y-pixels per character, 7 + 1

# Get a dictionary of GIF filenames at the passed base directory
def get_files(base):
    allfiles = os.listdir(base)
    file_names = []
    for _, filetext in enumerate(allfiles):
        if not filetext.startswith("."):
            if filetext not in ('boot_out.txt', 'System Volume Information'):
                if filetext.endswith(".gif"):
                    file_names.append(filetext)
    return file_names

screen_state = 1
screen_default = 1
screen_badge = 1
screen_trailer = 2

# print("setup done")

# ------------------ END OF SETUP --------------------

blink_speed = 0.5
green_leds_status = 0
initial_time = time.monotonic()
def green_leds_blink():
    global blink_speed, green_leds_status, initial_time
    current_time = time.monotonic()
    if current_time - initial_time > blink_speed:
        initial_time = current_time
        green_leds_status = not green_leds_status
        green_leds.value = green_leds_status
    #print(current_time," ",initial_time," ",green_leds_status)


def custom_wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos*3), int(pos*3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos*3), int(pos*3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos*3))

def custom_wheel2(pos,max_brightness=255):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    # Added max_brightness
    const_transition1 = (max_brightness/3)
    const_transition2 = (2*max_brightness/3)
    if pos < 0 or pos > max_brightness:
        return 0, 0, 0
    if pos < const_transition1:
        return int(max_brightness - pos*3), int(pos*3), 0
    if pos < const_transition2:
        pos -= const_transition1
        return 0, int(max_brightness - pos*3), int(pos*3)
    pos -= const_transition2
    return int(pos * 3), 0, int(max_brightness - (pos*3))


wheel_delay = 1
wheel_delay_count = 0
wheel = 0
colorwheel_enable = 1
def buttons_scan():
    global wheel_delay, wheel_delay_count, wheel, colorwheel_enable
    global screen_state
    brightness = 16
    irq_button = 0
    nSw = [1,button_s1.value,button_s2.value, button_s3.value, button_s4.value, button_s5.value, button_s6.value]
    # print(nSw[1],nSw[2],nSw[3],nSw[4],nSw[5],nSw[6])
    sw = [not value for value in nSw]
    for stat in sw:
        if stat == 1:
            irq_button = 1
            break


    if wheel_delay_count >= wheel_delay:
        wheel = (wheel + 1) % (brightness+1)
        # if wheel > 256: wheel = 0
        wheel_delay_count = 0


    if sw[1]: colorwheel_enable = 1
    if sw[2]: colorwheel_enable = 0
    if sw[5]:
        wheel_delay_count = wheel_delay_count
        if screen_state == screen_badge:
            screen_state = screen_trailer
        elif screen_state == screen_trailer:
            screen_state = screen_badge
        else:
            screen_state = screen_default
        time.sleep(0.05) # debouncer
    else: wheel_delay_count = wheel_delay_count + 1

    if sw[3] or sw[6] or sw[4]:
        # manual LED colors: r,g,b
        rgb_led.color = (brightness*sw[3],brightness*sw[6],brightness*sw[4])
    elif colorwheel_enable:
        #rgb_led.color = colorwheel(wheel) # note, kinda bright
        rgb_led.color = custom_wheel2(wheel,brightness) # custom
    elif not colorwheel_enable:
        rgb_led.color = (0,0,0)

badge_loaded = 0

def generate_name_screen(fname, lname, text_title, text_organization, logo_file="Full Logo 2025 Shine 320x100.bmp"):
    screenvar = displayio.Group()
    f = open(logo_file, "rb")
    pic = displayio.OnDiskBitmap(f)
    # Create a Tilegrid with the bitmap and put in the displayio group
    # CircuitPython 6 & 7 compatible
    t = displayio.TileGrid(pic, pixel_shader=getattr(pic, "pixel_shader", displayio.ColorConverter()))

    # CircuitPython 7 compatible only
    # t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    screenvar.append(t)

    # add text - name
    # above bitmap is 320x100 on a 320x240 display
    text_name = fname + " " + lname
    # self-centering and scalar selection
    text_name_scale = 3
    text_name_size = len(text_name)
    text_name_xpixels = text_name_scale * text_name_size * FONT_X_SIZE    # total pixel width of the string
    if text_name_xpixels < DISPLAY_WIDTH:
        x_off_center_calc = int((DISPLAY_WIDTH/2) - (text_name_xpixels/2))
        text_group_name = displayio.Group(scale=text_name_scale, x=x_off_center_calc, y=130)
        text_area_name = label.Label(font, text=text_name, color=color)
        text_group_name.append(text_area_name) # subgroup for text scaling
        screenvar.append(text_group_name)
    else:
        # Maybe make into 2 lines, large first name and smaller last name
        # First name
        text_name = first_name
        text_name_scale = 3
        text_name_size = len(text_name)
        text_name_xpixels = text_name_scale * text_name_size * FONT_X_SIZE    # total pixel width of the string
        x_off_center_calc = (DISPLAY_WIDTH/2) - (text_name_xpixels/2)
        text_group_name = displayio.Group(scale=text_name_scale, x=x_off_center_calc, y=130)
        text_area_name = label.Label(font, text=text_name, color=color)
        text_group_name.append(text_area_name) # subgroup for text scaling
        screenvar.append(text_group_name)

        # Last name
        y_off_calc = text_name_scale * FONT_Y_SIZE
        text_name = last_name
        text_name_scale = 2
        text_name_size = len(text_name)
        text_name_xpixels = text_name_scale * text_name_size * FONT_X_SIZE    # total pixel width of the string
        x_off_center_calc = (DISPLAY_WIDTH/2) - (text_name_xpixels/2)
        text_group_name = displayio.Group(scale=text_name_scale, x=x_off_center_calc, y=(130 + y_off_calc))
        text_area_name = label.Label(font, text=text_name, color=color)
        text_group_name.append(text_area_name) # subgroup for text scaling
        screenvar.append(text_group_name)


    # add text - title
    if len(text_title) > 0:
        text_title_scale = 2 if len(text_organization) > 0 else 3
        text_title_size = len(text_title)
        text_title_xpixels = text_title_scale * text_title_size * FONT_X_SIZE    # total pixel width of the string
        x_off_center_calc = int((DISPLAY_WIDTH/2) - (text_title_xpixels/2))
        text_group_title = displayio.Group(scale=text_title_scale, x=x_off_center_calc, y=185)
        text_area_title = label.Label(font, text=text_title, color=color)
        text_group_title.append(text_area_title) # subgroup for text scaling
        screenvar.append(text_group_title)

    # add text - organization
    if len(text_organization) > 0:
        text_organization_scale = 2 if len(text_title) > 0 else 3
        text_organization_size = len(text_organization)
        text_organization_xpixels = text_organization_scale * text_organization_size * FONT_X_SIZE    # total pixel width of the string
        x_off_center_calc = int((DISPLAY_WIDTH/2) - (text_organization_xpixels/2))
        text_group_organization = displayio.Group(scale=text_organization_scale, x=x_off_center_calc, y=215)
        text_area_organization = label.Label(font, text=text_organization, color=color)
        text_group_organization.append(text_area_organization) # subgroup for text scaling
        screenvar.append(text_group_organization)
    return screenvar


#while True:
def badge_func(screen1, screen2):
    global badge_loaded
    if badge_loaded == 2:
        display.root_group = screen1
        badge_loaded = 0
    else:
        display.root_group = screen2
        badge_loaded = 2

    # Refresh the display to have it actually show the image
    # NOTE: Do not refresh eInk displays sooner than 180 seconds
    display.refresh()
    #print("refreshed")

            # memory clean up
    gc.collect()
    print('Free memory at code point 1: {} bytes'.format(gc.mem_free()) )
    print(badge_loaded)

COL_OFFSET = 0
ROW_OFFSET = 30
def gif_func():
    bg = displayio.Group()
    # Set black background to clear screen
    bg_gif = displayio.Bitmap(320,240,1)
    bg_black = displayio.Palette(1)
    bg_black[0] = color_black
    bg_sprite = displayio.TileGrid(bg_gif,pixel_shader=bg_black,x=0,y=0)
    bg.append(bg_sprite)
    # Place the display group on the screen
    display.root_group = bg
    display.refresh()

    files = get_files("/")
    for i in range(len(files)):
        odg = gifio.OnDiskGif(files[i])
        # Skip Feather GIFs if put on PyPortal
        if odg.width != DISPLAY_WIDTH:
            # print("File "+files[i]+" not right width, skipping\n")
            continue

        start = time.monotonic()
        next_delay = odg.next_frame()  # Load the first frame
        end = time.monotonic()
        call_delay = end - start

        # Display GIF file frames
        # note that this is the direct writing approach
        # initial GIF is rotated due to hw, so just rotated GIF instead
        while screen_state == screen_trailer:
            sleeptime = max(0, next_delay - call_delay)
            time.sleep(sleeptime)
            next_delay = odg.next_frame()
            display_bus.send(42, struct.pack(">hh", COL_OFFSET, odg.bitmap.width - 1 + COL_OFFSET))
            display_bus.send(43, struct.pack(">hh", ROW_OFFSET, odg.bitmap.height - 1 + ROW_OFFSET))
            display_bus.send(44, odg.bitmap)
            green_leds_blink()
            buttons_scan()
            if screen_state != screen_trailer:
                break
        # End while
        # Clean up memory
        odg.deinit()
        odg = None
        gc.collect()
        print('Free memory at code point 1: {} bytes'.format(gc.mem_free()) )
        time.sleep(0.05)
        break

#print("done")
prev_state = 0
screenflipcnt = 1
badge_screen = generate_name_screen(first_name, last_name, title, organization)
ad_screen = generate_name_screen("Come See", "MTT-S", "", "Egyptian Ballroom")
screen_flip_count = 20
badge_loaded = 2
while True:
    # pass
    green_leds_blink()
    buttons_scan()
    time.sleep(0.05)
    screenflipcnt += 1
    if screenflipcnt % screen_flip_count == 0:
        if prev_state == screen_badge:
            prev_state = screen_trailer
    if prev_state != screen_state:
        prev_state = screen_state
        if screen_state == screen_badge:
            badge_func(badge_screen, ad_screen)
        elif screen_state == screen_trailer:
            gif_func()
        else:
            badge_func(badge_screen, ad_screen)

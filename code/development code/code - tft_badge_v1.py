# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
2025 IEEE Rising Stars Conference
Badge Design
TFT Display code
"""

import time
import board
import busio
import displayio
import fourwire
import terminalio
#import adafruit_il0373
#import digitalio

from adafruit_display_text import label
import adafruit_ili9341

first_name = "Alberto"
last_name = "Tam Yong"
title = "Badge Design Engineer"
organization = "IEEE Rising Stars Conf."

print("init")

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

font = terminalio.FONT
color = 0xFFFFFF

print("setup done")

while True:
    print("TFT load image")
    # Display a ruler graphic from the root directory of the CIRCUITPY drive
    with open("Full Logo 2025 Shine 320x100.bmp", "rb") as f:
        pic = displayio.OnDiskBitmap(f)
        # Create a Tilegrid with the bitmap and put in the displayio group
        # CircuitPython 6 & 7 compatible
        t = displayio.TileGrid(
            pic, pixel_shader=getattr(pic, "pixel_shader", displayio.ColorConverter())
        )
        # CircuitPython 7 compatible only
        # t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
        g.append(t)

        # add text - name
        # above bitmap is 320x100 on a 320x240 display
        text_group_name = displayio.Group(scale=3, x=20, y=130)
        text_name = first_name + " " + last_name
        text_area_name = label.Label(font, text=text_name, color=color)
        #text_area_name.anchor_point = ( 0.5, 0.0) # anchor to top-middle of text
        #text_area_name.anchored_position = (DISPLAY_WIDTH/2, 0)
        text_group_name.append(text_area_name) # subgroup for text scaling
        g.append(text_group_name)

        # add text - title
        text_group_title = displayio.Group(scale=2, x=40, y=185)
        text_title = title
        text_area_title = label.Label(font, text=text_title, color=color)
        text_group_title.append(text_area_title) # subgroup for text scaling
        g.append(text_group_title)

        # add text - organization
        text_group_organization = displayio.Group(scale=2, x=30, y=215)
        text_organization = organization
        text_area_organization = label.Label(font, text=text_organization, color=color)
        text_group_organization.append(text_area_organization) # subgroup for text scaling
        g.append(text_group_organization)

        # Place the display group on the screen
        display.root_group = g

        # Refresh the display to have it actually show the image
        # NOTE: Do not refresh eInk displays sooner than 180 seconds
        display.refresh()
        print("refreshed")

        break
        #time.sleep(10)

print("done")
while True:
    pass

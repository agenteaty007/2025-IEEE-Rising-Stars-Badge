# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test script for Adafruit 2.13" 212x104 tri-color display
Supported products:
  * Adafruit 2.13" Tri-Color Display Breakout
  * https://www.adafruit.com/product/4086 (breakout) or
  * https://www.adafruit.com/product/4128 (FeatherWing)
"""

import time
import board
import busio
import displayio
import fourwire
#import adafruit_il0373
#import digitalio

from adafruit_display_text import label
import adafruit_ili9341

print("init")

# Used to ensure the display is free in CircuitPython
displayio.release_displays()

#*** TFT Display ***
# TFT display configuration
spi0 = busio.SPI(clock=board.GP18, MOSI=board.GP19)

#tft_cs = digitalio.DigitalInOut(board.GP9)
#tft_dc = digitalio.DigitalInOut(board.GP17)
#tft_rst = digitalio.DigitalInOut(board.GP16)
tft_cs = board.GP9
tft_dc = board.GP17
tft_rst = board.GP16

# TFT display init
display_bus = fourwire.FourWire(spi0, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

time.sleep(1)  # Wait a bit

# Create a display group for our screen objects
g = displayio.Group()

print("setup done")

mode_select = "4"

while True:
    # mode_select = input("user input selection: ")

    if mode_select == "0":
        print("Hello world")
    elif mode_select == "1":
        print(mode_select)
        print("Eink load image")
        # Display a ruler graphic from the root directory of the CIRCUITPY drive
        with open("/display-ruler.bmp", "rb") as f:
            pic = displayio.OnDiskBitmap(f)
            # Create a Tilegrid with the bitmap and put in the displayio group
            # CircuitPython 6 & 7 compatible
            t = displayio.TileGrid(
                pic, pixel_shader=getattr(pic, "pixel_shader", displayio.ColorConverter())
            )
            # CircuitPython 7 compatible only
            # t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
            g.append(t)

            # Place the display group on the screen
            display.root_group = g

            # Refresh the display to have it actually show the image
            # NOTE: Do not refresh eInk displays sooner than 180 seconds
            display.refresh()
            print("refreshed")

            time.sleep(3)
    elif mode_select == "3":
        print(mode_select)
        print("TFT blue")
        #display.fill(0)
        splash = displayio.Group()
        display.root_group = splash
        color_bitmap = displayio.Bitmap(320,240,1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x0000FF # red
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)
        time.sleep(3)
        mode_select = "4"
    elif mode_select == "4":
        print(mode_select)
        print("TFT red")
        # red
        #display.fill(color565(255, 0, 0))
        splash = displayio.Group()
        display.root_group = splash
        color_bitmap = displayio.Bitmap(320,240,1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFF0000 # red
        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)
        time.sleep(3)
        mode_select = "3"
    else:
        print("Not found. Renter value.")


#while True:
#    pass

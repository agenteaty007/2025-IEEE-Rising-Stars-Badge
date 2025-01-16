2025 IEEE Rising Stars Conference
Badge

Note: This is an early-prototype of the code and setup. All based on drafts and development.

In short, hold BOOTSEL, plug board to computer, let go, drag appropriate "uf2" file in, wait for reboot, copy-paste code in.

Detailed Code Programming Instructions:
1. Start with usb cable disconnected.
2. Hold down BOOTSEL on the Pico board.
3. While holding down the button, connect USB to computer.
4. Wait and hold until "RPI-RP2" drive appears. (it'll be just like a flashdrive)
5. Now you can let go of the button.
6. Identify which Raspberry Pi Pico you have on your board. i.e. Pico, PicoW, Pico2, Pico2W
7. Identify the correct UF2 file that matches your board. I placed a folder named "uf2" in the .zip.
8. Drag the file into the RPI-RP2 drive. Like copy-pasting.
9. The drive will disappear and reappear as "CIRCUITPY".
10. Now the board is ready for CircuitPYthon. The main code executes from "code.py".
11. For the badge code, I recommend deleting all the files in "CIRCUITPY".
12. Go to the folder with the custom badge code.
13. Copy all files and folders inside that folder.
14. Paste all files and folders in "CIRCUITPY" drive.
15. Once pasted, the code will automatically start executing.

For reference, learn more about CircuitPython at:
https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython

CircuitPython executes directly form the "code.py" file. You can edit the code with any text editor, such as notepad.
Near the top of the code, I set up variables for "first_name", "last_name", "title", "organization".
Edit those variables to customize your badge. Save file. Code will automatically reboot.

Feel free to further explore, edit, and tinker.

More details will be available soon.
https://ieee-risingstars.org/2025/badge/
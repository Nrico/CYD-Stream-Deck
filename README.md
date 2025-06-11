# CircuitPython Stream Deck Clone

A simple, low-cost touch-controlled Stream Deck–style macro pad built with CircuitPython, a yellow display, and a resistive touchscreen. Each on-screen button sends a USB HID keyboard shortcut to your computer.

## Features

* USB HID keyboard emulation via CircuitPython
* Configurable grid of touch buttons
* Customizable key combinations for each button
* Visual feedback on button press
* Simple one-file `code.py` design

## Hardware Requirements

* **Microcontroller** running CircuitPython with built-in display support (e.g., PyPortal, QT Py with OLED)
* **Yellow TFT/OLED display** or any compatible display
* **Resistive touchscreen** (e.g., Adafruit 2.8" Resistive Touchscreen)
* **PCA9685 PWM board** *(optional, if you plan to add LEDs or other outputs)*
* USB cable for connecting to your computer

## Software Requirements

* [CircuitPython](https://circuitpython.org/) 8.0.0 or later
* Adafruit CircuitPython libraries:

  * `adafruit_display_shapes`
  * `adafruit_display_text`
  * `adafruit_touchscreen`
  * `adafruit_hid`

## Wiring

1. Connect your display's SPI or built-in interface to your board (follow your display's wiring guide).
2. Wire the touchscreen pins to your board (e.g., X+, Y+, X–, Y– to analog pins).
3. Ensure USB is connected for HID.

## Installation

1. Copy `code.py` (the main script) to the root of your CIRCUITPY drive.
2. Copy all required library folders from the Adafruit CircuitPython Bundle (displayio, touchscreen, HID) into `lib/` on the CIRCUITPY drive.

## Web Flasher

You can flash the CYD board directly from your browser using the files in
`web-flasher/`. Because WebUSB and the File System Access API both require a
secure context, you must open `index.html` from an HTTPS origin or `localhost`.

1. Start a simple server in this repository (for example
   `python -m http.server`).
2. Navigate to `https://localhost:8000/web-flasher/` (adjust the port if
   needed).
3. Click **Connect** and choose the board's serial port.
4. Click **Flash Firmware** to upload the provided CircuitPython firmware
   (`firmware.uf2` or `firmware.bin`).
5. Once the board resets and the `CIRCUITPY` drive appears, click **Copy
   Libraries** and select that drive. `main.py` and library folders will be
   copied automatically.

## Usage

1. Plug the board into your computer via USB.
2. In a text editor or application, tap buttons on the touchscreen to send corresponding key combinations.
3. Adjust `button_mappings` in `code.py` to change labels and keycodes.

## Configuration

* **Grid Layout**: Edit `COLUMNS` to change number of columns; rows auto-adjust.
* **Button Mappings**: In `button_mappings`, update each entry’s `label` and `keys` array (use `Keycode` values).
* **Touch Calibration**: Update the `calibration` tuple passed to `Touchscreen()` to match your hardware.

```python
# Example entry:
# {"label": "Copy", "keys": [Keycode.CONTROL, Keycode.C]}
```

## Customization

* Swap text labels for icons using `Bitmap` objects and `displayio.TileGrid`.
* Change fill colors in the `Rect` to match your aesthetic.
* Add pages by creating multiple button groups and switching on a mode button.

## Troubleshooting

* **No touch response**: Verify wiring and calibration values.
* **Incorrect keycodes**: Ensure `adafruit_hid.keycode` is imported and used.
* **Debounce issues**: Tweak `time.sleep()` delays in the main loop.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

*Developed by Enrico Trujillo*

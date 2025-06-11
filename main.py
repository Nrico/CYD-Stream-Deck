# main.py for CircuitPython Stream-Deck-style Controller

import time
import board
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import adafruit_touchscreen  # For a resistive touch panel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ——— 1) USB HID Keyboard ———
kbd = Keyboard(usb_hid.devices)

# ——— 2) Display Setup ———
# If your board has a built-in display, this works. Otherwise, set up an external bus.
display = board.DISPLAY
splash = displayio.Group()
display.root_group = splash

# ——— 2b) Touchscreen Setup ———
# Replace these pins & calibration with your hardware’s wiring & values!
ts = adafruit_touchscreen.Touchscreen(
    board.A1, board.A2, board.A3, board.A4,
    calibration=((5200, 300), (5200, 300)),  # adjust these
    size=(display.width, display.height)
)

# ——— 3) Button Definitions ———
# Customize these to suit your favorite shortcuts:
button_mappings = [
    {"label": "Term",  "keys": [Keycode.CONTROL, Keycode.ALT, Keycode.T]},  # Ctrl+Alt+T
    {"label": "Copy",  "keys": [Keycode.CONTROL, Keycode.C]},
    {"label": "Paste", "keys": [Keycode.CONTROL, Keycode.V]},
    {"label": "Undo",  "keys": [Keycode.CONTROL, Keycode.Z]},
    {"label": "Redo",  "keys": [Keycode.CONTROL, Keycode.Y]},
    {"label": "Save",  "keys": [Keycode.CONTROL, Keycode.S]},
    {"label": "New",   "keys": [Keycode.CONTROL, Keycode.N]},
    {"label": "Open",  "keys": [Keycode.CONTROL, Keycode.O]},
    {"label": "AltTab","keys": [Keycode.ALT, Keycode.TAB]},
]

# Grid size
COLUMNS = 3
ROWS = (len(button_mappings) + COLUMNS - 1) // COLUMNS
BW = display.width  // COLUMNS
BH = display.height // ROWS

# ——— 4) Render Buttons ———
buttons = []
for i, mapping in enumerate(button_mappings):
    col = i % COLUMNS
    row = i // COLUMNS
    x0 = col * BW
    y0 = row * BH

    # button background
    rect = Rect(x0, y0, BW, BH, fill=0x222222, outline=0xFFFFFF)
    splash.append(rect)

    # center text
    txt = label.Label(
        terminalio.FONT,
        text=mapping["label"],
        color=0xFFFFFF
    )
    txt.x = x0 + (BW - len(mapping["label"])*6) // 2
    txt.y = y0 + (BH - 8) // 2
    splash.append(txt)

    buttons.append({
        "x0":    x0, "y0":    y0,
        "x1": x0+BW, "y1": y0+BH,
        "keys": mapping["keys"],
        "rect": rect
    })

# ——— 5) Main Loop: Poll & Dispatch ———
while True:
    touch = ts.touch_point
    if touch:
        tx, ty = touch
        for btn in buttons:
            if btn["x0"] < tx < btn["x1"] and btn["y0"] < ty < btn["y1"]:
                # ——— 6) Flash & Send ———
                btn["rect"].fill = 0x555555
                time.sleep(0.1)
                kbd.press(*btn["keys"])
                kbd.release_all()
                btn["rect"].fill = 0x222222
                # simple debounce
                time.sleep(0.3)
                break
    time.sleep(0.05)

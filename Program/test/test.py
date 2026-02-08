import keyboard

keyboard.add_hotkey('alt+q', lambda: print1())

def print1():
    print("КЛАВІШІ")

print("Програма запущена. Натисніть Alt+Z (або Esc для виходу)...")

# Утримує програму активною
keyboard.wait('esc')
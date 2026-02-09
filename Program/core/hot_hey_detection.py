import keyboard
from communications import comm
from PyQt5.QtCore import QObject
import json

class Hot_Key_Detector(QObject):
    def __init__(self):
        super().__init__()
        self.check_ui_data()
        self.get_data()

    def run(self):
        keyboard.add_hotkey('alt+z', lambda: self.start())

    def start(self):
        self.check_ui_data()
        self.get_data()
        if self.method_activation in ["BOTH", "KEYS"]:
            comm.detect_hotkey.emit()

    def get_data(self):
        self.method_activation = self.data.get("general", {}).get("assis_activate")

    def check_ui_data(self):
        with open('pyqt5_ui/settings_ui.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
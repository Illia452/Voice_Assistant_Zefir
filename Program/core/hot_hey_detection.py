import keyboard
from communications import comm
from PyQt5.QtCore import QObject

class Hot_Key_Detector(QObject):
    def __init__(self):
        super().__init__()

    def run(self):
        keyboard.add_hotkey('alt+z', lambda: self.start())

    def start(self):
        print("клааааааааа")
        comm.detect_hotkey.emit()
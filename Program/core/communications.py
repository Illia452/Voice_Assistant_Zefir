from PyQt5.QtCore import QObject, pyqtSignal

class Communications(QObject):
    def __init__(self):
        super().__init__()

    start_push_window = pyqtSignal()
    stop_push_window = pyqtSignal()
    start_gstt = pyqtSignal()
    stop_gstt = pyqtSignal()
    stream_text_gstt = pyqtSignal(str)
    start_search_silence = pyqtSignal()
    final_command = pyqtSignal(str)

comm = Communications()
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
    reset_wakeword = pyqtSignal()
    get_data_ui = pyqtSignal(str)
    change_data_ui = pyqtSignal()
    detect_hotkey = pyqtSignal()
    stop_timer = pyqtSignal()
    focus_on_push = pyqtSignal()
    reset_focus = pyqtSignal()
    text_for_voicework = pyqtSignal(str)
    stop_gtts = pyqtSignal()
    wake_up_feedback = pyqtSignal()
    activate_assistant = pyqtSignal()
    update_history = pyqtSignal()
    start_program = pyqtSignal()
    stop_program = pyqtSignal()
    micro_on = pyqtSignal()
    micro_off = pyqtSignal()

comm = Communications()
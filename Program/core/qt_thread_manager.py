from pyqt5_ui.main_window import UI_MainWindow
from pyqt5_ui.push_window import PushWindow
from wakeword_pipeline.vosk_stt_en import Speech_Recognition
from gstt_processes.logic_gstt import LogicGSTT
from gstt_processes.google_stt import GSTT
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
import asyncio



class Wakeword_Pipeline_Worker(QObject):
    finished = pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        self.speech_recognition = Speech_Recognition()
        asyncio.run(self.speech_recognition.print_text())
        self.finished.emit()



class Google_STT_Worker(QObject):
    finished = pyqtSignal()
    def __init__(self, logic_gstt):
        super().__init__()
        self.logic_gstt = logic_gstt

    def run(self):
        self.google_stt = GSTT(self.logic_gstt)
        self.google_stt.run()


class Thread_Manager():
    def __init__(self):
        self.threads = {}

        self.logic_gstt = LogicGSTT()

    def start_threads(self, name, worker, run_method):
        thread = QThread()
        worker.moveToThread(thread)
        thread.started.connect(run_method)
        worker.finished.connect(thread.quit)
        worker.finished.connect(thread.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        self.threads[name] = {"thread":thread, "worker":worker} 

    def create_wakeword_pipeline(self):
        worker = Wakeword_Pipeline_Worker()
        self.start_threads("wakeword", worker, worker.run)

    def create_googlestt(self):
        worker = Google_STT_Worker(self.logic_gstt)
        self.start_threads("google_stt", worker, worker.run)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    

    ui = UI_MainWindow()
    ui.show()
    push = PushWindow()
    push.hide()
    thread_manager = Thread_Manager()
    thread_manager.create_wakeword_pipeline()
    thread_manager.create_googlestt()

    sys.exit(app.exec_())
from communications import comm
from PyQt5.QtCore import QObject

class LogicGSTT(QObject):
    def __init__(self):
        super().__init__()
        comm.start_gstt.connect(self.activate_and_run)
        comm.stop_gstt.connect(self.stop_process)
        self.active_is = False
        self.stream_audio = None
        
    def activate_and_run(self):
        self.active_is = True
        print(">>>> ЗАПУСК GSTT")

    def stop_process(self):
        self.active_is = False
        self.stream_audio._buff.put(None)

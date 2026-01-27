from communications import comm
from PyQt5.QtCore import QObject, pyqtSlot

class AnalyzeCommand(QObject):
    def __init__(self):
        super().__init__()
        comm.text_command.connect(self.print_command)

    @pyqtSlot(str)
    def print_command(self, text):
        
        print(f'>>> КОМАНДА: {text}')
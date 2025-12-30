from communications import comm

class AnalyzeCommand():
    def __init__(self):
        comm.text_command.connect(self.print_command)

    def print_command(self, text):
        print(text)
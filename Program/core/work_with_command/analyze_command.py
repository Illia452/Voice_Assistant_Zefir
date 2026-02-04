from communications import comm
from PyQt5.QtCore import QObject, pyqtSlot
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from work_with_command.instructions_for_gemini import PROMPT
load_dotenv("../secret_data/gemini_api_key.env")
import time


class AnalyzeCommand(QObject):
    def __init__(self):
        super().__init__()
        comm.final_command.connect(self.start_analyze_command)
        self.client = genai.Client(api_key=os.getenv("API_KEY"))
        self.chat = self.client.chats.create(model="gemini-2.5-flash")



    @pyqtSlot(str)
    def start_analyze_command(self, text):
        print(f'>>> КОМАНДА: {text}')
        self.send_commandtoai(text)


    def send_commandtoai(self, command):


        response = self.chat.send_message(f"{PROMPT}\n\n USER COMMAND: {command}")
        print(response.text)


        # for message in chat.get_history():
        #     print(f'role - {message.role}',end=": ")
        #     print(message.parts[0].text)

        # print(response.text)
        # print(start-time.time())






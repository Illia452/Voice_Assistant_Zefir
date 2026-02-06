from communications import comm
from PyQt5.QtCore import QObject, pyqtSlot
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from work_with_command.instructions_for_gemini import PROMPT
from work_with_command.running_commands import Screenshot
load_dotenv("../secret_data/gemini_api_key.env")
import time
import json



class AnalyzeCommand(QObject):
    def __init__(self):
        super().__init__()
        comm.final_command.connect(self.start_analyze_command)
        self.client = genai.Client(api_key=os.getenv("API_KEY"))
        self.chat = self.client.chats.create(model="gemini-2.5-flash",
                    config={
                        "system_instruction": PROMPT,
                        "response_mime_type": "application/json"
                    }
                                             )



    @pyqtSlot(str)
    def start_analyze_command(self, text):
        print(f'>>> КОМАНДА: {text}')
        self.send_commandtoai(text)


    def send_commandtoai(self, command):

        response = self.chat.send_message(f"USER COMMAND: {command}")
        print(response.text)

        response_json = json.loads(response.text)
        self.analyze_response(response_json)

        # for message in chat.get_history():
        #     print(f'role - {message.role}',end=": ")
        #     print(message.parts[0].text)

        # print(response.text)
        # print(start-time.time())

    def analyze_response(self, response_json):
        command_found = response_json.get("command_found")
        print(command_found)

        if command_found:
            command_id = response_json.get("command_id")
            self.analyze_command_id(command_id)
            
    def analyze_command_id(self, command_id):
        match command_id:
            case "screen":
                print("СКРІН")
            case "set_timer":
                print("ТАЙМЕР")
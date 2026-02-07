from communications import comm
from PyQt5.QtCore import QObject, pyqtSlot
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

from work_with_command.instructions_for_gemini import PROMPT
from work_with_command.running_commands import Screenshot, BrightnessControl 

load_dotenv("../secret_data/gemini_api_key.env")

class AnalyzeCommand(QObject):
    def __init__(self):
        super().__init__()
        comm.final_command.connect(self.start_analyze_command)
        self.client = genai.Client(api_key=os.getenv("API_KEY"))
        
        self.command_workers = {
            "screen": Screenshot(),
            "brightness": BrightnessControl()
        }
        
    def get_fresh_chat(self):
        return self.client.chats.create(
            model="gemini-2.0-flash",
            config={
                "system_instruction": PROMPT,
                "response_mime_type": "application/json"
            }
        )

    @pyqtSlot(str)
    def start_analyze_command(self, text):
        if not text.strip():
            return
        print(f'>>> КОМАНДА: {text}')
        self.process_pipeline(text)


    def process_pipeline(self, user_text):
        chat = self.get_fresh_chat()
        
        response = chat.send_message(f"USER COMMAND: {user_text}")
        data = json.loads(response.text)
        
        command_id = data.get("command_id")
        command_found = data.get("command_found")

        if command_found:
            worker = self.command_workers[command_id]
            worker.create_prompt(user_text)
            
            second_response = chat.send_message(f"NEXT STEP: {worker.PROMPT}")
            
            final_data = json.loads(second_response.text)

            if final_data.get("all_data") == True:
                worker.running_command(final_data)
            
            # if final_data.get("voice_response"):
            #     print(f"VOICE: {final_data['voice_response']}")
        
        else:
            if data.get("voice_response"):
                print(f"INFO: {data['voice_response']}")


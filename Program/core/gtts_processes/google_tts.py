import os
import pyaudio
from google.cloud import texttospeech
from dotenv import load_dotenv
from PyQt5.QtCore import QObject, pyqtSlot
from communications import comm 
import random
import time
import json

class Google_TTS_Model(QObject):
    def __init__(self):
        super().__init__()

        self.check_ui_data()
        self.get_data()

        comm.text_for_voicework.connect(self.get_text)
        comm.stop_gtts.connect(self.close_all)
        comm.wake_up_feedback.connect(self.get_activation_phrase)

        load_dotenv("../secret_data/apikey_tts.env")
        api_key = os.getenv("API_KEY")
        client_options = {"api_key": api_key}
        self.client = texttospeech.TextToSpeechClient(client_options=client_options)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=24000,
                                output=True)


        self.streaming_config = texttospeech.StreamingSynthesizeConfig(
            voice=texttospeech.VoiceSelectionParams(
                name="uk-UA-Chirp3-HD-Charon",
                language_code="uk-UA",
            )
        )

    def get_data(self):
        self.method_activation = self.data.get("voice", {}).get("voice_support")

    def check_ui_data(self):
        with open('pyqt5_ui/settings_ui.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        

    @pyqtSlot()
    def get_activation_phrase(self):
        phrases = [
            "Слухаю вас.",
            "Я на зв’язку.",
            "До ваших послуг.",
            "Так?",
            "Кажіть.",
            "Слухаю.",
            "Слухаю уважно.",
            "Чим можу допомогти?"
        ]
        text = random.choice(phrases)
        self.get_text(text)
        time.sleep(0.4)
        comm.start_gstt.emit()



    @pyqtSlot(str)
    def get_text(self, text):
        self.check_ui_data()
        self.get_data()
        if not text or self.method_activation == False:
            return

        print(f"Озвучую: {text}")

        def request_generator():
            yield texttospeech.StreamingSynthesizeRequest(streaming_config=self.streaming_config)
            yield texttospeech.StreamingSynthesizeRequest(
                input=texttospeech.StreamingSynthesisInput(text=text)
            )

        try:
            responses = self.client.streaming_synthesize(request_generator())

            for response in responses:
                if response.audio_content:
                    self.stream.write(response.audio_content)
        except Exception as e:
            print(f"Error TTS: {e}")

    def close_all(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
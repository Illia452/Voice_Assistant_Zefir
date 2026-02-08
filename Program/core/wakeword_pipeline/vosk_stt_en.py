from vosk import Model, KaldiRecognizer
import pyaudio
import numpy as np
import noisereduce as nr
from pydub import AudioSegment
import json
from wakeword_pipeline.wakeword_logic import WakeWordChecker, SilenceSearcher
import asyncio
from PyQt5.QtCore import QObject

class Speech_Recognition(QObject):
    def __init__(self, loop=None):
        model = Model(r'..\..\models\speech_to_text\vosk-model-small-en-us-0.15')
        self.recognizer = KaldiRecognizer(model, 16000)

        self.wakeword_checker = WakeWordChecker(loop=loop)
        self.silence_searcher = SilenceSearcher()
        
        cap = pyaudio.PyAudio()

        self.stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
        self.stream.start_stream()


    async def delete_noise(self):
        data = await asyncio.to_thread(self.stream.read, 4096)
        masiv = np.frombuffer(data, dtype=np.int16) # Перетворення байтових даних в масив
        audio_without_noise = nr.reduce_noise(y=masiv, sr=16000) # Зняття шуму з аудіопотоку
        self.bytes_audio = audio_without_noise.astype(np.int16).tobytes() # Конвертація масиву в байти


    async def volume_up(self):
        audio_segment = AudioSegment(
        data=self.bytes_audio,
        sample_width=2,    # 16 бітний формат (= 2 байти)
        frame_rate=16000,   
        channels=1         
        )
        self.str_audio = audio_segment + 6 
        audio_np = np.array(self.str_audio.get_array_of_samples(), dtype=np.int16) # перетворення у numpy масив
        self.final_audio = audio_np.tobytes() # перетворення у байти
        await self.silence_searcher.search_silence(self.str_audio)
        

    async def delete_none_results(self, res_key):
        if len(self.result[res_key]) == 0:
            return
        else:
            self.text = (self.result[res_key])
            print(self.text)
            await self.wakeword_checker.check_wakeword_status(self.text)
            self.text = None


    async def speech_to_text(self):
        if self.recognizer.AcceptWaveform(self.final_audio): 
            rec = self.recognizer.Result()
            self.result = json.loads(rec)
            await self.delete_none_results("text")
                                
        else:
            # постійне прослуховування аудіо з реальним виведенням
            rec = self.recognizer.PartialResult()
            self.result = json.loads(rec)
            await self.delete_none_results("partial")


    async def print_text(self):
        while True:
            await self.delete_noise()
            await self.volume_up()
            await self.speech_to_text()
            

if __name__ == "__main__":
    speech_recognition = Speech_Recognition()
    asyncio.run(speech_recognition.print_text())
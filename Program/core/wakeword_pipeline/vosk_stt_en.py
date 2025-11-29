from vosk import Model, KaldiRecognizer
import pyaudio
import numpy as np
import noisereduce as nr
from pydub import AudioSegment
import json
from detect_wakeword import WakeWordChecker

class Recognition_Speech():
    def __init__(self):
        model = Model(r'..\..\..\models\speech_to_text\vosk-model-small-en-us-0.15')
        self.recognizer = KaldiRecognizer(model, 16000)

        self.wakeword_checker = WakeWordChecker()
        
        cap = pyaudio.PyAudio()

        self.stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
        self.stream.start_stream()


    def delete_noise(self):
        data = self.stream.read(4096) 
        masiv = np.frombuffer(data, dtype=np.int16) # Перетворення байтових даних в масив
        audio_without_noise = nr.reduce_noise(y=masiv, sr=16000) # Зняття шуму з аудіопотоку
        self.bytes_audio = audio_without_noise.astype(np.int16).tobytes() # Конвертація масиву в байти


    def volume_up(self):
        audio_segment = AudioSegment(
        data=self.bytes_audio,
        sample_width=2,    # 16 бітний формат (= 2 байти)
        frame_rate=16000,   
        channels=1         
        )
        self.str_audio = audio_segment + 6 
        audio_np = np.array(self.str_audio.get_array_of_samples(), dtype=np.int16) # перетворення у numpy масив
        self.final_audio = audio_np.tobytes() # перетворення у байти
        

    def delete_none_results(self, res_key):
        if len(self.result[res_key]) == 0:
            return
        else:
            self.text = (self.result[res_key])
            self.wakeword_checker.check_wakeword_status(self.text)
            print(self.text)
            self.text = None


    def speech_to_text(self):
        if self.recognizer.AcceptWaveform(self.final_audio): 
            rec = self.recognizer.Result()
            self.result = json.loads(rec)
            self.delete_none_results("text")
                                
        else:
            # постійне прослуховування аудіо з реальним виведенням
            rec = self.recognizer.PartialResult()
            self.result = json.loads(rec)
            self.delete_none_results("partial")


    def print_text(self):
        while True:
            self.delete_noise()
            self.volume_up()
            self.speech_to_text()
            

if __name__ == "__main__":
    speech_recognition = Recognition_Speech()
    speech_recognition.print_text()
import time
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.find_silence import detect_silence
from PyQt5.QtCore import QObject, pyqtSignal
from communications import comm

class WakeWordChecker():
    def __init__(self):
        self.uk_list_wakewords = ["заір","зельфія","опір", "зір зефір", "зір зоря", "зегер", "дзеффіреллі",
        "зефір","захід", "з ефір", "ефір", "земфіра", "засіяти", "захир", "захір", "за часів","часів",
        "за шию", "зефірс", "захер", "захур", "заньєр", "за кар'єру", "звір", "зір", "жахів", "вже ефір",
        "жаль зір", "вважає р","зір","жаль зір","вже ефір","вже зір","жан-п'єр","ефір","взявши р",
        "режисер","уже","твір","лея","в ефірі","наші","сесій","між ефіру","сім","одесі","це гір","вечір",
        "ігор","жахів","спікер","вже фірм","р","це зір","цей твір","герой"]
        
        self.en_list_wakewords = ["the fear", "this year", "is fear", "zero fear", "zephyr",
        "they feed", "the field", "the here", "is here", "effective here", "if is few", "it's a few", "see it", 
        "the ship", "last year", "there's a few", "live here", "the sheer", "they fear",
        "the therefore", "the food", "as i fea", "the share", "they feel", "the feel", "the fee"]

        self.speech_waiter = SpeechWaiter()
        self.logic_after_wakeword = LogicAfterWakeWord()
        self.is_wakeword = False
        self.time_wakeword = 0

    async def check_wakeword_status(self, text):
        if self.is_wakeword:

            cooldown = time.time() - self.time_wakeword

            if cooldown < 1.25:
                return
            else:
                self.timer.cancel()
                # listen command
                # search silence 
                comm.start_search_silence.emit()
        else:
            await self.search_wakeword(text)


    async def search_wakeword(self, text):
        for wakeword in self.en_list_wakewords:
            if wakeword in text:
                print("Є КЛючове слово")

                self.time_wakeword = time.time()
                self.is_wakeword = True
                self.logic_after_wakeword.actions_after_wakeword()
                #launch gstt
                await self.start_timer()
                break

    async def start_timer(self):
        self.timer = asyncio.create_task(
            self.speech_waiter.check_wait_time(self)
            )
        

class SpeechWaiter():
    async def check_wait_time(self, wakeword_cheker):

        try:
            await asyncio.sleep(5)
            print("ЧАС ОЧІКУВАННЯ МОВЛЕННЯ МИНУВ")
            comm.stop_gstt.emit()
            wakeword_cheker.is_wakeword = False

        except asyncio.CancelledError:
            print("ТАйМЕР СКАСОВАНО БО Є МОВЛЕННЯ")
            wakeword_cheker.is_wakeword = False



class LogicAfterWakeWord(QObject):
    def __init__(self):
        super().__init__()

    def actions_after_wakeword(self):
        comm.start_push_window.emit()
        comm.start_gstt.emit()



class SilenceSearcher():
    def __init__(self):
        self.list_audio = []
        comm.start_search_silence.connect(self.activate_searcher)
        self.active_is = False

    async def search_silence(self, audio):   # пошук тиші в аудіопотоці
        if self.active_is:
            self.list_audio.append(audio) # додавання фрагментів після підвищення гучності
            united_audio = sum(self.list_audio) # об'єднання цих фрагментів 
            self.list_silence = detect_silence(united_audio, min_silence_len=500, silence_thresh=-40, seek_step=100) # налаштування для функції тиші

            for silence in self.list_silence:
                if (silence[1] - silence[0]) >= 2800: # шукаємо тишу в 1800мс
                    print("ЗНАЙДЕНО ТИШУ")
                    comm.stop_push_window.emit()
                    comm.stop_gstt.emit()
                    self.active_is = False
                    self.list_silence = []
    
                    break

    def activate_searcher(self):
        self.active_is = True

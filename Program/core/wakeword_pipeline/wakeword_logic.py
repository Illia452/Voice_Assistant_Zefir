import time
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.find_silence import detect_silence
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from communications import comm

class WakeWordChecker(QObject):
    def __init__(self, loop=None):
        super().__init__()
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
        self.loop = loop

        self.speech_waiter = SpeechWaiter()
        self.logic_after_wakeword = LogicAfterWakeWord()
        self.is_wakeword = False
        self.time_wakeword = 0
        comm.reset_wakeword.connect(self.reset_wakeword)
        comm.stop_timer.connect(self.reset_timer)
        comm.detect_hotkey.connect(self.hot_key_detect, Qt.DirectConnection)

    async def check_wakeword_status(self, text):
        if self.is_wakeword:

            cooldown = time.time() - self.time_wakeword

            if cooldown < 1.25:
                return
            else:
                comm.stop_timer.emit()
                # listen command
                # search silence 
                comm.start_search_silence.emit()
        else:
            await self.search_wakeword(text)

    async def activate_assistant(self):
        self.time_wakeword = time.time()
        self.is_wakeword = True
        self.logic_after_wakeword.actions_after_wakeword()
        await self.start_timer() 


    async def search_wakeword(self, text):
        for wakeword in self.en_list_wakewords:
            if wakeword in text:
                print("Є КЛючове слово")
                await self.activate_assistant()
                break

    async def start_timer(self):
        self.timer = asyncio.create_task(
            self.speech_waiter.check_wait_time(self)
            )
        
    @pyqtSlot()    
    def reset_timer(self):
        self.timer.cancel()

    @pyqtSlot() 
    def reset_wakeword(self):
        self.is_wakeword = False

    @pyqtSlot()
    def hot_key_detect(self):
        if not self.is_wakeword:
            if self.loop and self.loop.is_running():
                self.loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(self.activate_assistant())
                )
        
class SpeechWaiter(QObject):
    def __init__(self):
        super().__init__()

        self.focus_on_push = False

        comm.focus_on_push.connect(self.focus_true, Qt.DirectConnection)


    async def check_wait_time(self, wakeword_cheker):

        try:
            await asyncio.sleep(5)
            print("ЧАС ОЧІКУВАННЯ МОВЛЕННЯ МИНУВ")
            comm.stop_gstt.emit()
            comm.reset_wakeword.emit()

            if not self.focus_on_push:
                comm.stop_push_window.emit()

        except asyncio.CancelledError:
            print("ТАйМЕР СКАСОВАНО БО Є МОВЛЕННЯ")

    def focus_true(self):
        self.focus_on_push = True

        comm.stop_gstt.emit()
        comm.reset_wakeword.emit()




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
                if (silence[1] - silence[0]) >= 2800: # шукаємо тишу в 2800мс
                    print("ЗНАЙДЕНО ТИШУ")

                    self.active_is = False
                    self.list_audio = []

                    comm.stop_push_window.emit()
                    comm.stop_gstt.emit()
                    comm.reset_wakeword.emit()
    
                    break

    def activate_searcher(self):
        self.list_audio = []
        self.active_is = True

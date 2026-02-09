import time
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.find_silence import detect_silence
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from communications import comm
import json

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
        self.is_wakeword = False
        self.time_wakeword = 0
        comm.reset_wakeword.connect(self.reset_wakeword)
        comm.stop_timer.connect(self.reset_timer)
        comm.detect_hotkey.connect(self.hot_key_detect, Qt.DirectConnection)

        self.focus_on_push = False
        comm.focus_on_push.connect(self.focus_true, Qt.DirectConnection)
        comm.reset_focus.connect(self.focus_false, Qt.DirectConnection)

        comm.activate_assistant.connect(self.assistant_on, Qt.DirectConnection)

        with open('pyqt5_ui/settings_ui.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.method_activation = self.data.get("general", {}).get("assis_activate")
        

    async def check_wakeword_status(self, text):
        if self.focus_on_push == True:
            return
        if self.is_wakeword:

            cooldown = time.time() - self.time_wakeword

            if cooldown < 1.25:
                return
            else:
                comm.stop_timer.emit()

                comm.start_search_silence.emit()
        else:
            await self.check_settings_ui(text)


    async def activate_assistant(self):
        if not self.focus_on_push:
            comm.wake_up_feedback.emit()
            comm.start_push_window.emit()
        self.time_wakeword = time.time()
        self.is_wakeword = True
                
        await self.start_timer() 


    async def search_wakeword(self, text):
        for wakeword in self.en_list_wakewords:
            if wakeword in text:
                print("Є КЛючове слово")
                comm.activate_assistant.emit()
                break

    async def start_timer(self):
        self.timer = asyncio.create_task(
            self.speech_waiter.check_wait_time(self)
            )
        
    async def check_settings_ui(self, text):
        await self.check_ui_data()
        await self.get_data()
        if self.method_activation in ["VOICE", "BOTH"]:
            await self.search_wakeword(text)
        
    async def get_data(self):
        self.method_activation = self.data.get("general", {}).get("assis_activate")

    async def check_ui_data(self):
        with open('pyqt5_ui/settings_ui.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
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

    @pyqtSlot()
    def focus_true(self):
        if not self.focus_on_push:
            self.focus_on_push = True
            comm.stop_gstt.emit()
            comm.reset_wakeword.emit()

    @pyqtSlot()
    def focus_false(self):
        self.focus_on_push = False

    @pyqtSlot()
    def assistant_on(self):
        if not self.is_wakeword:
            if self.loop and self.loop.is_running():
                self.loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(self.activate_assistant())
                )


        
class SpeechWaiter(QObject):
    def __init__(self):
        super().__init__()


    async def check_wait_time(self, wakeword_logic):

        try:
            await asyncio.sleep(5)
            print("ЧАС ОЧІКУВАННЯ МОВЛЕННЯ МИНУВ")
            comm.stop_gstt.emit()
            comm.reset_wakeword.emit()
            if wakeword_logic.focus_on_push == False:
                comm.stop_push_window.emit()

        except asyncio.CancelledError:
            print("ТАйМЕР СКАСОВАНО БО Є МОВЛЕННЯ")
            







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

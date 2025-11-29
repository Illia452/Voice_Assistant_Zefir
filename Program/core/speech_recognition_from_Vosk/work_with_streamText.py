import time
import sys
import os
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utils.find_silence import detect_silence

class Work_withTexts_FromVosk(QObject):

    start_listen = pyqtSignal()
    stop_listen = pyqtSignal()
    start_Push = pyqtSignal()
    close_Push = pyqtSignal()
    google_docs_text_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.uk_list_key_words = ["заір","зельфія","опір", "зір зефір", "зір зоря", "зегер", "дзеффіреллі",
        "зефір","захід", "з ефір", "ефір", "земфіра", "засіяти", "захир", "захір", "за часів","часів",
        "за шию", "зефірс", "захер", "захур", "заньєр", "за кар'єру", "звір", "зір", "жахів", "вже ефір",
        "жаль зір", "вважає р","зір","жаль зір","вже ефір","вже зір","жан-п'єр","ефір","взявши р",
        "режисер","уже","твір","лея","в ефірі","наші","сесій","між ефіру","сім","одесі","це гір","вечір",
        "ігор","жахів","спікер","вже фірм","р","це зір","цей твір","герой"]
        
        self.en_list_key_words = ["the fear", "this year", "is fear", "zero fear", "zephyr",
        "they feed", "the field", "the here", "is here", "effective here", "if is few", "it's a few", "see it", 
        "the ship", "last year", "there's a few", "live here", "the sheer", "they fear",
        "the therefore", "the food", "as i fea", "the share", "they feel", "the feel", "the fee"]
        self.time_passed_after_openPush = 0
        self.iSdetect_key_word = False
        self.pushIS_Active = False
        self.start_write_text = False
        self.isText = False
        self.time_wait_passed = False
        self.find_silence = False
        self.list_audio = []




    def check_whether_detectedKW(self, text):
        if self.iSdetect_key_word:
            self.startPushWindow_GetText()
        else:
            self.find_keyWord(text)

    

    def find_keyWord(self, text_from_streamVosk):
        for key_word in self.en_list_key_words:
            if key_word in text_from_streamVosk:
                self.steps_after_DetectKeyWord()
                break

    def steps_after_DetectKeyWord(self):
        self.iSdetect_key_word = True
        print("КЛЮЧОВЕ СЛОВО РОЗПІЗНАНО")


    def startPushWindow_GetText(self):
        if self.pushIS_Active == False:
            self.pushIS_Active = True
            time.sleep(1)
            self.start_listen.emit()
            self.start_Push.emit()
            self.time_open_push = time.time()
            time.sleep(0.1)
            self.start_write_text = True
        else:
            self.steps_if_PushWindow_active()

    def steps_if_PushWindow_active(self):
        if self.isText == False:
            self.time_passed_after_openPush = time.time() - self.time_open_push
            print(f"ЧАС ОЧІКУВАННЯ: {self.time_passed_after_openPush}")
            self.check_how_Many_time_passed_after_openPush()
        else:
            self.check_whether_find_silence()


    def check_whether_find_silence(self):
        if self.find_silence:
            self.steps_if_found_silence()

    def steps_if_found_silence(self):
        print("КРОКИ ПІСЛЯ ТОГО ЯК БУЛО ЗНАЙДЕНО ТИШУ")
        self.iSdetect_key_word = False
        self.pushIS_Active = False
        self.start_write_text = False
        self.time_wait_passed = False

        self.isText = False
        self.close_Push.emit()
        time.sleep(0.2)
        self.stop_listen.emit()


    def steps_if_time_passed(self):
        print("Кроки після витоку часу")
        self.iSdetect_key_word = False
        self.pushIS_Active = False
        self.start_write_text = False
        self.time_wait_passed = False
        self.stop_listen.emit()
        time.sleep(10)
        self.close_Push.emit()


    def check_how_Many_time_passed_after_openPush(self):
        if self.time_passed_after_openPush > 4.8:
            self.time_wait_passed = True

    
    def status_text_OFF(self):
        self.isText = False

    def status_text_ON(self):
        self.isText = True

    def status_find_silence_OFF(self):
        self.find_silence = False
            

    def get_data_about_audio(self, data_audio):
        if self.isText == True:
            self.data_audio = data_audio
            self.search_silence(self.data_audio)
        else:
            self.data_audio = None




    def search_silence(self, audio):   # пошук тиші в аудіопотоці
        self.list_audio.append(audio) # додавання фрагментів після підвищення гучності
        united_audio = sum(self.list_audio) # об'єднання цих фрагментів 
        self.list_silence = detect_silence(united_audio, min_silence_len=500, silence_thresh=-40, seek_step=100) # налаштування для функції тиші

        for silence in self.list_silence:
            if (silence[1] - silence[0]) >= 2800: # шукаємо тишу в 1800мс
                print("ЗНАЙДЕНО ТИШУ")
                self.find_silence = True 
                self.list_audio = []
                united_audio = None
                break


    def send_command(self, command):
        print(f"НАША КОМАНДА: {command}")


    @pyqtSlot(str) # Декоратор, що вказує, що це слот, який приймає рядок
    def receive_google_docs_text(self, text_content):
        self.google_docs_text_available.emit(text_content)




    # def startPushWindow_GetText(self):
    #     if self.pushIS_Active == False:
    #         self.pushIS_Active = True
    #         time.sleep(1)
    #         self.control_signals.open_PushWindow()
    #         self.time_open_push = time.time()
    #         time.sleep(0.1)
    #         self.control_signals.start_write_text_inPush()
    #     else:
    #         self.steps_if_PushWindow_active()

    # def steps_if_PushWindow_active(self):
    #     if self.isText == False:
    #         self.time_passed_after_openPush = time.time() - self.time_open_push
    #         self.check_how_Many_time_passed_after_openPush()



            

    # def change_status_isText_(self):
    #     self.isText = True



    # def waitSpeechAfterDetectedKW(self, iStext):
    #     self.time_that_passed = time.time() - self.time_detected_keyword
    #     print(f"ЧАС: {self.time_that_passed} ЧИ Є ТЕКСТ: {iStext}")
    #     if 1.5 <= self.time_that_passed:
    #         if iStext:

    #             time.sleep(2)

    #             #запускаємо мікро в докс
    #         elif iStext != True and 4.8 <= self.time_that_passed:
    #             self.iSdetect_key_word = False
    #             print("ЧАС ОЧІКУВАННЯ МИНУВ")

from actions_after_wakeword import SpeechWaiter
import time

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
        self.is_wakeword = False



    def check_wakeword_status(self, text):
        if self.is_wakeword:
            # cancel timer
            self.is_wakeword = False
        else:
            self.search_wakeword(text)
    def search_wakeword(self, text):
        for wakeword in self.en_list_wakewords:
            if wakeword in text:
                print("Є КЛючове слово")
                self.is_wakeword = True
                #launch pushwindow
                #launch stt
                self.speech_waiter.

                
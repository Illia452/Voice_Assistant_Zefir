import asyncio
import time

class SpeechWaiter():
    def __init__(self):
        pass
    def check_wait_time(self, time_wakeword):
        if time.time() - time_wakeword > 5:
            print("ЧАС МИНУВ")
        else:
        
            
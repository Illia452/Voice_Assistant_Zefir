import asyncio
import time

class SpeechWaiter():
    def __init__(self):
        pass
    
    async def check_wait_time(self, wakeword_cheker):

        try:
            await asyncio.sleep(6)
            print("ЧАС ОЧІКУВАННЯ МОВЛЕННЯ МИНУВ")
            wakeword_cheker.is_wakeword = False

        except asyncio.CancelledError:
            print("ТАйМЕР СКАСОВАНО БО Є МОВЛЕННЯ")
            wakeword_cheker.is_wakeword = False
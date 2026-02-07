from screeninfo import get_monitors
import json
import mss
import mss.tools
import os
import time

class Screenshot():
    def __init__(self):
        self.monitor_count = 0
        self.PROMPT = []
        with open('pyqt5_ui/settings_ui.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        

    def get_data(self):
        self.monitor_count = len(get_monitors())
        self.format = self.data.get("screenshot", {}).get("format")
        self.path = self.data.get("screenshot", {}).get("path")

    def check_ui_data(self):
        with open('pyqt5_ui/settings_ui.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def create_prompt(self, user_command):
        self.check_ui_data()
        self.get_data()


        self.PROMPT = (f"""ЗАВДАННЯ: Оброби команду "Screenshot".

                ПОТОЧНІ НАЛАШТУВАННЯ ТА СТАН:
                - Формат: {self.format} (JPG/PNG)
                - Шлях збереження: {self.path} (Default)
                - Кількість екранів: {self.monitor_count}

                КОМАНДА КОРИСТУВАЧА: "{user_command}"

                ТВОЯ ЛОГІКА:
                1. Якщо екранів > 1 і не вказано який — ти ПОВИНЕН запитати на якому екрані робити скрін"..
                3. Якщо користувач каже одні дані, а за замовчуванням у нас інше беремо у пріорітет дані користувача(наприклад: за замвчуванням у нас стоїть формат jpg, але користувач хоче зробити скрін у форматі png - беремо дані корисутувача)
                
                ВІДПОВІДЬ ТИ ПОВИНЕН ДАТИ JSON
                тобто це будуть дані щоб виконати цю команду

                "all_data": "bool" (True/False) - чи усі дані зібрані? Якщо так то - true/ ні - false(продовжуємо допитувати дані у користувача)
                "monitor": "str" (1/2/3/0), - якого монітора скрін робити? 0 - це всіх моніторів, 1 - це першого, 2 - це другого ітд
                "format": "str" (JPG/PNG), - у якому форматі робити скрін
                "path": "str" {self.path},
                "voice_response": "Текст, який буде озвучено користувачу"
                
                """)
        
        print(self.PROMPT)

    def running_command(self, text):
        response = text
        monitor = response.get("monitor")
        format = response.get("format")
        path = response.get("path")



        self.take_screenshot(monitor, path, format)


    def take_screenshot(self, monitor_index, save_path, file_format):

        time.sleep(0.2)
        with mss.mss() as sct:
            # Створюємо папку, якщо її немає
            os.makedirs(save_path, exist_ok=True)
            
            # Вибираємо монітор та робимо знімок
            monitor = sct.monitors[int(monitor_index)]
            screenshot = sct.grab(monitor)

            # Формуємо шлях та зберігаємо
            filename = f"screenshot_mon_{monitor_index}.{file_format}"
            output = os.path.join(save_path, filename)

            # mss зберігає у PNG
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=output)
            print(f"Збережено: {output}")
    # Приклад використання:
    # Зняти другий монітор (якщо є) і зберегти в папку 'my_pics'

from screeninfo import get_monitors
import json
import mss
import mss.tools
import os
import time
import screen_brightness_control as sbc 
import subprocess
import webbrowser

class Screenshot():
    def __init__(self):
        self.monitor_count = 0
        self.PROMPT = "" 
        self.data = {}
        self.check_ui_data()

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
                
                КОМАНДА КОРИСТУВАЧА: "{user_command}"

                ТВОЯ ЛОГІКА:
                1. Якщо екранів > 1 і не вказано який — ти ПОВИНЕН запитати на якому екрані робити скрін"..
                2. Якщо користувач каже одні дані, а за замовчуванням у нас інше беремо у пріорітет дані користувача
                (наприклад: за замвчуванням у нас стоїть формат jpg, але користувач хоче зробити скрін у форматі png - беремо дані корисутувача)

                ПОТОЧНІ НАЛАШТУВАННЯ ТА СТАН:
                - Формат: {self.format} (JPG/PNG)
                - Шлях збереження: {self.path} (Default)
                - Кількість екранів: {self.monitor_count}
                
                <output_format>
                Поверни JSON:
                {{
                    "monitor": "str" (1/2/3/0) - 0 це всі дисплеї, 1 - перший дисплей,
                    "format": "str", (JPG/PNG)
                    "path": "str", 
                    "voice_response": "Текст озвучки" - (в кінці речення обов'язоково ставимо КРАПКУ), 
                    "all_data": true (чи усі дані зібрані? Якщо так то - true/ ні - false(продовжуємо допитувати дані у користувача))
                }}
                </output_format>
                """)


    def running_command(self, response_json): # Змінив аргумент на json для універсальності
        monitor = response_json.get("monitor")
        format = response_json.get("format")
        path = response_json.get("path")


        self.take_screenshot(monitor, path, format)

    def take_screenshot(self, monitor_index, save_path, file_format):

        time.sleep(0.2)

        with mss.mss() as sct:

            os.makedirs(save_path, exist_ok=True)
            
            monitor = sct.monitors[int(monitor_index)]
            screenshot = sct.grab(monitor)

            filename = f"screenshot_mon_{monitor_index}.{file_format}"
            output = os.path.join(save_path, filename)

            mss.tools.to_png(screenshot.rgb, screenshot.size, output=output)
            print(f"Збережено: {output}")


class BrightnessControl():
    def __init__(self):
        self.PROMPT = ""
    
    def create_prompt(self, user_command):
        try:
            current_brightness = sbc.get_brightness()[0]
        except:
            current_brightness = 50 # якщо помилка вважаємо середнє

        self.PROMPT = (f"""ЗАВДАННЯ: Оброби команду зміни яскравості.
        
        КОМАНДА КОРИСТУВАЧА: "{user_command}"
        
        СТАН СИСТЕМИ:
        - Поточна яскравість: {current_brightness}%
        
        Твоя задача: Вирахувати нову яскравість на основі слів користувача.
        - Якщо каже "збільш", додай 10-20%.
        - Якщо "зменш", відніми.
        - Якщо "постав 100", постав 100.
        - Максимум 100, мінімум 0.
        
        <output_format>
        Поверни JSON:
        {{
            "new_brightness_value": int (0-100),
            "voice_response": "Текст, наприклад: 'Яскравість 70 відсотків'" - (в кінці речення обов'язоково ставимо КРАПКУ),
            "all_data": true
        }}
        </output_format>
        """)

    def running_command(self, response_json):
        new_val = response_json.get("new_brightness_value")
        if new_val is not None:

            sbc.set_brightness(new_val)
            print(f"Яскравість змінено на {new_val}")
            

class AppControl:
    def __init__(self):
        self.PROMPT = ""
        self.apps_list = []

    def get_installed_apps(self):
        # список імен програм які бачить вінда
        cmd = 'powershell "Get-StartApps | Select-Object Name | ConvertTo-Json"'
        result = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
        data = json.loads(result)
        return [app['Name'] for app in data]


    def create_prompt(self, user_command):
        self.apps_list = self.get_installed_apps()
        
        self.PROMPT = f"""
        ЗАВДАННЯ: Запуск програм у Windows.
        КОРИСТУВАЧ СКАЗАВ: "{user_command}"
        СПИСОК ВСТАНОВЛЕНИХ ПРОГРАМ (EXE/Ярлики): {", ".join(self.apps_list)}

        Твоя задача:
        1. Визнач, чи хоче користувач відкрити системний додаток Windows (UWP) чи звичайну програму зі списку.
        2. Якщо додаток системний (Калькулятор, Налаштування, Камера, Календар, Фото тощо), згенеруй відповідну команду 'start [протокол]:'.
        3. Якщо додаток є у списку встановлених програм, вибери точну назву.
        4. Якщо назва не точна, вибери найбільш схожу.

        Поверни ТІЛЬКИ JSON:
        {{
            "app_name": "Назва зі списку АБО null, якщо це системний протокол",
            "system_command": "Команда (наприклад: 'start calculator:') АБО null, якщо це звичайна програма",
            "voice_response": "Запускаю [Назва]" - (в кінці речення обов'язоково ставимо КРАПКУ),
            "all_data": true,
            "is_system": true/false
        }}

        ПІДКАЗКА ПО СИСТЕМНИМ ПРОТОКОЛАМ:
        - Калькулятор: start calculator:
        - Налаштування/Параметри: start ms-settings:
        - Камера: start microsoft.windows.camera:
        - Календар: start outlookcal:
        - Магазин (Store): start ms-windows-store:
        - Фото: start ms-photos:
        - Пошта: start mailto:
        - Браузер Edge: start microsoft-edge:
        """

    def running_command(self, response_json):
        is_system = response_json.get("is_system", False)
        system_cmd = response_json.get("system_command") # Наприклад: "start microsoft.windows.camera:"
        app_name = response_json.get("app_name")


        if is_system and system_cmd:
            protocol = system_cmd.replace("start ", "").strip()
            print(f">>> Спроба відкрити протокол: {protocol}")
            os.startfile(protocol) 
            return


        if app_name:
            print(f">>> Шукаю AppID для: {app_name}")
            cmd = f'powershell "Start-Process shell:AppsFolder\\$((Get-StartApps | Where-Object {{ $_.Name -eq \'{app_name}\' }}).AppID)"'
            subprocess.Popen(cmd, shell=True)


class WebControl:
    def __init__(self):
        self.PROMPT = ""

    def create_prompt(self, user_command):
        self.PROMPT = f"""
        ЗАВДАННЯ: Відкрити веб-сайт або знайти інформацію.
        КОРИСТУВАЧ СКАЗАВ: "{user_command}"

        Твоя задача:
        1. Визнач, який сайт хоче користувач (наприклад, "ютуб" -> "https://www.youtube.com").
        2. Якщо це конкретний запит на пошук (наприклад, "знайди як варити борщ"), сформуй посилання на Google пошук: 
           "https://www.google.com/search?q=як+варити+борщ"
        
        Поверни JSON:
        {{
            "url": "повне посилання з https://",
            "voice_response": "Відкриваю [назва сайту]" - (в кінці речення обов'язоково ставимо КРАПКУ),
            "all_data": true
        }}
        """

    def running_command(self, response_json):
        url = response_json.get("url")
        if url:
            webbrowser.open_new_tab(url)
            print(f">>> СИСТЕМА: Відкрито посилання {url}")
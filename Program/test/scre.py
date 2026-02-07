import mss
import mss.tools
import os
import json

class ScreenshotManager:
    def running_command(self, text):
        # Декодуємо JSON-команду
        response = json.loads(text)
        monitor = response.get("monitor")
        format = response.get("format", "png")
        path = response.get("path", "screenshots")

        self.take_screenshot(monitor, path, format)

    def take_screenshot(self, monitor_index, save_path, file_format):
        with mss.mss() as sct:
            # --- ДІАГНОСТИКА (видалить після перевірки) ---
            print(f"Знайдено моніторів: {len(sct.monitors) - 1}")
            for i, m in enumerate(sct.monitors):
                print(f"Монітор {i}: {m}")
            # ---------------------------------------------

            # Створюємо папку
            os.makedirs(save_path, exist_ok=True)
            
            # Перетворюємо індекс у ціле число
            try:
                idx = int(monitor_index)
            except (ValueError, TypeError):
                idx = 1 # якщо прийшло щось дивне, беремо перший монітор

            # Перевірка наявності монітора
            if idx >= len(sct.monitors):
                print(f"Помилка: Монітора {idx} не існує. Вибираю доступний.")
                idx = len(sct.monitors) - 1

            # Захоплюємо екран
            monitor_data = sct.monitors[idx]
            screenshot = sct.grab(monitor_data)

            # Формуємо шлях
            filename = f"screenshot_mon_{idx}.{file_format}"
            output = os.path.join(save_path, filename)

            # Зберігаємо
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=output)
            print(f"Збережено скріншот монітора {idx} за шляхом: {output}")


sm = ScreenshotManager()
sm.running_command('{"monitor": 2, "format": "png", "path": "C:/Screens"}')
import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import win32gui
from pywinauto import Application
import pygetwindow as gw



class WindowSelenium():

    def __init__(self):
        load_dotenv("../secret_data/inf.env")
        self.unique_title = "MySupereWindow_12345"
        options = uc.ChromeOptions()

        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--allow-file-access-from-files")
        options.add_argument("--use-fake-device-for-media-stream")

        self.driver = uc.Chrome(options=options)


        self.selenium_running = True

    def delay_lvl1(self):
        time.sleep(random.uniform(2, 4))

    def delay_lvl2(self):
        time.sleep(random.uniform(5, 7))



    def getting_HWMD(self):
    # driver.set_window_position(10000, 100)
        self.driver.get(f"data:text/html,<title>{self.unique_title}</title>")

        # Знаходимо вікно по заголовку
        window = gw.getWindowsWithTitle(self.unique_title)[0]
        hwnd = window._hWnd
        print(f"HWND: {hwnd}")

        # Підключаємось до цього вікна через PyWinAuto
        app = Application(backend="win32").connect(handle=hwnd)
        self.win = app.window(handle=hwnd).wrapper_object()
        self.win.set_focus()


    
    def move_WindowOutsideDisplay(self):
        # Переміщаємо вікно за межі екрана 
        self.win.move_window(x=0, y=0, width=1920, height=1080)

        # Клікаємо по координатах
        # time.sleep(1)
        # self.win.click_input(coords=(200, 300))

        print("вікно сховано")
        self.delay_lvl2()


    def click_to9point(self):
        singin = self.driver.find_element(By.CLASS_NAME, 'gb_B')
        singin.click()
        self.delay_lvl1()
        

    def click_ToWidgetEMAIL(self, driver, by, value, timeout=10):
        self.driver.switch_to.frame("app")
        self.delay_lvl1()
        # Чекаємо, поки елемент з'явиться в DOM
        el = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        # Скролимо до елемента
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        # Робимо клік через js (навіть якщо елемент частково прихований)
        driver.execute_script("arguments[0].click();", el)

        self.driver.switch_to.default_content()
        self.delay_lvl1()

    def click_signin(self):
        singin1 = self.driver.find_element(By.LINK_TEXT, "Зв’язані додатки й сервіси")
        singin1.click()
        self.delay_lvl1()

    def click_and_input_Email(self):
        email = self.driver.find_element(By.ID, 'identifierId')
        email.click()
        self.delay_lvl1()

        email.send_keys(os.getenv("EMAIL"))
        self.delay_lvl1()

        next_after_email = self.driver.find_element(By.ID, 'identifierNext')
        next_after_email.click()
        self.delay_lvl1()

    def click_and_input_Password(self):
        password = self.driver.find_element(By.NAME, 'Passwd')
        password.click()
        self.delay_lvl1()

        password.send_keys(os.getenv("PASSWORD"))
        self.delay_lvl1()

        next_after_password = self.driver.find_element(By.ID, 'passwordNext')
        next_after_password.click()
        self.delay_lvl1()
        x, y = pyautogui.position()
        print(f"Поточні координати миші: X={x}, Y={y}")
        pyautogui.click(x=6, y=506)

        pyautogui.moveTo(x, y)
 


    def openGoogleDocs(self):
        self.delay_lvl1()
        self.driver.get("https://docs.google.com/document/d/1jxQs9DNNV9gKY_9NvsixZlcqe_Sc-LZKlTwWkp8kYbI/edit?tab=t.0")
        self.delay_lvl1()


    def click_Button_Instruments(self):
        instruments = self.driver.find_element(By.ID, 'docs-tools-menu')
        instruments.click()
        self.delay_lvl1()


    def click_Button_VoiceWrite(self):
        voice_write = self.driver.find_element(By.ID, ":94")
        voice_write.click()
        self.delay_lvl1()


    def click_Start_VoiceWrite(self):
        self.voice_button_start = self.driver.find_element(By.XPATH, '//*[@id="docs-palette-dictation"]/div[1]/div[3]/div[1]')
        self.voice_button_start.click()

    def click_Stop_VoiceWrite(self):
        self.voice_button_stop = self.driver.find_element(By.CLASS_NAME, "docs-mic-control.docs-mic-control-recording")
        self.voice_button_stop.click()

    def isElement(self):
        aria_pressed = self.voice_button_start.get_attribute("aria-pressed")
        print("aria-pressed =", aria_pressed) 


    def on_off_buttonMicrophone(self):
        self.find_buttob_micro = self.driver.find_element(By.CLASS_NAME, "docs-palette.docs-mic-palette")
        self.status_micro = self.find_buttob_micro.is_displayed()
        print(self.status_micro)
        if self.status_micro:
            print("МІКРО У ДОКС ВИМКНЕНО")
        else:
            print("МІКРО У ДОКС ВКЛЮЧЕНО")


    def check_whether_ON_micro(self):
        if self.status_micro == True:
            self.click_Start_VoiceWrite()

    def check_whether_OFF_micro(self):
        if self.status_micro != True:
            self.click_Stop_VoiceWrite()

    

    def check_whether_need_micro(self):
        if self.work_with_text.start_write_text:
            self.on_off_buttonMicrophone()
            time.sleep(0.5)
            self.check_whether_ON_micro()
        else:
            self.on_off_buttonMicrophone()
            time.sleep(0.5)
            self.check_whether_OFF_micro()
                


    
    def stop_Selenium(self):
        self.driver.quit()

    def signInAccountGoogle(self):

        self.driver.get("https://google.com")
        self.delay_lvl2()

        self.click_to9point()
        self.click_ToWidgetEMAIL(self.driver, By.CLASS_NAME, "tX9u1b")
        self.click_signin()
        self.click_and_input_Email()
        self.click_and_input_Password()
    
    def work_withGoogleDocs(self):
        self.openGoogleDocs()
        self.click_Button_Instruments()
        self.click_Button_VoiceWrite()
        while True:
            self.check_whether_need_micro()
            time.sleep(0.5)



    def startWindow(self):
        self.getting_HWMD()
        self.move_WindowOutsideDisplay()
        self.signInAccountGoogle()
        self.work_withGoogleDocs()
        
        try:
            time.sleep(500)
        except OSError as e:
            print(f"Помилка з файлом: {e}")
            self.driver.quit()

if __name__ == "__main__":
    window_selenium = WindowSelenium()
    window_selenium.startWindow()

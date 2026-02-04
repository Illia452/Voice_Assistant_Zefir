import sys
from PyQt5.QtWidgets import (QMainWindow, QLabel, QLineEdit, QPushButton, 
                             QWidget, QGraphicsDropShadowEffect, QScrollArea, 
                             QVBoxLayout, QApplication, QFrame)
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPixmap, QIcon

class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.createMainWindow()
        self.createTitleStatus()
        self.createInputField_ForCommands()
        # Кнопку Send створимо після InputField, щоб прив'язати її положення
        self.createButtonSend() 
        self.createButtonStartStop()
        self.createIconZefir()
        self.createButtonUseMicrophone()
        
        # Створюємо вікна налаштувань та історії
        self.createSettingWindoww()
        self.createHistoryWindow()
        
        # Кнопки, що відкривають ці вікна
        self.createButtonSetting()
        self.createButtonHistory()

    def createMainWindow(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(960, 600)
        # Градієнт залишаємо, він гарний
        self.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, "
                           "stop:0 #F3E8FF, stop:1 #D8B4FE); font-family: 'Roboto';")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

    def createTitleStatus(self):
        self.textStatus = QLabel("Не активний", self.centralwidget)
        self.textStatus.setGeometry(QtCore.QRect(300, 30, 360, 41))
        self.textStatus.setAlignment(Qt.AlignCenter)
        self.textStatus.setStyleSheet("font-size: 24pt; color: #581c87; font-weight: bold; background: transparent;")

    def createInputField_ForCommands(self):
        self.InputField = QLineEdit(self.centralwidget)
        # Трохи розширив і центрував
        self.InputField.setGeometry(QtCore.QRect(230, 480, 500, 50))
        self.InputField.setPlaceholderText("Введіть команду вручну...")
        
        # Стиль поля вводу + відступ справа для кнопки send
        self.InputField.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border-radius: 25px;
                padding: 5px 50px 5px 20px; 
                font-size: 16px;
                color: #333;
                border: 2px solid transparent;
            }
            QLineEdit:focus {
                border: 2px solid #a855f7;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 5)
        self.InputField.setGraphicsEffect(shadow)

    def createButtonSend(self):
        self.button_send = QPushButton(self.centralwidget)
        # Розміщуємо кнопку ПОВЕРХ поля вводу справа
        self.button_send.setGeometry(QtCore.QRect(685, 485, 40, 40))
        self.button_send.setCursor(Qt.PointingHandCursor)
        self.button_send.setStyleSheet("""
            QPushButton {
                background-color: #c084fc;
                border-radius: 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #a855f7;
            }
            QPushButton:pressed {
                background-color: #7e22ce;
            }
        """)
        # Тут треба додати іконку, якщо є файл
        # icon = QIcon("../image/icon/send_regular_icon.svg")
        # self.button_send.setIcon(icon)
        self.button_send.setText("➤") # Тимчасовий символ
        self.button_send.clicked.connect(self.on_send_click)

    def on_send_click(self):
        text = self.InputField.text()
        if text:
            # Додаємо в історію як повідомлення користувача
            self.add_message_to_history(text, is_user=True)
            self.InputField.clear()
            
            # Імітація відповіді бота
            QtCore.QTimer.singleShot(1000, lambda: self.add_message_to_history("Я почув: " + text, is_user=False))

    def createButtonStartStop(self):
        self.button_startStop = QPushButton(self.centralwidget)
        self.button_startStop.setGeometry(QtCore.QRect(390, 310, 70, 70))
        self.button_startStop.setCursor(Qt.PointingHandCursor)
        self.button_startStop.setStyleSheet("""
            QPushButton {
                background-color: #c084fc;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #a855f7; transform: scale(1.1); }
        """)
        # Тінь
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.button_startStop.setGraphicsEffect(shadow)
        self.button_startStop.setText("⏯") # Тимчасово
        # Логіку кліку можна залишити твою

    def createButtonUseMicrophone(self):
        self.button_microphone = QPushButton(self.centralwidget)
        self.button_microphone.setGeometry(QtCore.QRect(500, 310, 70, 70))
        self.button_microphone.setCursor(Qt.PointingHandCursor)
        self.button_microphone.setStyleSheet("""
            QPushButton {
                background-color: #c084fc;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #a855f7; }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.button_microphone.setGraphicsEffect(shadow)
        self.button_microphone.setText("🎤") # Тимчасово

    def createIconZefir(self):
        self.image_iconZefir = QLabel(self.centralwidget)
        self.image_iconZefir.setGeometry(380, 100, 200, 200)
        # Завантаж свою картинку тут
        pixmap = QPixmap('../image/icon/zefir.png') 
        self.image_iconZefir.setPixmap(pixmap)

        self.image_iconZefir.setAlignment(Qt.AlignCenter)
        self.image_iconZefir.setStyleSheet("font-size: 100px; background: transparent;")
        
        # Ефект світіння
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(255, 255, 255, 150))
        self.image_iconZefir.setGraphicsEffect(shadow)

    # --- ЛОГІКА ІСТОРІЇ ---
    def createButtonHistory(self):
        self.button_history = QPushButton(self.centralwidget)
        self.button_history.setGeometry(QtCore.QRect(900, 20, 40, 40))
        self.button_history.setText("📜")
        self.button_history.clicked.connect(self.toggle_history)
        self.button_history.setStyleSheet("background: rgba(255,255,255,0.5); border-radius: 10px;")

    def createHistoryWindow(self):
        # Панель тепер є дочірнім елементом centralwidget
        self.history_window = QWidget(self.centralwidget)
        # Робимо її високою і притискаємо до правого краю (але з відступом)
        self.history_window.setGeometry(QtCore.QRect(680, 80, 260, 380))
        
        # GLASSMORPHISM STYLE
        self.history_window.setStyleSheet("""
            QWidget#HistoryPanel {
                background-color: rgba(255, 255, 255, 0.45);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
            QLabel { color: #4c1d95; background: transparent; }
        """)
        self.history_window.setObjectName("HistoryPanel")
        
        # Тінь для всієї панелі
        panel_shadow = QGraphicsDropShadowEffect()
        panel_shadow.setBlurRadius(30)
        panel_shadow.setColor(QColor(88, 28, 135, 40))
        self.history_window.setGraphicsEffect(panel_shadow)

        # Заголовок
        lbl = QLabel("Історія команд", self.history_window)
        lbl.setGeometry(0, 10, 260, 30)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 14pt; font-weight: bold;")

        # Scroll Area
        self.scroll_area = QScrollArea(self.history_window)
        self.scroll_area.setGeometry(10, 50, 240, 320)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")

        # Контейнер для повідомлень (використовуємо Layout!)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop) # Щоб повідомлення йшли зверху
        self.scroll_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.scroll_content)
        self.history_window.hide()

    def toggle_history(self):
        if self.history_window.isVisible():
            self.history_window.hide()
        else:
            self.history_window.show()
            self.history_window.raise_() # Підняти нагору

    def add_message_to_history(self, text, is_user=True):
        # Створюємо лейбл для повідомлення
        msg_lbl = QLabel(text)
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet(f"""
            background-color: {'rgba(255,255,255,0.7)' if is_user else 'rgba(192, 132, 252, 0.7)'};
            color: {'#333' if is_user else 'white'};
            padding: 8px;
            border-radius: 10px;
            font-size: 12px;
        """)
        # Додаємо у layout
        self.scroll_layout.addWidget(msg_lbl)
        
        # Автопрокрутка вниз
        QtCore.QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    # --- ЛОГІКА НАЛАШТУВАНЬ (Спрощена аналогічно історії) ---
    def createButtonSetting(self):
        self.button_setting = QPushButton(self.centralwidget)
        self.button_setting.setGeometry(QtCore.QRect(20, 20, 40, 40))
        self.button_setting.setText("⚙")
        self.button_setting.clicked.connect(self.toggle_settings)
        self.button_setting.setStyleSheet("background: rgba(255,255,255,0.5); border-radius: 10px;")

    def createSettingWindoww(self):
        self.setting_window = QWidget(self.centralwidget)
        self.setting_window.setGeometry(QtCore.QRect(20, 80, 240, 300))
        self.setting_window.setObjectName("SettingsPanel")
        self.setting_window.setStyleSheet("""
            QWidget#SettingsPanel {
                background-color: rgba(255, 255, 255, 0.45);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
        """)
        # Тінь
        panel_shadow = QGraphicsDropShadowEffect()
        panel_shadow.setBlurRadius(30)
        panel_shadow.setColor(QColor(88, 28, 135, 40))
        self.setting_window.setGraphicsEffect(panel_shadow)
        
        lbl = QLabel("Налаштування", self.setting_window)
        lbl.setGeometry(0, 10, 240, 30)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 14pt; font-weight: bold; color: #4c1d95; background: transparent;")
        
        # Чекбокс
        # ... тут твій код чекбокса ...
        self.setting_window.hide()

    def toggle_settings(self):
        if self.setting_window.isVisible():
            self.setting_window.hide()
        else:
            self.setting_window.show()
            self.setting_window.raise_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI_MainWindow()
    ui.show()
    sys.exit(app.exec_())
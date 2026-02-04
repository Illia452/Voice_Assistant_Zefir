import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QCheckBox, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, pyqtProperty, QPoint, QSize
from PyQt5.QtGui import QColor, QFont, QPixmap, QPainter, QIcon

# --- КЛАС КРАСИВОГО ПЕРЕМИКАЧА (TOGGLE) ---
class GlassToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Трохи зменшені розміри: ширина 40, висота 22
        self.setFixedSize(40, 22)
        self.setCursor(Qt.PointingHandCursor)
        
        # Початкова позиція кульки (тепер відступ 2 пікселі)
        self._circle_position = 2
        
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(450) # Лишаємо плавність
        self.animation.setEasingCurve(QEasingCurve.InOutQuint)

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        is_checked = self.isChecked()
        # Кольори: насичений фіолетовий для "ON", легке скло для "OFF"
        bg_color = QColor(147, 51, 234, 230) if is_checked else QColor(255, 255, 255, 80)
        
        p.setBrush(bg_color)
        p.setPen(Qt.NoPen)
        # Малюємо фон (капсулу)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 11, 11)
        
        # Малюємо кульку (зменшили до 18x18, щоб вона була акуратною)
        p.setBrush(QColor("white"))
        p.drawEllipse(int(self._circle_position), 2, 18, 18)

    def nextCheckState(self):
        super().nextCheckState()
        # Нові межі для анімації кульки:
        # 2 — початкова позиція (зліва)
        # 20 — кінцева позиція (40 ширина - 18 кулька - 2 відступ)
        start = self._circle_position
        end = 20 if self.isChecked() else 2
        
        self.animation.stop()
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()
# --- ОСНОВНИЙ КЛАС ІНТЕРФЕЙСУ ---
class UI_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.createMainWindow()
        self.createTitleStatus()
        self.createInputField_ForCommands()
        self.createButtonSend()
        self.createButtonStartStop()
        self.createIconZefir()
        self.createButtonUseMicrophone()
        
        # Створюємо панель налаштувань (з контентом)
        self.createSettingPanel()
        
        self.createButtonHistory()

    def createMainWindow(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(960, 600)
        # Градієнт фону
        self.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #F3E8FF, stop:1 #D8B4FE);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.setFocusPolicy(Qt.ClickFocus)

    def createTitleStatus(self):
        self.textStatus = QtWidgets.QLabel(self.centralwidget)
        self.textStatus.setGeometry(QtCore.QRect(300, 30, 351, 41))
        self.textStatus.setAlignment(Qt.AlignCenter)
        self.textStatus.setStyleSheet("font: 20pt \"Roboto\"; color: rgb(88, 28, 135); background-color: transparent;")
        self.textStatus.setText("Не активний")

    def createInputField_ForCommands(self):
        self.InputField = QtWidgets.QLineEdit(self.centralwidget)
        self.InputField.setGeometry(QtCore.QRect(230, 450, 500, 48))
        self.InputField.setPlaceholderText("Введіть команду вручну...")
        self.InputField.setFont(QFont("Roboto", 14))
        self.InputField.setStyleSheet("""
            QLineEdit {
                background-color: rgb(243, 244, 246);
                border-radius: 10px;
                padding: 5px 45px 5px 10px;
                font-size: 16px;
                border: 1px solid #e5e7eb;
            }
            QLineEdit:focus {
                border: 2px solid #a855f7;
                background-color: #faf5ff;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.InputField.setGraphicsEffect(shadow)

    def createButtonSend(self):
        self.button_send = QtWidgets.QPushButton(self.centralwidget)
        self.button_send.setGeometry(QtCore.QRect(690, 460, 30, 30))
        self.button_send.setCursor(Qt.ArrowCursor)
        self.button_send.setStyleSheet("""
            QPushButton { background-color: rgb(243, 244, 246); border-radius: 5px; }
            QPushButton:hover { background-color: #c0c1c3; }
        """)
        # Тут можна додати іконку, якщо є файл
        # self.button_send.setIcon(QIcon("../image/icon/send_regular_icon.svg"))

    def createButtonStartStop(self):
        self.button_startStop = QtWidgets.QPushButton(self.centralwidget)
        self.button_startStop.setGeometry(QtCore.QRect(390, 310, 64, 64))
        self.button_startStop.setStyleSheet("""
            QPushButton { background-color: #c084fc; border-radius: 5px; border: 1px solid #e1e6ef; }
            QPushButton:hover { background-color: #a855f7; }
        """)
        self.status_buttonStartStop = False
        self.button_startStop.clicked.connect(self.clickButton_StartStop)

    def clickButton_StartStop(self):
        if self.status_buttonStartStop:
            self.textStatus.setText("Не активний")
            self.status_buttonStartStop = False
        else:
            self.textStatus.setText("Активний")
            self.status_buttonStartStop = True

    def createIconZefir(self):
        self.image_iconZefir = QLabel(self.centralwidget)
        self.image_iconZefir.setGeometry(370, 80, 200, 200)
        # Шлях до картинки має бути вірним
        pixmap = QPixmap('../image/icon/zefir.png') 
        if pixmap.isNull():
             # Тимчасова заглушка, якщо картинки немає
             self.image_iconZefir.setText("ZEFIR")
             self.image_iconZefir.setStyleSheet("font-size: 30px; color: purple;")
        else:
            self.image_iconZefir.setPixmap(pixmap)
        
        self.image_iconZefir.setAlignment(Qt.AlignCenter)
        self.image_iconZefir.setScaledContents(True)

    def createButtonUseMicrophone(self):
        self.button_microphone = QtWidgets.QPushButton(self.centralwidget)
        self.button_microphone.setGeometry(QtCore.QRect(490, 310, 64, 64))
        self.button_microphone.setStyleSheet("""
            QPushButton { background-color: #c084fc; border-radius: 5px; border: 1px solid #e1e6ef; }
            QPushButton:hover { background-color: #a855f7; }
        """)

    # --- ПАНЕЛЬ НАЛАШТУВАНЬ ---
    def createSettingPanel(self):
        # 1. Головний контейнер (сама панель)
        self.settings_panel = QtWidgets.QWidget(self.centralwidget)
        self.settings_panel.setGeometry(20, 50, 40, 40)
        self.settings_panel.setObjectName("settings_panel")
        
        # Стиль для згорнутого стану
        self.glass_style_collapsed = """
            QWidget#settings_panel {
                background-color: rgba(255, 255, 255, 0.45);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
        """
        # Стиль для розгорнутого стану
        self.glass_style_expanded = """
            QWidget#settings_panel {
                background-color: rgba(255, 255, 255, 0.45);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
        """
        self.settings_panel.setStyleSheet(self.glass_style_collapsed)

        # Тінь для панелі
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15); shadow.setOffset(0, 4); shadow.setColor(QColor(0, 0, 0, 30))
        self.settings_panel.setGraphicsEffect(shadow)

        # 2. Іконка "Шестерня" (Завжди видима)
        self.settings_icon = QLabel(self.settings_panel)
        # Заглушка, якщо іконки немає
        # self.settings_icon.setPixmap(QPixmap("../image/icon/settings_regular_icon.svg")) 
        self.settings_icon.setText("⚙") 
        self.settings_icon.setStyleSheet("color: #581c87; font-size: 20px; background: transparent; border: none;")
        self.settings_icon.setGeometry(5, 5, 30, 30)
        self.settings_icon.setAlignment(Qt.AlignCenter)

        # Обробка кліку по панелі для відкриття
        self.settings_open = False
        self.settings_icon.mousePressEvent = self.toggleSettingsPanel # Клік по іконці
        # self.settings_panel.mousePressEvent = self.toggleSettingsPanel # Клік по всій панелі (можна вимкнути, якщо заважає)

        # --- ВНУТРІШНІЙ КОНТЕЙНЕР ДЛЯ ЕЛЕМЕНТІВ ---
        # Ми поміщаємо все сюди, щоб легко ховати/показувати разом
        self.settings_content = QWidget(self.settings_panel)
        self.settings_content.setGeometry(0, 0, 220, 375)
        self.settings_content.setStyleSheet("background: transparent; border: none;")
        self.settings_content.hide() # Сховано за замовчуванням

        # 3. Стрілочка "Повне вікно" (Верхній ПРАВИЙ кут)
        self.btn_full_settings = QPushButton("↗", self.settings_content)
        self.btn_full_settings.setGeometry(180, 10, 30, 30)
        self.btn_full_settings.setCursor(Qt.PointingHandCursor)
        self.btn_full_settings.setStyleSheet("""
            QPushButton { color: #581c87; font-weight: bold; font-size: 16px; background: transparent; }
            QPushButton:hover { background: rgba(255,255,255,0.3); border-radius: 15px; }
        """)
        self.btn_full_settings.clicked.connect(lambda: print("Open Full Settings"))

        # 4. Швидкі налаштування (Рядки з текстом і тумблерами)
        self.createQuickSettingRow("Темна тема", 60)
        self.createQuickSettingRow("Автозапуск", 110)
        self.createQuickSettingRow("Голос", 160)

        # 5. Кнопка "More..." (Внизу)
        self.btn_more = QPushButton("More ...", self.settings_content)
        self.btn_more.setGeometry(20, 320, 100, 30)
        self.btn_more.setStyleSheet("""
            QPushButton {
                color: #b91c1c; /* Червоний, як на твоєму малюнку */
                font: bold 14pt 'Comis Sans MS'; /* Шрифт "від руки" або схожий */
                background: transparent;
                text-align: left;
            }
            QPushButton:hover { color: #dc2626; }
        """)

    def createQuickSettingRow(self, text, y_pos):
        """ Допоміжна функція для створення рядка налаштувань """
        # Текст
        lbl = QLabel(text, self.settings_content)
        lbl.setGeometry(20, y_pos + 3, 120, 20)
        lbl.setStyleSheet("color: #581c87; font-size: 11pt; font-weight: bold;")
        
        # Тумблер (GlassToggle)
        toggle = GlassToggle(self.settings_content)
        toggle.move(150, y_pos) # Позиція X=150 (справа)

    def toggleSettingsPanel(self, event=None):
        anim = QPropertyAnimation(self.settings_panel, b"geometry")
        anim.setDuration(400) # Трохи повільніше для плавності
        anim.setEasingCurve(QEasingCurve.OutBack)

        if not self.settings_open:
            # --- ВІДКРИВАЄМО ---
            anim.setStartValue(QRect(20, 50, 40, 40))
            anim.setEndValue(QRect(20, 50, 220, 375))
            
            self.settings_panel.setStyleSheet(self.glass_style_expanded)
            
            # Показуємо контент ПІСЛЯ початку анімації або одразу
            self.settings_content.show()
            self.settings_open = True
        else:
            # --- ЗАКРИВАЄМО ---
            anim.setStartValue(QRect(20, 50, 220, 375))
            anim.setEndValue(QRect(20, 50, 40, 40))
            
            self.settings_panel.setStyleSheet(self.glass_style_collapsed)
            
            # Ховаємо контент
            self.settings_content.hide()
            self.settings_open = False

        anim.start()
        self.settings_panel.anim = anim

    def createButtonHistory(self):
        self.button_history = QtWidgets.QPushButton(self.centralwidget)
        self.button_history.setGeometry(QtCore.QRect(905, 30, 35, 40))
        self.button_history.setStyleSheet("""
            QPushButton { background-color: rgb(209, 213, 219); border-radius: 5px; border: 1px solid #d1d5db; }
            QPushButton:hover { background-color: #9ca3af; }
        """)
        # Іконка історії
        # self.button_history.setIcon(QIcon("../image/icon/history_regular_icon.svg"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_MainWindow()
    ui.show()
    sys.exit(app.exec_())
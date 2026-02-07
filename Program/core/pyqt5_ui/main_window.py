from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QButtonGroup
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, pyqtProperty, QPoint, QSize
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QCheckBox
from PyQt5.QtGui import QColor, QFont, QPixmap, QPainter, QIcon
import json
import os


class ModernRadioButton(QtWidgets.QRadioButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QRadioButton {
                font-size: 14px; color: #4b5563; padding: 5px;
            }
            QRadioButton::indicator {
                width: 18px; height: 18px;
                border-radius: 11px;
                border: 2px solid #9ca3af; /* Сірий обідок коли вимкнено */
                background: transparent;
            }
            QRadioButton::indicator:checked {
                border: 1px solid #8b5cf6; /* Товстий фіолетовий обідок створює ефект крапки всередині */
                border-radius: 10px;
                background: #8b5cf6;
            }
            QRadioButton:hover { color: #6d28d9; }
        """)

class GlassToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Трохи зменшені розміри: ширина 40, висота 22
        self.setFixedSize(40, 22)
        self.setCursor(Qt.PointingHandCursor)
        
        # Початкова позиція кульки (тепер відступ 2 пікселі)
        self._circle_position = 2
        
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(350) # Лишаємо плавність
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
        bg_color = QColor(147, 51, 234, 230) if is_checked else QColor("#EDE9FE")
        
        p.setBrush(bg_color)
        p.setPen(Qt.NoPen)
        # Малюємо фон (капсулу)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 11, 11)
        
        # Малюємо кульку (зменшили до 18x18, щоб вона була акуратною)
        p.setBrush(QColor("white"))
        p.drawEllipse(int(self._circle_position), 2, 18, 18)
    
    def hitButton(self, pos: QPoint):
        # Повертаємо True, якщо клік потрапив у будь-яку точку віджета
        return self.rect().contains(pos)

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

class UI_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        with open('pyqt5_ui/settings_ui.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.setupUI()




    def setupUI(self):
        self.load_settings_data()
        self.createMainWindow()
        self.createTitleStatus()
        self.createInputField_ForCommands()
        self.createButtonSend()
        self.createButtonStartStop()
        self.createIconZefir()
        self.createButtonUseMicrophone()
        self.createSettingPanel()
        self.createHistoryPanel()
        self.full_setting_content()



    def createMainWindow(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(960,600)
        self.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, \n"
                                      "                                stop:0 #F3E8FF, stop:1 #D8B4FE);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.setFocusPolicy(Qt.ClickFocus)

    def close_set(self):
        # 1. Анімація зникнення (Fade Out)
        self.anim_opacity_close = QPropertyAnimation(self.fade_effect, b"opacity")
        self.anim_opacity_close.setDuration(400)
        self.anim_opacity_close.setStartValue(1.0)
        self.anim_opacity_close.setEndValue(0.0)
        self.anim_opacity_close.setEasingCurve(QEasingCurve.InQuad)

        # 2. Анімація опускання вниз
        self.anim_pos_close = QPropertyAnimation(self.main_container, b"geometry")
        self.anim_pos_close.setDuration(400)
        self.anim_pos_close.setStartValue(QRect(0, 0, 960, 600))
        self.anim_pos_close.setEndValue(QRect(0, 30, 960, 600))
        
        # 3. Коли анімація закінчиться — реально сховати віджет (hide)
        self.anim_opacity_close.finished.connect(self.main_container.hide)

        self.anim_opacity_close.start()
        self.anim_pos_close.start()

    def full_setting_content(self):
        # Головний контейнер
        self.main_container = QtWidgets.QWidget(self.centralwidget)
        self.main_container.setGeometry(0, 0, 960, 600)
        self.main_container.setStyleSheet("background: #EDE9FE;") 
        
        # 1. Створюємо ефект прозорості
        self.fade_effect = QGraphicsOpacityEffect(self.main_container)
        self.main_container.setGraphicsEffect(self.fade_effect)
        
        # 2. Ховаємо контейнер і ставимо прозорість на 0
        self.fade_effect.setOpacity(0)
        self.main_container.hide()

        self.main_container.raise_()

        # --- ОСНОВНИЙ ЛЕЙАУТ ВІКНА ---
        self.layout_full = QtWidgets.QVBoxLayout(self.main_container)
        self.layout_full.setContentsMargins(0, 0, 0, 0)
        self.layout_full.setSpacing(0)

        # 1. ШАПКА (HEADER)
        self.header_frame = QtWidgets.QFrame(self.main_container)
        self.header_frame.setFixedHeight(80)
        self.header_frame.setStyleSheet("background: transparent;")
        
        header_layout = QtWidgets.QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(30, 0, 30, 0)

        # Кнопка Назад
        self.btn_back_full = QtWidgets.QPushButton("  Назад")
        self.btn_back_full.setCursor(Qt.PointingHandCursor)
        self.btn_back_full.setMinimumSize(100, 40)
        self.btn_back_full.clicked.connect(self.close_set) # Твоя функція закриття
        self.btn_back_full.setIcon(QtGui.QIcon("../image/icon/arrow_left.svg")) 
        self.btn_back_full.setStyleSheet("""
            QPushButton {
                background-color: white; border-radius: 12px; color: #581c87;
                font-size: 15px; font-weight: bold; border: 1px solid rgba(139, 92, 246, 0.2);
            }
            QPushButton:hover { background-color: #F5F3FF; border: 1px solid #8b5cf6; }
        """)

        # Заголовок
        self.label_title_full = QtWidgets.QLabel("Налаштування")
        self.label_title_full.setStyleSheet("font-size: 26px; font-weight: bold; color: #581c87;")

        header_layout.addWidget(self.btn_back_full)
        header_layout.addStretch()
        header_layout.addWidget(self.label_title_full)
        header_layout.addStretch()
        header_layout.addSpacing(100) 

        self.layout_full.addWidget(self.header_frame)

        # --- НИЖНЯ ЧАСТИНА ---
        self.body_container = QtWidgets.QWidget(self.main_container)
        body_layout = QtWidgets.QHBoxLayout(self.body_container)
        body_layout.setContentsMargins(20, 0, 25, 25)
        body_layout.setSpacing(20)

        # 2. БОКОВА ПАНЕЛЬ (МЕНЮ)
        self.sidebar = QtWidgets.QFrame(self.body_container)
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
        """)
        
        sidebar_inner_layout = QtWidgets.QVBoxLayout(self.sidebar)
        sidebar_inner_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_inner_layout.setSpacing(10)

        # Стиль кнопок
        menu_button_style = """
            QPushButton {
                text-align: left; padding-left: 15px; height: 45px;
                border: none; border-radius: 12px;
                color: #6B7280; font-size: 14px; font-weight: 500;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.4); color: #581c87; }
            QPushButton:checked { background-color: white; color: #a855f7; font-weight: bold; }
        """

        # Створення кнопок меню
        self.btn_menu_general = QtWidgets.QPushButton("⚡ Загальні")
        self.btn_menu_voice = QtWidgets.QPushButton("🎙️ Голос")
        self.btn_menu_commands = QtWidgets.QPushButton("⌨️ Команди") # Новий розділ
        self.btn_menu_interface = QtWidgets.QPushButton("🎨 Інтерфейс")
        self.btn_menu_about = QtWidgets.QPushButton("ℹ️ Про систему")

        # Список кнопок для зручного керування
        self.menu_buttons = [
            self.btn_menu_general, 
            self.btn_menu_voice, 
            self.btn_menu_commands,
            self.btn_menu_interface, 
            self.btn_menu_about
        ]

        for btn in self.menu_buttons:
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(menu_button_style)
            sidebar_inner_layout.addWidget(btn)

        sidebar_inner_layout.addStretch()

        # 3. ОБЛАСТЬ КОНТЕНТУ (STACKED WIDGET)
        self.content_stack = QtWidgets.QStackedWidget(self.body_container)
        self.content_stack.setStyleSheet("""
            QStackedWidget {
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
        """)

        # --- СТВОРЕННЯ СТОРІНОК ---
        
        # Стор. 0: Загальні (Вже готова)
        self.page_general = QtWidgets.QWidget()
        self.setup_general_page() # Я виніс наповнення в окремий метод, щоб тут було чисто
        self.content_stack.addWidget(self.page_general)

        # Стор. 1: Голос (Пуста заготовка)
        self.page_voice = QtWidgets.QWidget()
        self.setup_placeholder_page(self.page_voice, "Налаштування Голосу та Мікрофону")
        self.content_stack.addWidget(self.page_voice)

        # Стор. 2: Команди (Пуста заготовка)
        self.page_commands = QtWidgets.QWidget()
        self.setup_commands_page()
        self.content_stack.addWidget(self.page_commands)

        # Стор. 3: Інтерфейс (Пуста заготовка)
        self.page_interface = QtWidgets.QWidget()
        self.setup_placeholder_page(self.page_interface, "Налаштування Зовнішнього Вигляду")
        self.content_stack.addWidget(self.page_interface)

        # Стор. 4: Про систему (Пуста заготовка)
        self.page_about = QtWidgets.QWidget()
        self.setup_placeholder_page(self.page_about, "Інформація про Асистента")
        self.content_stack.addWidget(self.page_about)


        # --- ЛОГІКА ПЕРЕМИКАННЯ ---
        # Використовуємо lambda, щоб передати індекс сторінки
        self.btn_menu_general.clicked.connect(lambda: self.switch_settings_tab(0, self.btn_menu_general))
        self.btn_menu_voice.clicked.connect(lambda: self.switch_settings_tab(1, self.btn_menu_voice))
        self.btn_menu_commands.clicked.connect(lambda: self.switch_settings_tab(2, self.btn_menu_commands))
        self.btn_menu_interface.clicked.connect(lambda: self.switch_settings_tab(3, self.btn_menu_interface))
        self.btn_menu_about.clicked.connect(lambda: self.switch_settings_tab(4, self.btn_menu_about))

        # Активуємо першу вкладку на старті
        self.switch_settings_tab(0, self.btn_menu_general)

        # Фінальна збірка
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.content_stack)
        self.layout_full.addWidget(self.body_container)


    def createGlassCard(self):
        """ Створює стилізовану білу напівпрозору картку """
        card = QtWidgets.QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.6);
                border-radius: 15px;
                border: 1px solid white;
            }
        """)
        return card


    def switch_settings_tab(self, index, active_btn):
        """ Перемикає сторінку в StackedWidget і підсвічує активну кнопку """
        self.content_stack.setCurrentIndex(index)
        
        # Знімаємо виділення з усіх кнопок
        for btn in self.menu_buttons:
            btn.setChecked(False)
        
        # Виділяємо натиснуту
        active_btn.setChecked(True)

    def setup_general_page(self):
        """ Наповнення сторінки 'Загальні' """
        layout = QtWidgets.QVBoxLayout(self.page_general)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop) # Щоб елементи не розтягувались по вертикалі

        # Картка 1 (Приклад)
        card = QtWidgets.QFrame()
        card.setMinimumHeight(80)
        card.setStyleSheet("background: rgba(255,255,255,0.6); border-radius: 15px; border: 1px solid white;")
        
        row = QtWidgets.QHBoxLayout(card)
        row.setContentsMargins(20, 0, 20, 0)
        
        text_layout = QtWidgets.QVBoxLayout()
        lbl_title = QtWidgets.QLabel("Запускати разом з Windows")
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #4B5563; border: none;")
        lbl_desc = QtWidgets.QLabel("Автоматичний старт при вході")
        lbl_desc.setStyleSheet("font-size: 12px; color: #9CA3AF; border: none;")
        text_layout.addWidget(lbl_title)
        text_layout.addWidget(lbl_desc)
        
        row.addLayout(text_layout)
        row.addStretch()
        row.addWidget(GlassToggle(card)) # тумблер

        layout.addWidget(card)
        # Тут можна додати інші картки для цієї сторінки...

    def setup_placeholder_page(self, page_widget, text):
        """ Тимчасовий метод для пустих сторінок, щоб ти бачив, що вони працюють """
        layout = QtWidgets.QVBoxLayout(page_widget)
        lbl = QtWidgets.QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 20px; color: #581c87; font-weight: bold;")
        layout.addWidget(lbl)

    def choose_folder_dialog(self):
        """ Відкриває провідник для вибору папки """
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Оберіть папку для скріншотів")
        if folder:
            # Оновлюємо текст у лейблі
            self.lbl_current_path.setText(folder)
            # Зберігаємо у JSON за вкладеним шляхом
            self.save_setting(["screenshot", "path"], folder)
            print(f"Новий шлях збережено: {folder}")

    # --- НОВА ЛОГІКА РОБОТИ З НАЛАШТУВАННЯМИ ---

    def load_settings_data(self):
        # Шлях до файлу (переконайся, що папка pyqt5_ui існує!)
        self.settings_file = "pyqt5_ui/settings_ui.json"
        
        # 1. Базова структура за замовчуванням (обов'язково вкладена)
        default_path = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        self.settings_data = {
            "screenshot": {
                "format": "PNG",
                "path": default_path
            }
        }

        # 2. Спроба зчитати файл
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content: # Перевірка чи файл не порожній
                        loaded_data = json.loads(content)
                        # Розумне оновлення: зливаємо screenshot дані
                        if "screenshot" in loaded_data:
                            self.settings_data["screenshot"].update(loaded_data["screenshot"])
            except Exception as e:
                print(f"Помилка читання JSON: {e}")


    def save_setting(self, keys, value):
        """
        keys: список ключів, наприклад ["screenshot", "format"]
        value: значення, яке зберігаємо
        """
        # Якщо передали один ключ як рядок, перетворюємо в список для універсальності
        if isinstance(keys, str):
            keys = [keys]

        # Проходимо по структурі словника до передостаннього ключа
        target = self.settings_data
        for key in keys[:-1]:
            if key not in target:
                target[key] = {} # Створюємо категорію, якщо її немає
            target = target[key]

        # Встановлюємо значення останньому ключу
        target[keys[-1]] = value

        # Записуємо оновлений словник у файл
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings_data, f, indent=4, ensure_ascii=False)
            print(f"Збережено в JSON: {keys} -> {value}")
        except Exception as e:
            print(f"Помилка запису файлу: {e}")

    def setup_commands_page(self):
        # Очистка лейауту (стандартна процедура для рефрешу сторінки)
        if self.page_commands.layout():
             QtWidgets.QWidget().setLayout(self.page_commands.layout())

        layout = QtWidgets.QVBoxLayout(self.page_commands)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        # --- КАРТКА 1: ФОРМАТ ---
        card_format = self.createGlassCard()
        card_fmt_layout = QtWidgets.QVBoxLayout(card_format)
        card_fmt_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_fmt = QtWidgets.QLabel("Формат збереження")
        lbl_fmt.setStyleSheet("font-size: 16px; font-weight: bold; color: #581c87;")
        card_fmt_layout.addWidget(lbl_fmt)

        # Створюємо кнопки
        self.radio_png = ModernRadioButton("PNG")
        self.radio_jpg = ModernRadioButton("JPG")
        self.radio_ask = ModernRadioButton("Запитувати щоразу")

        # Група кнопок (допомагає керувати ними як єдиним цілим)
        self.format_group = QtWidgets.QButtonGroup(self)
        self.format_group.addButton(self.radio_png, 1)
        self.format_group.addButton(self.radio_jpg, 2)
        self.format_group.addButton(self.radio_ask, 3)

        # ВІДНОВЛЕННЯ СТАНУ З JSON
        screenshot_cfg = self.settings_data.get("screenshot", {})
        
        # Формат
        current_fmt = screenshot_cfg.get("format", "PNG")
        if current_fmt == "PNG": self.radio_png.setChecked(True)
        elif current_fmt == "JPG": self.radio_jpg.setChecked(True)
        else: self.radio_ask.setChecked(True)

        # Шлях (якщо в JSON чомусь порожньо — беремо дефолт)
        default_p = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        saved_path = screenshot_cfg.get("path", default_p)

        # Встановлюємо текст у лейбл


        # ПІДКЛЮЧЕННЯ ЗБЕРЕЖЕННЯ
        # Використовуємо lambda, щоб передати конкретне значення
        self.radio_png.clicked.connect(lambda: self.save_setting(["screenshot", "format"], "PNG"))
        self.radio_jpg.clicked.connect(lambda: self.save_setting(["screenshot", "format"], "JPG"))
        self.radio_ask.clicked.connect(lambda: self.save_setting(["screenshot", "format"], "ASK"))

        layout_opts = QtWidgets.QVBoxLayout()
        layout_opts.addWidget(self.radio_png)
        layout_opts.addWidget(self.radio_jpg)
        layout_opts.addWidget(self.radio_ask)
        card_fmt_layout.addLayout(layout_opts)
        layout.addWidget(card_format)

        # --- КАРТКА 2: ШЛЯХ ---
# --- КАРТКА 2: ШЛЯХ ---
        card_path = self.createGlassCard()
        card_path_layout = QtWidgets.QVBoxLayout(card_path)
        card_path_layout.setContentsMargins(20, 20, 20, 20)

        lbl_path_t = QtWidgets.QLabel("Папка для скріншотів")
        lbl_path_t.setStyleSheet("font-size: 16px; font-weight: bold; color: #581c87; margin-bottom: 5px;")
        card_path_layout.addWidget(lbl_path_t)
        
        # Горизонтальний контейнер для елементів шляху
        row_path = QtWidgets.QHBoxLayout()
        row_path.setSpacing(12) # Відступ між іконкою, текстом і кнопкою

        # 1. Іконка папки
        icon_label = QtWidgets.QLabel("📂")
        icon_label.setStyleSheet("font-size: 18px;")
        
        # 2. Лейбл шляху (головний елемент)
        screenshot_cfg = self.settings_data.get("screenshot", {})
        saved_path = screenshot_cfg.get("path", "Оберіть шлях...")
        
        self.lbl_current_path = QtWidgets.QLabel(saved_path)
        # Вмикаємо ElideMode (три крапки), якщо текст не влазить
        self.lbl_current_path.setMinimumWidth(100) # Мінімальна ширина щоб не зник зовсім
        self.lbl_current_path.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.5); 
                border-radius: 8px; 
                padding: 8px 12px; 
                color: #4b5563; 
                font-family: 'Segoe UI', consolas;
                font-size: 13px;
                border: 1px solid rgba(0,0,0,0.05);
            }
        """)
        
        # 3. Кнопка зміни
        btn_change = QtWidgets.QPushButton("Змінити")
        btn_change.setCursor(Qt.PointingHandCursor)
        btn_change.setFixedWidth(100) # Фіксуємо кнопку, щоб вона не стрибала
        btn_change.setFixedHeight(34)
        btn_change.setStyleSheet("""
            QPushButton { 
                background-color: #8b5cf6; 
                color: white; 
                border-radius: 8px; 
                font-weight: bold; 
                border: none; 
            }
            QPushButton:hover { background-color: #7c3aed; }
            QPushButton:pressed { background-color: #6d28d9; }
        """)
        btn_change.clicked.connect(self.choose_folder_dialog)

        # Додаємо все в рядок
        row_path.addWidget(icon_label)
        row_path.addWidget(self.lbl_current_path, 1) # '1' каже лейблу розтягуватися максимально
        row_path.addWidget(btn_change)
        
        card_path_layout.addLayout(row_path)
        layout.addWidget(card_path)
        
        layout.addStretch()



    def createTitleStatus(self):
        self.textStatus = QtWidgets.QLabel(self.centralwidget)
        self.textStatus.setGeometry(QtCore.QRect(300, 30, 351, 41))
        self.textStatus.setAlignment(Qt.AlignCenter)
        self.textStatus.setStyleSheet("font: 20pt \"Roboto\";\n"
                                    "color: rgb(88, 28, 135);\n"
                                    "background-color: transparent;")
        self.textStatus.setObjectName("label")


    def createInputField_ForCommands(self):
        self.InputField = QtWidgets.QLineEdit(self.centralwidget)
        self.InputField.setGeometry(QtCore.QRect(230, 450, 500, 48))
        self.InputField.setPlaceholderText("Введіть команду вручну...")
        self.InputField.setFocusPolicy(Qt.ClickFocus)
        self.InputField.setFont(QFont("Roboto", 14))  # Шрифт
        
        self.InputField.setStyleSheet("""
            QLineEdit {
                background-color: rgb(243, 244, 246);
                border-radius: 10px;
                padding: 5px 45px 5px 10px;
                font-size: 16px;
                border: 1px solid #e5e7eb;                         
            }
            QLineEdit:focus {
                border: 2px solid #a855f7;  /* Бордер з'являється при фокусі */
                background-color: #faf5ff;  /* Легка зміна кольору */
            }
        """)
        
        
        self.InputField.setText("")
        self.InputField.setObjectName("lineEdit")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)  # Розмиття
        shadow.setOffset(0, 4)  # Зміщення тіні (по X та Y)
        shadow.setColor(QColor(0, 0, 0, 30))  # Колір тіні (чорний з прозорістю)
        self.InputField.setGraphicsEffect(shadow)

    def createButtonSend(self):
        self.button_send = QtWidgets.QPushButton(self.centralwidget)
        self.button_send.setGeometry(QtCore.QRect(690, 460, 30, 30))
        self.button_send.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.button_send.setStyleSheet("""
			QPushButton {
				background-color: rgb(243, 244, 246);
                border-radius: 5px;
        	}
            QPushButton:hover {
                background-color: #c0c1c3;  
                                
            }                    
		""")
        self.button_send.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/send_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_send.setIcon(icon)
        self.button_send.setObjectName("button_send")
        self.saved_text = ""


    def createButtonStartStop(self):
        self.button_startStop = QtWidgets.QPushButton(self.centralwidget)
        self.button_startStop.setGeometry(QtCore.QRect(390, 310, 64, 64))
        self.button_startStop.setStyleSheet("""
			QPushButton {
				background-color: #c084fc;
				border-radius: 5px;
				border: 1px solid #e1e6ef;
			}
			QPushButton:hover {
                background-color: #a855f7;
									
			}
	    """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)  # Розмиття
        shadow.setOffset(0, 4)  # Зміщення тіні (по X та Y)
        shadow.setColor(QColor(0, 0, 0, 30))  # Колір тіні (чорний з прозорістю)
        self.button_startStop.setGraphicsEffect(shadow)
        
        self.button_startStop.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/play_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_startStop.setIcon(icon)
        self.button_startStop.setIconSize(QtCore.QSize(20, 20))
        self.button_startStop.setObjectName("button_startStop")
        self.button_startStop.clicked.connect(self.clickButton_StartStop)
        self.status_buttonStartStop = False
        self.clickButton_StartStop()


    def clickButton_StartStop(self):
        if self.status_buttonStartStop:
            self.switchON_ButtonStartStop()
            self.status_buttonStartStop = False

        else:
            self.switchOFF_ButtonStartStop()
            self.status_buttonStartStop = True

    def switchON_ButtonStartStop(self):
        self.textStatus.setText("Активний")
        self.button_startStop.setStyleSheet("""
        QPushButton {
            background-color: rgba(140, 210, 205, 0.65);
            border-radius: 5px;
            border: 1px solid #e1e6ef;
        }
        QPushButton:hover {
            background-color: rgba(124, 196, 192, 0.65);
        }
        """)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/pause_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_startStop.setIcon(icon)
        self.button_startStop.setIconSize(QtCore.QSize(20, 20))

    def switchOFF_ButtonStartStop(self):
        self.textStatus.setText("Не активний")
        self.button_startStop.setStyleSheet("""
        QPushButton {
            background-color: #c084fc;
            border-radius: 5px;
            border: 1px solid #e1e6ef;
        }
        QPushButton:hover {
            background-color: #a855f7;
                                
        }
        """)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/play_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off) 
        self.button_startStop.setIcon(icon)
        self.button_startStop.setIconSize(QtCore.QSize(20, 20))


    def createIconZefir(self):
        self.image_iconZefir = QLabel(self.centralwidget)  # Створюємо новий QLabel
        self.image_iconZefir.setGeometry(370, 80, 200, 200)  # Встановлюємо розмір та позицію
        pixmap = QPixmap('../image/icon/zefir.png')  # Завантажуємо зображення
        self.image_iconZefir.setPixmap(pixmap)  # Встановлюємо зображення в QLabel
        self.image_iconZefir.setAlignment(Qt.AlignCenter)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)  # Розмиття
        shadow.setOffset(0, 4)  # Зміщення тіні (по X та Y)
        shadow.setColor(QColor(0, 0, 0, 100))  # Колір тіні (чорний з прозорістю)
        self.image_iconZefir.setGraphicsEffect(shadow)

        self.image_iconZefir.setScaledContents(True)
        self.image_iconZefir.setStyleSheet("""
			QLabel {
				background-color: transparent;
			}
        """)


    def createButtonUseMicrophone(self):
        self.button_microphone = QtWidgets.QPushButton(self.centralwidget)
        self.button_microphone.setGeometry(QtCore.QRect(490, 310, 64, 64))
        self.button_microphone.setStyleSheet("""
			QPushButton {
				background-color: #c084fc;
				border-radius: 5px;
				border: 1px solid #e1e6ef;
			}
			QPushButton:hover {
                background-color: #a855f7;
									
			}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)  # Розмиття
        shadow.setOffset(0, 4)  # Зміщення тіні (по X та Y)
        shadow.setColor(QColor(0, 0, 0, 30))  # Колір тіні (чорний з прозорістю)
        self.button_microphone.setGraphicsEffect(shadow)
        self.button_microphone.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/mic_on_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_microphone.setIcon(icon)
        self.button_microphone.setIconSize(QtCore.QSize(22, 22))
        self.button_microphone.setObjectName("button_microphone")
        self.button_microphone.clicked.connect(self.clickButton_Microphone)
        self.status_buttonMicrophone = False
        self.clickButton_Microphone()

    def clickButton_Microphone(self):
        if self.status_buttonMicrophone:
            self.switchON_ButtonMicrophone()
            self.status_buttonMicrophone = False

        else:
            self.switchOFF_ButtonMicrophone()
            self.status_buttonMicrophone = True


    def switchON_ButtonMicrophone(self):
            self.button_microphone.setStyleSheet("""
			QPushButton {
				background-color: #c084fc;
				border-radius: 5px;
				border: 1px solid #e1e6ef;
			}
			QPushButton:hover {
                background-color: #a855f7;
									
			}
	        """)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("../image/icon/mic_on_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button_microphone.setIcon(icon)
            self.button_microphone.setIconSize(QtCore.QSize(22, 22))


    def switchOFF_ButtonMicrophone(self):
        self.button_microphone.setStyleSheet("""
        QPushButton {
            background-color: rgba(230, 160, 160, 0.9);
            border-radius: 5px;
            border: 1px solid #e1e6ef;
        }
        QPushButton:hover {
            background-color: rgba(223, 146, 146, 0.9);
        }
        """)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/mic_off_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_microphone.setIcon(icon)
        self.button_microphone.setIconSize(QtCore.QSize(22, 22))


    def createSettingPanel(self):
        self.settings_panel = QtWidgets.QWidget(self.centralwidget)
        self.settings_panel.setGeometry(20, 50, 40, 40)
        self.settings_panel.setObjectName("settings_panel")

        self.design_setting_panel = self.settings_panel.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.45);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
            QLabel {
                background: transparent;
                border: none;
            }                                                          
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.settings_panel.setGraphicsEffect(shadow)

        self.settings_icon = QLabel(self.settings_panel)
        self.settings_icon.setPixmap(QPixmap("../image/icon/settings_regular_icon.svg"))
        self.settings_icon.setGeometry(0, 0, 40, 40)
        self.settings_icon.setAlignment(Qt.AlignCenter)

        self.create_SettingContent()

        self.settings_open = False

        self.settings_icon.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.settings_icon.mousePressEvent = self.toggleSettingsPanel

    def create_SettingContent(self):
        self.settings_content = QtWidgets.QWidget(self.settings_panel)
        self.settings_content.setGeometry(0, 0, 220, 375)
        self.settings_content.setStyleSheet("background: transparent; border: none;")
        self.settings_content.hide()

        self.icon_sett = QtWidgets.QPushButton(self.settings_content)
        self.icon_sett.setGeometry(0, 0, 40, 40)
        self.icon_sett.setStyleSheet("background: transparent; border: 5px;")
        self.icon_sett.setCursor(Qt.PointingHandCursor)
        self.icon_sett.mousePressEvent = self.toggleSettingsPanel

        self.btn_full_settings = QtWidgets.QLabel(self.settings_content)
        self.btn_full_settings.setPixmap(QPixmap("../image/icon/arrow_right_regular_icon.svg"))
        self.btn_full_settings.setGeometry(185, 0, 40, 40)
        self.btn_full_settings.setCursor(Qt.PointingHandCursor)
        self.btn_full_settings.setStyleSheet("""
            QPushButton { color: #581c87; font-weight: bold; font-size: 16px; background: transparent; }
            QPushButton:hover { background: rgba(255,255,255,0.3); border-radius: 15px; }
        """)
        self.btn_full_settings.mousePressEvent = self.full_setting_panel

        self.createQuickSettingRow("Темна тема", 60)
        self.createQuickSettingRow("Автозапуск", 110)
        self.createQuickSettingRow("Голос", 160)

        self.settings_full = False

    def createQuickSettingRow(self, text, y_pos):
        """ Допоміжна функція для створення рядка налаштувань """
        # Текст
        lbl = QLabel(text, self.settings_content)
        lbl.setGeometry(20, y_pos, 120, 20)
        lbl.setStyleSheet("color: #581c87; font-size: 11pt;")
        
        # Тумблер (GlassToggle)
        toggle = GlassToggle(self.settings_content)
        toggle.move(150, y_pos) # Позиція X=150 (справа)



    def full_setting_panel(self, event=None):
        # 1. Закриваємо маленьке швидке меню, якщо воно відкрите
        if self.settings_open:
            self.toggleSettingsPanel()

        # 2. Показуємо великий контейнер і піднімаємо його наверх
        self.main_container.show()
        self.main_container.raise_()

        # 3. Анімація прозорості (Fade In)
        self.anim_opacity = QPropertyAnimation(self.fade_effect, b"opacity")
        self.anim_opacity.setDuration(500)
        self.anim_opacity.setStartValue(0.0)
        self.anim_opacity.setEndValue(1.0)
        self.anim_opacity.setEasingCurve(QEasingCurve.OutQuad)

        # 4. Анімація руху знизу вгору (Slide Up)
        # Вікно стартує трохи нижче (y=30) і піднімається в 0
        self.anim_pos = QPropertyAnimation(self.main_container, b"geometry")
        self.anim_pos.setDuration(500)
        self.anim_pos.setStartValue(QRect(0, 30, 960, 600))
        self.anim_pos.setEndValue(QRect(0, 0, 960, 600))
        self.anim_pos.setEasingCurve(QEasingCurve.OutBack) # Ефект легкого "відскоку"

        # 5. Запускаємо обидві анімації разом
        self.anim_opacity.start()
        self.anim_pos.start()


    def toggleSettingsPanel(self, event=None):
        anim = QPropertyAnimation(self.settings_panel, b"geometry")
        anim.setDuration(400)
        anim.setEasingCurve(QEasingCurve.OutBack)

        if not self.settings_open:
            anim.setStartValue(QRect(20, 50, 40, 40))
            anim.setEndValue(QRect(20, 50, 220, 375))
            self.settings_panel.setStyleSheet("""
                QWidget {
                    background-color: rgba(255, 255, 255, 0.45);
                    border-radius: 14px;
                    border: 1px solid rgba(255, 255, 255, 0.6);
                }
                QLabel {
                    background: transparent;
                    border: none;
                }             
                
            """)
            self.settings_content.show()
            
            self.settings_open = True
        else:
            anim.setStartValue(QRect(20, 50, 220, 375))
            anim.setEndValue(QRect(20, 50, 40, 40))
            self.settings_panel.setStyleSheet("""
                QWidget {
                    background-color: rgba(255, 255, 255, 0.45);
                    border-radius: 5px;
                    border: 1px solid rgba(255, 255, 255, 0.6);
                }			
                
                QLabel {
                    background: transparent;
                    border: none;
                }                                 
            """)
            self.settings_content.hide()
            self.settings_open = False

        anim.start()
        self.settings_panel.anim = anim

                


    def createHistoryPanel(self):
        # Створюємо панель (контейнер)
        self.history_panel = QtWidgets.QWidget(self.centralwidget)
        # Початкова позиція справа (X=900, Y=50)
        self.history_panel.setGeometry(900, 50, 40, 40)
        self.history_panel.setObjectName("history_panel")

        # Стиль ідентичний налаштуванням (скло)
        self.design_history_panel = self.history_panel.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.45);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }
            QLabel {
                background: transparent;
                border: none;
            }                                                      
        """)

        # Тінь
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.history_panel.setGraphicsEffect(shadow)

        # Іконка на згорнутій панелі
        self.history_icon = QLabel(self.history_panel)
        self.history_icon.setPixmap(QPixmap("../image/icon/history_regular_icon.svg"))
        self.history_icon.setGeometry(0, 0, 40, 40)
        self.history_icon.setAlignment(Qt.AlignCenter)

        # Створюємо контент (спочатку прихований)
        self.create_HistoryContent()

        self.history_open = False
        self.history_full = False

        # Логіка кліків (як ми робили для налаштувань)
        self.history_icon.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.history_icon.setCursor(Qt.PointingHandCursor)
        self.history_icon.mousePressEvent = self.toggleHistoryPanel

    def create_HistoryContent(self):
        self.history_content = QtWidgets.QWidget(self.history_panel)
        # Розмір контенту: ширина 245, висота 450
        self.history_content.setGeometry(0, 0, 245, 450)
        self.history_content.setStyleSheet("background: transparent; border: none;")
        self.history_content.hide()

        # Кнопка-іконка всередині (щоб клікати для закриття)
        # Важливо: у налаштувань вона зліва (0,0), тут краще теж лишити її логічно
        # або змістити вправо, якщо хочеш дзеркальності. Я залишу зліва для зручності.
        self.icon_hist_inner = QtWidgets.QPushButton(self.history_content)
        self.icon_hist_inner.setGeometry(0, 0, 40, 40) # Або (205, 0) якщо хочеш справа
        self.icon_hist_inner.setStyleSheet("background: transparent; border: none;")
        self.icon_hist_inner.setCursor(Qt.PointingHandCursor)
        self.icon_hist_inner.mousePressEvent = self.toggleHistoryPanel
        
        # Кнопка розгортання на весь екран (стрілочка)
        self.btn_full_history = QtWidgets.QLabel(self.history_content)
        self.btn_full_history.setPixmap(QPixmap("../image/icon/arrow_right_regular_icon.svg"))
        # Розміщуємо стрілку з іншого боку або так само
        self.btn_full_history.setGeometry(200, 0, 40, 40)
        self.btn_full_history.setCursor(Qt.PointingHandCursor)
        self.btn_full_history.setStyleSheet("""
            QLabel:hover { background: rgba(255,255,255,0.3); border-radius: 15px; }
        """)
        self.btn_full_history.mousePressEvent = self.full_history_panel

        # Заголовок "Історія"
        self.lbl_history_title = QLabel("Історія", self.history_content)
        self.lbl_history_title.setGeometry(60, 10, 120, 20)
        self.lbl_history_title.setAlignment(Qt.AlignCenter)
        self.lbl_history_title.setStyleSheet("color: #581c87; font-size: 12pt; font-weight: bold;")

        # Scroll Area для списку
        self.history_scroll = QtWidgets.QScrollArea(self.history_content)
        self.history_scroll.setGeometry(10, 50, 225, 390)
        self.history_scroll.setWidgetResizable(True)
        # Прибираємо рамки самого скролу, щоб було "чисто"
        self.history_scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { width: 8px; background: transparent; }
            QScrollBar::handle:vertical { background: rgba(88, 28, 135, 0.3); border-radius: 4px; }
        """)
        
        self.scroll_content_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content_widget)
        self.history_scroll.setWidget(self.scroll_content_widget)

    def toggleHistoryPanel(self, event=None):
        anim = QPropertyAnimation(self.history_panel, b"geometry")
        anim.setDuration(400)
        anim.setEasingCurve(QEasingCurve.OutBack)

        if not self.history_open:
            # ВІДКРИТТЯ (Initial -> Quick View)
            # Старт: X=900, W=40 (правий край = 940)
            anim.setStartValue(QRect(900, 50, 40, 40))
            
            # Фініш: Ширина 245. Щоб правий край лишився 940, X має стати: 940 - 245 = 695
            anim.setEndValue(QRect(695, 50, 245, 450))
            
            self.history_panel.setStyleSheet("""
                QWidget {
                    background-color: rgba(255, 255, 255, 0.45);
                    border-radius: 14px;
                    border: 1px solid rgba(255, 255, 255, 0.6);
                }
                QLabel { background: transparent; border: none; }
            """)
            self.history_content.show()
            self.history_open = True
        else:
            # ЗАКРИТТЯ (Quick View -> Initial)
            anim.setStartValue(QRect(695, 50, 245, 450))
            anim.setEndValue(QRect(900, 50, 40, 40))
            
            self.history_panel.setStyleSheet("""
                QWidget {
                    background-color: rgba(255, 255, 255, 0.45);
                    border-radius: 8px;
                    border: 1px solid rgba(255, 255, 255, 0.6);
                }
                QLabel { background: transparent; border: none; }
            """)
            self.history_content.hide()
            self.history_open = False
            self.history_full = False # Скидаємо прапорець повного екрану

        anim.start()
        self.history_panel.anim = anim

    def full_history_panel(self, event=None):
        anim = QPropertyAnimation(self.history_panel, b"geometry")
        anim.setDuration(500)
        anim.setEasingCurve(QEasingCurve.OutBack)

        if not self.history_full:
            # РОЗГОРТАННЯ НА ВЕСЬ ЕКРАН
            anim.setStartValue(QRect(695, 50, 245, 450)) # Поточний стан
            anim.setEndValue(QRect(0, 0, 960, 600))      # На все вікно
            
            self.history_panel.setStyleSheet("""
                QWidget {
                    background-color: rgba(255, 255, 255, 0.45);
                    border-radius: 0px;
                    border: 1px solid rgba(255, 255, 255, 0.6);
                }
                QLabel { background: transparent; border: none; }
            """)
            self.history_full = True
        else:
            # ПОВЕРНЕННЯ ДО МАЛЕНЬКОГО ВІКНА (не до кнопки, а до панелі 245х450)
            anim.setStartValue(QRect(0, 0, 960, 600))
            anim.setEndValue(QRect(900, 50, 40, 40)) # Або одразу згортаємо в кнопку, як у налаштуваннях
            
            # Якщо хочеш як у налаштуваннях (одразу в іконку):
            self.history_panel.setStyleSheet("""
                QWidget {
                    background-color: rgba(255, 255, 255, 0.45);
                    border-radius: 8px;
                    border: 1px solid rgba(255, 255, 255, 0.6);
                }
                QLabel { background: transparent; border: none; }
            """)
            self.history_content.hide()
            self.history_open = False
            self.history_full = False

        anim.start()
        self.history_panel.anim = anim




        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_MainWindow()
    ui.show()
    sys.exit(app.exec_())
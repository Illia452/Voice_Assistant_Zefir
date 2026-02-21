from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QButtonGroup
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, pyqtProperty, QPoint, QTimer
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QCheckBox
from PyQt5.QtGui import QColor, QFont, QPixmap, QPainter, QIcon
import json
import os
from communications import comm
import arrow


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
        self.setFixedSize(40, 22)
        self.setCursor(Qt.PointingHandCursor)
        
        self._circle_position = 2
        
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(350)
        self.animation.setEasingCurve(QEasingCurve.InOutQuint)

        self.toggled.connect(self.start_transition)

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transition(self, is_checked):
        """Цей метод відповідає за рух кульки"""
        self.animation.stop()
        # 2 — старт, 20 — кінець (40 ширина - 18 кулька - 2 відступ)
        end_value = 20 if is_checked else 2
        self.animation.setEndValue(float(end_value))
        self.animation.start()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        is_checked = self.isChecked()
        # Використовуємо _circle_position для плавного переходу кольору або просто міняємо
        bg_color = QColor(147, 51, 234, 230) if is_checked else QColor("#EDE9FE")
        
        p.setBrush(bg_color)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 11, 11)
        
        p.setBrush(QColor("white"))
        # Малюємо кульку за її поточними координатами з анімації
        p.drawEllipse(int(self._circle_position), 2, 18, 18)
    
    def hitButton(self, pos: QPoint):
        return self.rect().contains(pos)

    # nextCheckState тепер можна не чіпати, або просто залишити порожнім super()
    # оскільки toggled.connect зробить всю роботу за нас

class UI_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        with open('pyqt5_ui/settings_ui.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.setupUI()
        comm.update_history.connect(self.update_history)
        self.setup_auto_update()

    def closeEvent(self, event):
        comm.stop_gtts.emit()
        event.accept() 


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
        self.full_history_content()



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
        self.btn_menu_general = QtWidgets.QPushButton("Загальні")
        self.btn_menu_voice = QtWidgets.QPushButton("Голос")
        self.btn_menu_commands = QtWidgets.QPushButton("Команди") # Новий розділ
        self.btn_menu_interface = QtWidgets.QPushButton("Інтерфейс")
        self.btn_menu_about = QtWidgets.QPushButton("Про систему")

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
        self.setup_voice_page()
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

    def setup_voice_page(self):
        """ Наповнення сторінки 'Голос' """
        if self.page_voice.layout():
            QtWidgets.QWidget().setLayout(self.page_voice.layout())

        layout = QtWidgets.QVBoxLayout(self.page_voice)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        # КАРТКА ГОЛОСОВОГО СУПРОВОДУ
        card_voice = self.createGlassCard()
        card_voice.setFixedHeight(100)
        voice_row = QtWidgets.QHBoxLayout(card_voice)
        voice_row.setContentsMargins(20, 0, 20, 0)
        
        text_v_layout = QtWidgets.QVBoxLayout()
        lbl_v_title = QtWidgets.QLabel("Голосовий супровід")
        lbl_v_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #581c87; border: none;")
        lbl_v_desc = QtWidgets.QLabel("Асистент буде озвучувати свої дії та відповіді")
        lbl_v_desc.setStyleSheet("font-size: 12px; color: #9CA3AF; border: none;")
        text_v_layout.addWidget(lbl_v_title)
        text_v_layout.addWidget(lbl_v_desc)
        
        voice_row.addLayout(text_v_layout)
        voice_row.addStretch()

        self.toggle_voice_main = GlassToggle(card_voice)
        # Стан з JSON
        self.toggle_voice_main.setChecked(self.settings_data.get("voice", {}).get("voice_support", True))
        # Сигнал
        self.toggle_voice_main.toggled.connect(lambda checked: self.sync_voice_support(checked, "main"))
        
        voice_row.addWidget(self.toggle_voice_main)
        layout.addWidget(card_voice)
        layout.addStretch()

    def sync_voice_support(self, state, source):
        """ Синхронізація перемикачів та запис у JSON """
        # Викликаємо save_setting з правильними аргументами:
        # 1. ["voice", "voice_support"] - це список ключів у JSON
        # 2. state - це True або False від тумблера
        self.save_setting(["voice", "voice_support"], state)

        # Синхронізуємо візуальний стан тумблерів
        if source == "main":
            # Якщо змінили в розділі "Голос", штовхаємо тумблер у швидких налаштуваннях
            if hasattr(self, 'toggle_voice_quick'):
                if self.toggle_voice_quick.isChecked() != state:
                    self.toggle_voice_quick.setChecked(state)
        else:
            # Якщо змінили у швидких, штовхаємо тумблер у розділі "Голос"
            if hasattr(self, 'toggle_voice_main'):
                if self.toggle_voice_main.isChecked() != state:
                    self.toggle_voice_main.setChecked(state)

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
        """ Наповнення сторінки 'Загальні' з вибором методу активації """
        # Очищення старого лейауту (якщо був)
        if self.page_general.layout():
            QtWidgets.QWidget().setLayout(self.page_general.layout())

        layout = QtWidgets.QVBoxLayout(self.page_general)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        # --- КАРТКА: МЕТОД АКТИВАЦІЇ ---
        card_act = self.createGlassCard()
        card_act_layout = QtWidgets.QVBoxLayout(card_act)
        card_act_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_act_title = QtWidgets.QLabel("Активація помічника")
        lbl_act_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #581c87;")
        
        lbl_act_desc = QtWidgets.QLabel("Оберіть від чого асистент повинен прокидатися для ваших запитів")
        lbl_act_desc.setStyleSheet("font-size: 13px; color: #9CA3AF; border: none; margin-bottom: 10px;")
        
        card_act_layout.addWidget(lbl_act_title)
        card_act_layout.addWidget(lbl_act_desc)

        # Створення радіо-кнопок
        self.radio_keys = ModernRadioButton("Гарячі клавіші (Alt + Z)")
        self.radio_voice = ModernRadioButton("Ключове слово (Зефір)")
        self.radio_both = ModernRadioButton("Комбінований (Голос + Клавіші)")

        # Групування
        self.act_group = QtWidgets.QButtonGroup(self)
        self.act_group.addButton(self.radio_keys)
        self.act_group.addButton(self.radio_voice)
        self.act_group.addButton(self.radio_both)

        # Відновлення стану з JSON
        current_act = self.settings_data.get("general", {}).get("assis_activate", "BOTH")
        if current_act == "KEYS": self.radio_keys.setChecked(True)
        elif current_act == "VOICE": self.radio_voice.setChecked(True)
        else: self.radio_both.setChecked(True)

        # Підключення збереження
        self.radio_keys.clicked.connect(lambda: self.save_setting(["general", "assis_activate"], "KEYS"))
        self.radio_voice.clicked.connect(lambda: self.save_setting(["general", "assis_activate"], "VOICE"))
        self.radio_both.clicked.connect(lambda: self.save_setting(["general", "assis_activate"], "BOTH"))

        # Додавання у лейаут картки
        card_act_layout.addWidget(self.radio_keys)
        card_act_layout.addWidget(self.radio_voice)
        card_act_layout.addWidget(self.radio_both)

        layout.addWidget(card_act)

        # # --- КАРТКА 2: АВТОЗАПУСК (ЗАГОТОВКА) ---
        # card_boot = self.createGlassCard()
        # card_boot.setFixedHeight(80)
        # boot_row = QtWidgets.QHBoxLayout(card_boot)
        # boot_row.setContentsMargins(20, 0, 20, 0)
        
        # boot_text_layout = QtWidgets.QVBoxLayout()
        # lbl_boot_t = QtWidgets.QLabel("Запускати разом з Windows")
        # lbl_boot_t.setStyleSheet("font-size: 16px; font-weight: bold; color: #4B5563; border: none;")
        # lbl_boot_d = QtWidgets.QLabel("Автоматичний старт при вході в систему")
        # lbl_boot_d.setStyleSheet("font-size: 12px; color: #9CA3AF; border: none;")
        # boot_text_layout.addWidget(lbl_boot_t)
        # boot_text_layout.addWidget(lbl_boot_d)
        
        # boot_row.addLayout(boot_text_layout)
        # boot_row.addStretch()
        # boot_row.addWidget(GlassToggle(card_boot))

        # layout.addWidget(card_boot)
        # layout.addStretch()

    def setup_placeholder_page(self, page_widget, text):
        """ Тимчасовий метод для пустих сторінок """
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
        self.settings_file = "pyqt5_ui/settings_ui.json"
        
        default_path = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
        self.settings_data = {
            "screenshot": {"format": "PNG", "path": default_path},
            "general": {"assis_activate": "BOTH"},
            "voice": {"voice_support": True}
        }

        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        loaded_data = json.loads(content)
                        # Злиття даних для всіх секцій
                        for key in ["screenshot", "general", "voice"]:
                            if key in loaded_data:
                                self.settings_data[key].update(loaded_data[key])
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

        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings_data, f, indent=4, ensure_ascii=False)



    def setup_commands_page(self):
        # Очистка лейауту (стандартна процедура для рефрешу сторінки)
        if self.page_commands.layout():
             QtWidgets.QWidget().setLayout(self.page_commands.layout())

        layout = QtWidgets.QVBoxLayout(self.page_commands)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        # --- КАРТКА 1: ФОРМАТ ---

        card_title = self.createGlassCard()
        card_title_layout = QtWidgets.QVBoxLayout(card_title)
        card_title_layout.setContentsMargins(20, 20, 20, 20)
        title_screen = QtWidgets.QLabel("Налашутвання для скріншоту")
        title_screen.setStyleSheet("font-size: 18px; font-weight: bold; color: #581c87")
        card_title_layout.addWidget(title_screen)

        layout.addWidget(card_title)


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

        lbl_path_t = QtWidgets.QLabel("Шлях збереження файлів")
        lbl_path_t.setStyleSheet("font-size: 16px; font-weight: bold; color: #581c87; margin-bottom: 5px;")
        card_path_layout.addWidget(lbl_path_t)
        
        # Горизонтальний контейнер для елементів шляху
        row_path = QtWidgets.QHBoxLayout()
        row_path.setSpacing(12) # Відступ між іконкою, текстом і кнопкою

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


    def clickButton_Send(self):
        user_text = self.InputField.text()
        text = user_text.strip()
        comm.final_command.emit(text)
        self.InputField.setText("")

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
        self.button_send.clicked.connect(self.clickButton_Send)
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

        self.lbl_settings_title = QLabel("Налаштування", self.settings_content)
        self.lbl_settings_title.setGeometry(40, 10, 140, 20)
        self.lbl_settings_title.setAlignment(Qt.AlignCenter)
        self.lbl_settings_title.setStyleSheet("color: #581c87; font-size: 11pt; font-weight: bold;")

        # ЧОРНА ЗОНА: Кнопка "Більше" знизу
        self.btn_more_settings = QtWidgets.QPushButton("Більше", self.settings_content)
        self.btn_more_settings.setGeometry(20, 320, 180, 35)
        self.btn_more_settings.setCursor(Qt.PointingHandCursor)
        self.btn_more_settings.setStyleSheet("""
            QPushButton {
                background-color: rgba(139, 92, 246, 0.1);
                color: #581c87;
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 10px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: rgba(139, 92, 246, 0.2);
                border: 1px solid #8b5cf6;
            }
        """)
        self.btn_more_settings.clicked.connect(self.full_setting_panel)

        self.createQuickSettingRow("Темна тема", 60)
        self.createQuickSettingRow("Автозапуск", 110)
        self.toggle_voice_quick = self.createQuickSettingRow("Голос", 160)
        
        # Встановлюємо початковий стан
        voice_state = self.settings_data.get("voice", {}).get("voice_support", True)
        self.toggle_voice_quick.setChecked(voice_state)
        
        # Підключаємо сигнал
        self.toggle_voice_quick.toggled.connect(lambda checked: self.sync_voice_support(checked, "quick"))

    def createQuickSettingRow(self, text, y_pos):
        lbl = QLabel(text, self.settings_content)
        lbl.setGeometry(20, y_pos, 120, 20)
        lbl.setStyleSheet("color: #581c87; font-size: 11pt; border: none; background: transparent;")
        
        toggle = GlassToggle(self.settings_content)
        toggle.move(150, y_pos)
        return toggle # Повертаємо об'єкт для подальшого використання



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

        # Логіка кліків
        self.history_icon.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.history_icon.setCursor(Qt.PointingHandCursor)
        self.history_icon.mousePressEvent = self.toggleHistoryPanel

    def create_HistoryContent(self):
        self.history_content = QtWidgets.QWidget(self.history_panel)
        self.history_content.setGeometry(0, 0, 220, 375)
        self.history_content.setStyleSheet("background: transparent; border: none;")
        self.history_content.hide()

        # Заголовок та кнопка іконки (залишаємо як було)
        self.icon_hist_inner = QtWidgets.QPushButton(self.history_content)
        self.icon_hist_inner.setGeometry(180, 0, 40, 40)
        self.icon_hist_inner.setStyleSheet("background: transparent; border: none;")
        self.icon_hist_inner.clicked.connect(self.toggleHistoryPanel)

        self.lbl_history_title = QLabel("Історія", self.history_content)
        self.lbl_history_title.setGeometry(45, 10, 130, 20)
        self.lbl_history_title.setAlignment(Qt.AlignCenter)
        self.lbl_history_title.setStyleSheet("color: #581c87; font-size: 11pt; font-weight: bold;")

        # СТВОРЮЄМО СКРОЛ-ЗОНУ
        self.history_scroll = QtWidgets.QScrollArea(self.history_content)
        self.history_scroll.setGeometry(10, 50, 200, 260)
        self.history_scroll.setWidgetResizable(True)
        self.history_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # Вимикаємо горизонтальну прокрутку
        self.history_scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                width: 4px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: rgba(139, 92, 246, 0.4);
                border-radius: 2px;
            }
        """)
        
        # Віджет-контейнер для списку
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setSpacing(8)
        self.scroll_layout.addStretch() # Пружина знизу, щоб блоки не розтягувалися
        
        self.history_scroll.setWidget(self.scroll_content)

        # Кнопка Більше
        self.btn_more_history = QtWidgets.QPushButton("Більше", self.history_content)
        self.btn_more_history.setGeometry(20, 325, 180, 35)
        self.btn_more_history.setStyleSheet("""
            QPushButton {
                background-color: rgba(139, 92, 246, 0.15);
                color: #581c87;
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 10px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: rgba(139, 92, 246, 0.2);
                border: 1px solid #8b5cf6;
            }
        """) 
        self.btn_more_history.clicked.connect(self.full_history_panel)

        # ДЛЯ ТЕСТУ: додамо кілька блоків
        self.update_history()

    def setup_auto_update(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_history)

        self.timer.start(60000)

    @pyqtSlot()
    def update_history(self):
        while self.scroll_layout.count() > 0:
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater() 


        history_file = "pyqt5_ui/history_ui.json"
        
        with open(history_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        history = data.get("history", {})
        i = 0
        for event in history:
            i += 1
            t = arrow.get(event[0])
            time = t.humanize(locale='uk')
            now = arrow.now()
            diff = now.timestamp() - event[0]
            if diff < 60:
                time = "щойно"
            if t.date() == arrow.now().shift(days=-1).date():
                time = "Вчора"

            self.add_history_item(event[1], time)

            if i > 20:
                break
                


    def toggleHistoryPanel(self, event=None):
        # Копіюємо логіку перевірки стану (як у settings)

        self.anim_hist = QPropertyAnimation(self.history_panel, b"geometry")
        self.anim_hist.setDuration(400)
        self.anim_hist.setEasingCurve(QEasingCurve.OutBack) # Така ж крива, як у settings

        if not self.history_open:
            # Відкриття: рухаємося з x=900 (кнопка) до x=720 (панель)
            self.anim_hist.setStartValue(QRect(900, 50, 40, 40))
            self.anim_hist.setEndValue(QRect(720, 50, 220, 375))
            
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
            self.history_icon.move(180, 0) # Переміщуємо іконку в край панелі
        else:
            # Закриття
            self.anim_hist.setStartValue(QRect(720, 50, 220, 375))
            self.anim_hist.setEndValue(QRect(900, 50, 40, 40))
            
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
            self.history_icon.move(0, 0)

        self.anim_hist.start()
    # --- ЛОГІКА ПОВНОЕКРАННОЇ ІСТОРІЇ ---

    def full_history_content(self):
        """ Контейнер історії на весь екран (аналог full_setting_content) """
        self.history_main_container = QtWidgets.QWidget(self.centralwidget)
        self.history_main_container.setGeometry(0, 0, 960, 600)
        self.history_main_container.setStyleSheet("background: #EDE9FE;") 
        
        self.fade_effect_hist = QGraphicsOpacityEffect(self.history_main_container)
        self.history_main_container.setGraphicsEffect(self.fade_effect_hist)
        self.fade_effect_hist.setOpacity(0)
        self.history_main_container.hide()

        layout_full_hist = QtWidgets.QVBoxLayout(self.history_main_container)
        layout_full_hist.setContentsMargins(30, 20, 30, 20)
        layout_full_hist.setAlignment(Qt.AlignTop)

        self.btn_back_hist = QtWidgets.QPushButton("  Назад")
        self.btn_back_hist.setCursor(Qt.PointingHandCursor)
        self.btn_back_hist.setMinimumSize(100, 40)
        self.btn_back_hist.clicked.connect(self.close_history) 
        self.btn_back_hist.setIcon(QtGui.QIcon("../image/icon/arrow_left_regular_icon.svg")) 
        self.btn_back_hist.setStyleSheet("""
            QPushButton {
                background-color: white; border-radius: 12px; color: #581c87;
                font-size: 15px; font-weight: bold; border: 1px solid rgba(139, 92, 246, 0.2);
            }
            QPushButton:hover { background-color: #F5F3FF; border: 1px solid #8b5cf6; }
        """)
        layout_full_hist.addWidget(self.btn_back_hist, alignment=Qt.AlignLeft)

    def close_history(self):
        """ Закриття повноекранної історії з анімацією """
        self.anim_opacity_hist_close = QPropertyAnimation(self.fade_effect_hist, b"opacity")
        self.anim_opacity_hist_close.setDuration(400)
        self.anim_opacity_hist_close.setStartValue(1.0)
        self.anim_opacity_hist_close.setEndValue(0.0)
        self.anim_opacity_hist_close.setEasingCurve(QEasingCurve.InQuad)

        self.anim_pos_hist_close = QPropertyAnimation(self.history_main_container, b"geometry")
        self.anim_pos_hist_close.setDuration(400)
        self.anim_pos_hist_close.setStartValue(QRect(0, 0, 960, 600))
        self.anim_pos_hist_close.setEndValue(QRect(0, 30, 960, 600))
        
        self.anim_opacity_hist_close.finished.connect(self.history_main_container.hide)

        self.anim_opacity_hist_close.start()
        self.anim_pos_hist_close.start()

    def add_history_item(self, text, time_str):
        # Контейнер для однієї картки
        item_widget = QtWidgets.QWidget()
        item_widget.setMinimumHeight(60)
        item_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 10px;
                border: 1px solid rgba(139, 92, 246, 0.1);
            }
            QWidget:hover {
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(139, 92, 246, 0.3);
            }
        """)

        layout = QtWidgets.QVBoxLayout(item_widget)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(2)

        # Текст запиту
        lbl_text = QLabel(text)
        lbl_text.setWordWrap(True)
        lbl_text.setStyleSheet("color: #1f2937; font-size: 15px; font-weight: 500; border: none; background: transparent;")

        # Час
        lbl_time = QLabel(time_str)
        lbl_time.setStyleSheet("color: #6e737a; font-size: 12px; border: none; background: transparent;")

        layout.addWidget(lbl_text)
        layout.addWidget(lbl_time)

        # Додаємо у головний лейаут скролу (який ми створимо нижче)
        self.scroll_layout.insertWidget(0, item_widget) # Нові записи будуть зверху

    def full_history_panel(self, event=None):
        """ Відкриття історії на весь екран """
        if self.history_open:
            self.toggleHistoryPanel() # Плавно ховаємо маленьке вікно

        self.history_main_container.show()
        self.history_main_container.raise_()

        self.anim_opacity_hist = QPropertyAnimation(self.fade_effect_hist, b"opacity")
        self.anim_opacity_hist.setDuration(500)
        self.anim_opacity_hist.setStartValue(0.0)
        self.anim_opacity_hist.setEndValue(1.0)
        self.anim_opacity_hist.setEasingCurve(QEasingCurve.OutQuad)

        self.anim_pos_hist = QPropertyAnimation(self.history_main_container, b"geometry")
        self.anim_pos_hist.setDuration(500)
        self.anim_pos_hist.setStartValue(QRect(0, 30, 960, 600))
        self.anim_pos_hist.setEndValue(QRect(0, 0, 960, 600))
        self.anim_pos_hist.setEasingCurve(QEasingCurve.OutBack)

        self.anim_opacity_hist.start()
        self.anim_pos_hist.start()




        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_MainWindow()
    ui.show()
    sys.exit(app.exec_())
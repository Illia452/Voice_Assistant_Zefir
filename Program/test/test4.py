from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, pyqtProperty, QPoint, QSize, QVariantAnimation
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QCheckBox
from PyQt5.QtGui import QColor, QFont, QPixmap, QPainter, QIcon




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
        bg_color = QColor(147, 51, 234, 230) if is_checked else QColor(255, 255, 255, 80)
        
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
        self.setupUI()


    def setupUI(self):
        self.createMainWindow()
        self.createTitleStatus()
        self.createInputField_ForCommands()
        self.createButtonSend()
        self.createButtonStartStop()
        self.createIconZefir()
        self.createButtonUseMicrophone()
        self.createSettingPanel()
        self.createHistoryPanel()
        # self.full_setting_content()



    def createMainWindow(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(960,600)
        self.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, \n"
                                      "                                stop:0 #F3E8FF, stop:1 #D8B4FE);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.setFocusPolicy(Qt.ClickFocus)

    # def full_setting_content(self):
    #     self.main_container = QtWidgets.QWidget(self.centralwidget)
    #     self.main_container.setGeometry(0, 0, 960, 600)
    #     self.main_container.setStyleSheet("background: #EDE9FE;")



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
        # Ініціалізуємо повний інтерфейс один раз, якщо ще не створений
        if not hasattr(self, 'full_settings_widget'):
            self.createFullSettingsUI()

        self.anim_geo = QPropertyAnimation(self.settings_panel, b"geometry")
        self.anim_geo.setDuration(500)
        self.anim_geo.setEasingCurve(QEasingCurve.OutQuint)

        self.anim_color = QVariantAnimation()
        self.anim_color.setDuration(500)
        
        color_glass = QColor(255, 255, 255, 115) 
        color_full = QColor(245, 243, 255, 245) # Більш непрозорий (245 alpha)

        if not self.settings_full:
            # ---> РОЗГОРТАННЯ
            self.anim_geo.setStartValue(QRect(20, 50, 220, 375))
            self.anim_geo.setEndValue(QRect(0, 0, 960, 600))
            
            self.anim_color.setStartValue(color_glass)
            self.anim_color.setEndValue(color_full)
            
            # Ховаємо мале меню одразу
            self.settings_content.hide() 
            
            # Коли анімація закінчиться -> покажемо велике меню
            self.anim_geo.finished.connect(lambda: self.full_settings_widget.show())
            self.anim_geo.finished.connect(self.raise_panels) # Щоб панель була зверху

            self.settings_full = True
            
        else:
            # ---> ЗГОРТАННЯ
            self.full_settings_widget.hide() # Ховаємо велике меню одразу
            
            self.anim_geo.setStartValue(QRect(0, 0, 960, 600))
            self.anim_geo.setEndValue(QRect(20, 50, 40, 40)) # Повертаємо в кнопку
            
            self.anim_color.setStartValue(color_full)
            self.anim_color.setEndValue(color_glass)
            
            self.settings_open = False
            self.settings_full = False

        # Оновлення стилю під час анімації
        def update_style(color):
            radius = 0 if self.settings_full and self.anim_geo.state() == QPropertyAnimation.Running else 14
            self.settings_panel.setStyleSheet(f"""
                QWidget#settings_panel {{
                    background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});
                    border-radius: {radius}px;
                    border: 1px solid rgba(255, 255, 255, 0.6);
                }}
            """)

        self.anim_color.valueChanged.connect(update_style)
        
        self.anim_geo.start()
        self.anim_color.start()

    def raise_panels(self):
        """ Піднімає панель нагору, щоб перекрити інші елементи """
        self.settings_panel.raise_()


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


class ModernSlider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setFixedHeight(30)
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c084fc, stop:1 #a855f7);
                border-radius: 5px;
            }
            QSlider::add-page:horizontal {
                background: #e5e7eb;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: white;
                border: 1px solid #c084fc;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #f3e8ff;
            }
        """)

    def createFullSettingsUI(self):
        # Головний контейнер для великих налаштувань (спочатку прихований)
        self.full_settings_widget = QtWidgets.QWidget(self.settings_panel)
        self.full_settings_widget.setGeometry(0, 0, 960, 600)
        self.full_settings_widget.setStyleSheet("background: transparent;")
        self.full_settings_widget.hide()

        # 1. Заголовок і кнопка "Назад"
        header_layout = QtWidgets.QHBoxLayout()
        
        self.btn_back = QtWidgets.QPushButton(" Назад")
        self.btn_back.setIcon(QIcon("../image/icon/arrow_left_regular_icon.svg")) # Заміни на свою іконку стрілки вліво
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setStyleSheet("""
            QPushButton { color: #581c87; font-size: 18px; border: none; font-weight: bold;}
            QPushButton:hover { color: #7e22ce; }
        """)
        self.btn_back.clicked.connect(self.full_setting_panel) # Клік закриває вікно
        
        title = QLabel("Налаштування")
        title.setStyleSheet("color: #581c87; font-size: 24pt; font-weight: bold;")
        
        header_layout.addWidget(self.btn_back)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()

        # 2. Основна розмітка (Зліва меню, Справа контент)
        body_layout = QtWidgets.QHBoxLayout()
        body_layout.setContentsMargins(40, 20, 40, 40)
        body_layout.setSpacing(40)

        # --- ЛІВА ПАНЕЛЬ (Меню) ---
        menu_layout = QtWidgets.QVBoxLayout()
        menu_layout.setSpacing(10)
        
        self.btn_tab_general = MenuButton("⚡ Загальні")
        self.btn_tab_voice = MenuButton("🎙️ Голос та Звук")
        self.btn_tab_interface = MenuButton("🎨 Інтерфейс")
        self.btn_tab_system = MenuButton("🖥️ Система")
        
        self.btn_tab_general.setChecked(True) # Активна перша вкладка

        menu_layout.addWidget(self.btn_tab_general)
        menu_layout.addWidget(self.btn_tab_voice)
        menu_layout.addWidget(self.btn_tab_interface)
        menu_layout.addWidget(self.btn_tab_system)
        menu_layout.addStretch()
        
        # --- ПРАВА ПАНЕЛЬ (Stacked Widget для сторінок) ---
        self.pages_stack = QtWidgets.QStackedWidget()
        
        # Сторінка 1: Загальні
        page_general = self.createPage_General()
        # Сторінка 2: Голос (приклад)
        page_voice = self.createPage_Voice()
        
        self.pages_stack.addWidget(page_general)
        self.pages_stack.addWidget(page_voice)
        # ... додай інші сторінки аналогічно

        # Логіка перемикання сторінок
        self.btn_tab_general.clicked.connect(lambda: self.switchTab(0, self.btn_tab_general))
        self.btn_tab_voice.clicked.connect(lambda: self.switchTab(1, self.btn_tab_voice))

        body_layout.addLayout(menu_layout, 1)
        body_layout.addWidget(self.pages_stack, 3)

        # Збираємо все в головний layout
        main_layout = QtWidgets.QVBoxLayout(self.full_settings_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(body_layout)

    def switchTab(self, index, button):
        self.pages_stack.setCurrentIndex(index)
        # Скидаємо стиль всім кнопкам
        for btn in [self.btn_tab_general, self.btn_tab_voice, self.btn_tab_interface, self.btn_tab_system]:
            btn.setChecked(False)
        button.setChecked(True)

    def createPage_General(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)

        # Картка 1
        card = self.createGlassCard()
        card_layout = QtWidgets.QVBoxLayout(card)
        
        lbl = QLabel("Основні параметри")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #581c87; margin-bottom: 10px;")
        card_layout.addWidget(lbl)

        # Рядок з налаштуванням
        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(QLabel("Запускати разом з Windows", styleSheet="color: #4b5563; font-size: 16px;"))
        row1.addStretch()
        row1.addWidget(GlassToggle()) # Твій клас
        
        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(QLabel("Автоматичне оновлення", styleSheet="color: #4b5563; font-size: 16px;"))
        row2.addStretch()
        row2.addWidget(GlassToggle())

        card_layout.addLayout(row1)
        card_layout.addLayout(row2)
        
        layout.addWidget(card)
        return page

    def createPage_Voice(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setAlignment(Qt.AlignTop)
        
        card = self.createGlassCard()
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setSpacing(15)

        lbl = QLabel("Налаштування мікрофону")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #581c87;")
        card_layout.addWidget(lbl)

        # Слайдер чутливості
        lbl_sens = QLabel("Чутливість мікрофону")
        lbl_sens.setStyleSheet("color: #4b5563; font-size: 14px;")
        slider = ModernSlider()
        slider.setValue(70)

        card_layout.addWidget(lbl_sens)
        card_layout.addWidget(slider)

        layout.addWidget(card)
        return page

    def createGlassCard(self):
        """ Створює білу напівпрозору підкладку для налаштувань """
        card = QtWidgets.QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.6);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.8);
            }
        """)
        return card

class MenuButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(200, 45)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 20px;
                background-color: transparent;
                color: #581c87;
                font-size: 16px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.5);
            }
            QPushButton:checked {
                background-color: white;
                font-weight: bold;
                color: #a855f7;
            }
        """)
        self.setCheckable(True)






        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_MainWindow()
    ui.show()
    sys.exit(app.exec_())
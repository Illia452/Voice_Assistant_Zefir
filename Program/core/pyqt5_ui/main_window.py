from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtGui import QPixmap
import sys


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
        self.createButtonSetting()
        self.createButtonHistory()


    def createMainWindow(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(960,600)
        self.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, \n"
                                      "                                stop:0 #F3E8FF, stop:1 #D8B4FE);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.setFocusPolicy(Qt.ClickFocus)


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


    def createButtonSetting(self):
        self.button_setting = QtWidgets.QPushButton(self.centralwidget)
        self.button_setting.setGeometry(QtCore.QRect(20, 30, 35, 40))
        self.button_setting.setStyleSheet("""
			QPushButton {
				background-color: rgb(209, 213, 219);
				border-radius: 5px;
				border: 1px solid #d1d5db;
			}
			QPushButton:hover {
                background-color: #9ca3af;
				border: 1px solid #9ca3af;					
			}
		""")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)  # Розмиття
        shadow.setOffset(0, 4)  # Зміщення тіні (по X та Y)
        shadow.setColor(QColor(0, 0, 0, 30))  # Колір тіні (чорний з прозорістю)
        self.button_setting.setGraphicsEffect(shadow)

        self.button_setting.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/settings_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_setting.setIcon(icon)
        self.button_setting.setIconSize(QtCore.QSize(20, 20))
        self.button_setting.setObjectName("button_setting")
        self.button_setting.clicked.connect(self.clickButton_Setting)
        self.status_buttonSetting = True
        self.createSettingWindoww()



    def clickButton_Setting(self):
        if self.status_buttonSetting:
            self.setting_window.show()
            self.status_buttonSetting = False
        else:
            self.setting_window.hide()
            self.status_buttonSetting = True


    def createSettingWindoww(self):
        self.setting_window = QtWidgets.QWidget(self.centralwidget)
        self.setting_window.setGeometry(QtCore.QRect(30, 120, 220, 450))
        self.setting_window # Виводимо віджет на передній план
        # self.set_window.raise_()
        self.setting_window.setStyleSheet("""
			QWidget {
				background-color: #d1d5db;
				border-radius: 10px;
				border: 1px solid #d1d5db;
			}
		""")
        
        self.setting_window.hide()
        self.createTitleSetting_forWindow()
        self.createElementsInSettingWindow()

        
    def createTitleSetting_forWindow(self):
        self.title_setting = QtWidgets.QLabel("Налаштування", self.setting_window)
        self.title_setting.setStyleSheet("""
			QWidget {
				background-color: transparent;
				color: #581c87;
                font: 12pt Roboto
			}
		""")
        self.title_setting.move(10, 10)


    def createElementsInSettingWindow(self):
        self.checkbox = QtWidgets.QCheckBox("", self.setting_window)  # Пробіл для відступу
        self.checkbox.move(170, 48)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 16px;
                color: white;
                padding: 5px;
                border-radius: 5px;
                                    
                
            }                    
            /* Відключаємо стандартний індикатор */
            QCheckBox::indicator {
                    width: 13px;
                    height: 13px;
                    border: 2px solid #581c87;  
                    border-radius: 4px;
                    background-color: #f3f4f6;
            }
                                    
            QCheckBox::indicator:checked {
                background-color: #f3f4f6;
                image: url(icon/checkmark_regular_icon.svg);
            }
            QCheckBox::indicator:checked:hover {
                background-color: #c0c1c3;
                
            }
            QCheckBox::indicator:unchecked:hover {
                background-color: #c0c1c3;
            }

        """)

        self.label2 = QtWidgets.QLabel("Голосовий супровід", self.setting_window)
        self.label2.setStyleSheet("""
			QWidget {
				background-color: transparent;
				color: #0f172a;
                font: 9pt Roboto
			}
		""")
        self.label2.move(20, 50)


    def createButtonHistory(self):
        self.button_history = QtWidgets.QPushButton(self.centralwidget)
        self.button_history.setGeometry(QtCore.QRect(905, 30, 35, 40))
        self.button_history.setStyleSheet("""
			QPushButton {
				background-color: rgb(209, 213, 219);
				border-radius: 5px;
				border: 1px solid #d1d5db;
			}
			QPushButton:hover {
                background-color: #9ca3af;
				border: 1px solid #9ca3af;					
			}
		""")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)  # Розмиття
        shadow.setOffset(0, 4)  # Зміщення тіні (по X та Y)
        shadow.setColor(QColor(0, 0, 0, 30))  # Колір тіні (чорний з прозорістю)
        self.button_history.setGraphicsEffect(shadow)

        self.button_history.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/history_regular_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_history.setIcon(icon)
        self.button_history.setIconSize(QtCore.QSize(20, 20))
        self.button_history.setObjectName("but_history")
        self.button_history.clicked.connect(self.clickButton_History)
        self.status_buttonHistory = True
        self.createHistoryWindow()
        self.history_window.hide()



    def clickButton_History(self):
        if self.status_buttonHistory:
            self.history_window.show()
            self.status_buttonHistory = False
        else:
            self.history_window.hide()
            self.status_buttonHistory = True


    def createHistoryWindow(self):
        self.history_window = QtWidgets.QWidget(self.centralwidget)
        self.history_window.setGeometry(QtCore.QRect(685, 120, 245, 450))
        self.history_window # Виводимо віджет на передній план
        # self.his_window.raise_()
        self.history_window.setStyleSheet("""
			QWidget {
				background-color: #d1d5db;
				border-radius: 10px;
				border: 1px solid #d1d5db;
			}
		""")

        self.createTitleHistory_forWindow()
        

    def createTitleHistory_forWindow(self):

        self.title_history = QtWidgets.QLabel("Історія", self.history_window)
        self.title_history.setStyleSheet("""
			QWidget {
				background-color: transparent;
				color: #581c87;
                font: 12pt Roboto;
                text-ali
			}
		""")
        self.title_history.move(10, 10)
        self.title_history.setAlignment(Qt.AlignCenter)

        self.scroll_area = QtWidgets.QScrollArea(self.history_window)
        self.scroll_area.setGeometry(10, 45, 225, 395)  
        self.scroll_area.setWidgetResizable(True) 

        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content) 
        



        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_MainWindow()
    ui.show()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsDropShadowEffect,  QMainWindow, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, pyqtSlot
from PyQt5.QtGui import QColor, QFontDatabase, QFont
from PyQt5 import QtCore, QtGui, QtWidgets
from communications import comm


class PushWindow(QWidget):
    def __init__(self): 
        super().__init__()

        self.setupPushWindow()
        comm.start_push_window.connect(self.show_window)
        comm.stop_push_window.connect(self.close_window)
        comm.stream_text_gstt.connect(self.print_text)
        self.command = ""

    def setupPushWindow(self):
        # Встановлюємо прапорці вікна:
        # Qt.FramelessWindowHint - прибирає рамку вікна та кнопки.
        # Qt.WindowStaysOnTopHint - робить вікно завжди поверх інших.
        # Qt.Tool - прибирає іконку з панелі завдань 
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        font_id = QFontDatabase.addApplicationFont("../fonts/Roboto-VariableFont_wdth,wght.ttf")
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.setFixedSize(550, 200)

        
        self.setupUI()

        # self.createTitleStatus()
        self.createButtonClose()
        # self.createIcon_Zefir()
        self.createButton_Plus()
        self.createButton_Microphone()
        self.createButton_Send()
        self.createInputField()

    @pyqtSlot()
    def show_window(self):
        self.animate_show_push()
        self.listen_command_ON()


    def setupUI(self):
        # Створюємо внутрішній віджет
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0,
                                            stop:0 #F3E8FF, stop:1 #D8B4FE);
                border-radius: 20px;
                border: 2px solid #A855F7;
            }
        """)
        self.container.setGeometry(0, 0, 550, 200)
        
        self.position_window()
        self.animate_show_push()


    def setFontSize(self, label, size_pt):
        font = QFont(self.font_family, size_pt)
        label.setFont(font)
        

    def createButtonClose(self):
        self.button_close = QtWidgets.QPushButton(self.container)
        self.button_close.setGeometry(QtCore.QRect(490, 15, 40, 40))
        self.button_close.setStyleSheet("""
			QPushButton {
				background-color: transparent;
			}
		""")
        self.button_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/arrow_right_regular_icon_fat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close.setIcon(icon)
        self.button_close.setIconSize(QtCore.QSize(35, 35))
        self.button_close.clicked.connect(self.clickButton_close)
        self.button_close.show()


    def clickButton_close(self):
        comm.reset_focus.emit()
        self.animate_hide_push()
        QtCore.QTimer.singleShot(200, self.close_window)


    def close_window(self):
        print("тУТ 1")
        self.inputField.setText('')
        self.close()




    def createButton_Plus(self):
        self.button_plus = QtWidgets.QPushButton(self.container)
        self.button_plus.setGeometry(QtCore.QRect(20, 15, 40, 40))
        self.button_plus.setStyleSheet("""
			QPushButton {
				background-color: transparent;
			}
		""")
        self.button_plus.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/fluent_add_regular_icon_fat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_plus.setIcon(icon)
        self.button_plus.setIconSize(QtCore.QSize(35, 35))
        self.button_plus.clicked.connect(self.clickButton_plus)
        self.button_plus.show()


    def clickButton_plus(self):
        pass
    

    def createButton_Microphone(self):
        self.button_micro = QtWidgets.QPushButton(self.container)
        self.button_micro.setGeometry(QtCore.QRect(20, 140, 40, 40))
        self.button_micro.setStyleSheet("""
			QPushButton {
				background-color: transparent;
			}
		""")
        self.button_micro.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/mic_on_regular_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_micro.setIcon(icon)
        self.button_micro.setIconSize(QtCore.QSize(35, 35))
        self.button_micro.clicked.connect(self.clickButton_Micro)
        self.button_micro.show()

    def listen_command_ON(self):
        self.button_micro.setGeometry(QtCore.QRect(15, 140, 45, 45))
        self.button_micro.setStyleSheet("""
			QPushButton {
				background-color: #D8B4FE;
                border-radius: 20px;
                border: 3px solid #A855F7;
			}
		""")
        self.container.setStyleSheet("""
            #container {
                background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0,
                                            stop:0 #F3E8FF, stop:1 #D8B4FE);
                border-radius: 20px;
                border: 5px solid #A855F7;
            }
        """)

    def listen_command_OFF(self):
        self.button_micro.setGeometry(QtCore.QRect(20, 140, 40, 40))
        self.button_micro.setStyleSheet("""
			QPushButton {
				background-color: transparent;
			}
		""")
        self.container.setStyleSheet("""
            #container {
                background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0,
                                            stop:0 #F3E8FF, stop:1 #D8B4FE);
                border-radius: 20px;
                border: 2px solid #A855F7;
            }
        """)


    def clickButton_Micro(self):
        comm.activate_assistant.emit()
        self.listen_command_ON()


    def createButton_Send(self):
        self.button_send = QtWidgets.QPushButton(self.container)
        self.button_send.setGeometry(QtCore.QRect(490, 140, 40, 40))
        self.button_send.setStyleSheet("""
			QPushButton {
				background-color: transparent;
			}
		""")
        self.button_send.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/icon/fluent_send_filled_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_send.setIcon(icon)
        self.button_send.setIconSize(QtCore.QSize(30, 30))
        self.button_send.clicked.connect(self.clickButton_Send)
        self.button_send.show()


    def clickButton_Send(self):
        current_text = self.inputField.toPlainText()
        text = current_text.strip()
        comm.final_command.emit(text)
        comm.stop_push_window.emit()



    def createInputField(self):
        self.inputField = QtWidgets.QTextEdit(self.container)
        self.max_widget_height = 160
        self.static_yPosition = 140
        self.static_ySize = 40
        self.set_yPosition_ySize_input_field(self.static_yPosition, self.static_ySize)
        self.inputField.setPlaceholderText("Запитайте у Zefir...")
        self.inputField.setFocusPolicy(Qt.ClickFocus)
        self.inputField.setFont(QFont("Roboto", 15))  # Шрифт
        
        self.inputField.setStyleSheet("""
            QTextEdit {
                color: rgba(88, 28, 135, 180);
                background-color: transparent;
                border: 0px solid #000000;
                                       
            }
        """)
        # padding: 5px 45px 5px 10px; 
        self.inputField.setText("")
        self.inputField.textChanged.connect(self.checkIfScrollNeeded)
        self.inputField.installEventFilter(self)
        self.inputField.show()

    def eventFilter(self, obj, event):
        if obj is self.inputField:
            if event.type() == QtCore.QEvent.FocusIn:
                self.on_input_focus()
                
        return super().eventFilter(obj, event)

    def on_input_focus(self):
        comm.focus_on_push.emit()
        self.listen_command_OFF()

    @QtCore.pyqtSlot(str)
    def print_text(self, text):
        self.command = text
        self.inputField.setText(self.command)



    def checkIfScrollNeeded(self):
        text_height = self.inputField.document().size().height() + 2
        present_widget_height = self.inputField.viewport().height()

        if text_height > present_widget_height and present_widget_height < 131:
            self.static_yPosition -= 30
            self.static_ySize += 30
            self.set_yPosition_ySize_input_field(self.static_yPosition, self.static_ySize)

        elif text_height < present_widget_height:
            self.static_yPosition += 30
            self.static_ySize -= 30
            self.set_yPosition_ySize_input_field(self.static_yPosition, self.static_ySize)

        # elif present_widget_height == 160:
        #     self.static_yPosition += 10
        #     self.static_ySize -= 10
        #     self.set_yPosition_ySize_input_field(self.static_yPosition, self.static_ySize)

        # elif 131 < present_widget_height < 159: 
        #     self.static_yPosition -= 10
        #     self.static_ySize += 10
        #     self.set_yPosition_ySize_input_field(self.static_yPosition, self.static_ySize)
            # self.inputField.setGeometry(QtCore.QRect(70, 90, 410, 90))

    def set_yPosition_ySize_input_field(self, y_position, y_size):
        self.inputField.setGeometry(QtCore.QRect(70, y_position, 410, y_size))

    def position_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        final_x = self.screen_width - self.width() - 20
        final_y = self.screen_height - self.height() - 55

        self.final_pos = QPoint(final_x, final_y)
        self.start_pos = QPoint(self.screen_width, final_y)  # за межами екрана справа

        self.move(self.start_pos)  # спочатку поза екраном

    def animate_show_push(self):
        self.show()
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(200)  # тривалість анімації в мілісекундах
        self.anim.setStartValue(self.start_pos)
        self.anim.setEndValue(self.final_pos)
        self.anim.start()

    def animate_hide_push(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(200)  # тривалість анімації в мілісекундах
        self.anim.setStartValue(self.final_pos)
        self.anim.setEndValue(self.start_pos)
        self.anim.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PushWindow()
    window.show()
    sys.exit(app.exec_())
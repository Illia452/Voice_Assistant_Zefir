from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GlassToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 26)
        self.setCursor(Qt.PointingHandCursor)
        
        # Анімація для кульки
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutSine)

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def hitButton(self, pos: QPoint):
        return self.rect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        # Кольори залежно від стану
        is_checked = self.isChecked()
        bg_color = QColor(126, 34, 206, 150) if is_checked else QColor(255, 255, 255, 50)
        
        # Малюємо фон (капсула)
        p.setBrush(bg_color)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 13, 13)
        
        # Малюємо кульку
        p.setBrush(QColor("white"))
        p.drawEllipse(int(self._circle_position), 3, 20, 20)

    def nextCheckState(self):
        super().nextCheckState()
        start = 3 if not self.isChecked() else 27
        end = 27 if self.isChecked() else 3
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()
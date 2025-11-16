from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, QParallelAnimationGroup, QRect, QTimer
from PyQt5.QtGui import QFont
import sys


class Splash(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600, 400)
        self.setStyleSheet("background:#ffffff;")

        # ---------------------------------------------------
        # عنصر اللوجو الأساسي
        self.logo = QLabel("D", self)
        self.logo.setFont(QFont("Arial", 120, QFont.Bold))
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setGeometry(0, 80, 600, 180)

        self.logo_fx = QGraphicsOpacityEffect()
        self.logo.setGraphicsEffect(self.logo_fx)
        self.logo_fx.setOpacity(0)

        # ---------------------------------------------------
        # اسم البرنامج
        self.name = QLabel("Downor", self)
        self.name.setFont(QFont("Arial", 48, QFont.Bold))
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setGeometry(0, 260, 600, 80)

        self.name_fx = QGraphicsOpacityEffect()
        self.name.setGraphicsEffect(self.name_fx)
        self.name_fx.setOpacity(0)

        # ---------------------------------------------------
        QTimer.singleShot(0, self.animate)

    def animate(self):
        seq = QSequentialAnimationGroup()

        # ---------------- 1) LOGO FADE-IN -------------------
        fade_logo = QPropertyAnimation(self.logo_fx, b"opacity")
        fade_logo.setDuration(500)
        fade_logo.setStartValue(0)
        fade_logo.setEndValue(1)

        seq.addAnimation(fade_logo)

        # ---------------- 2) NAME APPEAR ---------------------
        fade_name_in = QPropertyAnimation(self.name_fx, b"opacity")
        fade_name_in.setDuration(400)
        fade_name_in.setStartValue(0)
        fade_name_in.setEndValue(1)

        slide_name_in = QPropertyAnimation(self.name, b"geometry")
        slide_name_in.setDuration(400)
        slide_name_in.setStartValue(QRect(0, 280, 600, 80))   # تحت شوية
        slide_name_in.setEndValue(QRect(0, 260, 600, 80))     # مكانه النهائي

        g1 = QParallelAnimationGroup()
        g1.addAnimation(fade_name_in)
        g1.addAnimation(slide_name_in)

        seq.addAnimation(g1)

        # ---------------- 3) NAME DISAPPEAR --------------------
        fade_name_out = QPropertyAnimation(self.name_fx, b"opacity")
        fade_name_out.setDuration(350)
        fade_name_out.setStartValue(1)
        fade_name_out.setEndValue(0)

        seq.addAnimation(fade_name_out)

        # ---------------- 4) LOGO PULSE -------------------------
        pulse_up = QPropertyAnimation(self.logo, b"geometry")
        pulse_up.setDuration(200)
        pulse_up.setStartValue(QRect(0, 80, 600, 180))
        pulse_up.setEndValue(QRect(-10, 70, 620, 200))

        pulse_down = QPropertyAnimation(self.logo, b"geometry")
        pulse_down.setDuration(200)
        pulse_down.setStartValue(QRect(-10, 70, 620, 200))
        pulse_down.setEndValue(QRect(0, 80, 600, 180))

        g2 = QSequentialAnimationGroup()
        g2.addAnimation(pulse_up)
        g2.addAnimation(pulse_down)

        seq.addAnimation(g2)

        seq.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Splash()
    w.show()
    sys.exit(app.exec_())

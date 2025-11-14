from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer, QRect, QEasingCurve
from PyQt5.QtGui import QPixmap
import sys

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: white;")
        self.init_ui()
        
    def init_ui(self):
        # اللوجو الأساسي
        self.logo = QLabel(self)
        self.logo_pixmap = QPixmap("97708b54-9248-4adf-8004-5a3ea44b9b49.png")  # ضع هنا مسار صورة اللوجو الأساسي
        self.logo.setPixmap(self.logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setGeometry(200, 100, 200, 200)
        
        # اسم البرنامج كصورة
        self.name_img = QLabel(self)
        self.name_pixmap = QPixmap("95b6597a-90bb-479f-8c33-b2320438d159.png")  # ضع هنا مسار صورة الاسم
        self.name_img.setPixmap(self.name_pixmap.scaled(300, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.name_img.setAlignment(Qt.AlignCenter)
        self.name_img.setGeometry(150, 220, 300, 60)
        self.name_img.setVisible(False)
        
        self.animate()

    def animate(self):
        # تأخير بسيط قبل ظهور الاسم
        def show_name():
            self.name_img.setVisible(True)
            anim = QPropertyAnimation(self.name_img, b"geometry")
            anim.setDuration(800)
            anim.setStartValue(QRect(250, 220, 0, 60))
            anim.setEndValue(QRect(150, 220, 300, 60))
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.start()
            
            # بعد الانتهاء، يختفي الاسم تدريجيًا
            anim.finished.connect(hide_name)

        def hide_name():
            fade = QPropertyAnimation(self.name_img, b"windowOpacity")
            fade.setDuration(500)
            fade.setStartValue(1)
            fade.setEndValue(0)
            fade.start()

        QTimer.singleShot(500, show_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())

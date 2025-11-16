# This is an Animation Screen

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt5.QtGui import QPixmap, QImage
import sys


def remove_white_background(pixmap, tolerance=30):
    """إزالة الخلفية البيضاء من صورة وجعلها شفافة"""
    img = pixmap.toImage()
    # تحويل الصورة إلى ARGB لتدعم الشفافية
    img = img.convertToFormat(QImage.Format_ARGB32)

    for y in range(img.height()):
        for x in range(img.width()):
            color = img.pixelColor(x, y)
            # تحقق إذا كان اللون قريب من الأبيض
            if (
                color.red() > 255 - tolerance
                and color.green() > 255 - tolerance
                and color.blue() > 255 - tolerance
            ):
                # اجعله شفاف
                img.setPixelColor(x, y, Qt.transparent)

    return QPixmap.fromImage(img)


class SplashScreen(QWidget):
    def __init__(self, parent : QWidget ):
        super().__init__(parent=parent)
        self.anim = None
        self.anim1 = None  # احفظ الـ animation
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(900, 500)
        self.setGeometry(0,0,900,500)
        self.setWindowTitle("Splash Screen")

        self.logo_label = QLabel(self)
        self.logo_label.setAlignment(Qt.AlignCenter)

        Our_logo = QPixmap("tabs\Our_Logo.png")
        main_logo = QPixmap("tabs\second_log.png")
        if not main_logo or main_logo.isNull():
            # صورة غير موجودة - نعرض نص بديل
            self.main_logo_label = QLabel("Logo not found: second_log.png", self)
            self.main_logo_label.setStyleSheet("color: #666; font-size: 18px;")
            self.main_logo_label.setAlignment(Qt.AlignCenter)
            self.main_logo_label.setGeometry(150, 250, 300, 100)
        else:
            self.main_logo_label = QLabel(self)
            self.main_logo_label.setAlignment(Qt.AlignCenter)
            scaled_main = main_logo.scaled(
                300, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.main_logo_label.setPixmap(scaled_main)
            self.main_logo_label.setGeometry(140, 120, 280, 110)
            self.main_logo_label.setVisible(False)
            QTimer.singleShot(2700, self.animation_part2)
        # إزالة الخلفية البيضاء من الصور
        if not Our_logo.isNull():
            Our_logo = remove_white_background(Our_logo)
        if not main_logo.isNull():
            main_logo = remove_white_background(main_logo)
        if not Our_logo or Our_logo.isNull():
            # صورة غير موجودة - نعرض نص بديل
            self.logo_label.setText("Logo not found: Our_Logo.png")
            self.logo_label.setStyleSheet("color: #666; font-size: 18px;")
            self.logo_label.setGeometry(300, 150, 200, 100)
        else:
            # نجعل الصورة تتناسب مع المساحة مع الحفاظ على النسبة
            scaled = Our_logo.scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled)
            # ابدأ من أسفل
            self.logo_label.setGeometry(390, 180, 120, 120)
            QTimer.singleShot(700, self.animation_part1)
    def animation_part1(self):
        # # إنشاء الـ animation
        self.anim = QPropertyAnimation(self.logo_label, b"geometry")
        self.anim.setDuration(2000)  # ميلي ثانية
        self.anim.setStartValue(QRect(390, 180, 120, 120))  # من الأسفل
        self.anim.setEndValue(QRect(260, 180, 120, 120))  # للأعلى
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()




    def animation_part2(self):
        self.main_logo_label.setVisible(True)
        self.anim1 = QPropertyAnimation(self.main_logo_label, b"geometry")
        self.anim1.setDuration(2000)
        self.anim1.setStartValue(QRect(700, 185, 300, 110))
        self.anim1.setEndValue(QRect(350, 185, 300, 110))
        self.anim1.setEasingCurve(QEasingCurve.OutBounce)
        self.anim1.start()


if __name__ == "__main__":
    import Downloader_manager

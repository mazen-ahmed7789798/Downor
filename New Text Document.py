from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt5.QtGui import QColor
import sys


class Loader(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600, 150)
        self.setStyleSheet("background: white;")

        # ---------------------------------------------
        # الشريط الخلفي (ثابت)
        self.bar = QLabel(self)
        self.bar.setGeometry(100, 60, 400, 20)
        self.bar.setStyleSheet(f"""
            background: #e0e0e0;
            border-radius: 10px;
        """)

        # ---------------------------------------------
        # البلوك المتحرك (عرضه = نص الشريط)
        block_width = 200  # نص 400

        self.block = QLabel(self)
        self.block.setGeometry(100, 60, block_width, 20)
        self.block.setStyleSheet("""
            background: #1e88e5;
            border-radius: 10px;
        """)

        # ---------------------------------------------
        # نبدأ الأنيميشن بعد أول ربع ثانية
        QTimer.singleShot(150, self.start_animation)

    def start_animation(self):

        block_width = self.block.width()
        bar_x = self.bar.x()
        bar_width = self.bar.width()

        start_x = bar_x
        end_x = bar_x + (bar_width - block_width)

        # ---------------------------------------------
        # أنيميشن رايح
        self.anim_forward = QPropertyAnimation(self.block, b"geometry")
        self.anim_forward.setDuration(1000)
        self.anim_forward.setStartValue(QRect(start_x, 60, block_width, 20))
        self.anim_forward.setEndValue(QRect(end_x, 60, block_width, 20))
        self.anim_forward.setEasingCurve(QEasingCurve.InOutQuad)

        # ---------------------------------------------
        # أنيميشن جاي
        self.anim_backward = QPropertyAnimation(self.block, b"geometry")
        self.anim_backward.setDuration(1000)
        self.anim_backward.setStartValue(QRect(end_x, 60, block_width, 20))
        self.anim_backward.setEndValue(QRect(start_x, 60, block_width, 20))
        self.anim_backward.setEasingCurve(QEasingCurve.InOutQuad)

        # ---------------------------------------------
        # نربطهم ببعض… أول ما الأولى تخلص يبدأ التانية
        self.anim_forward.finished.connect(self.anim_backward.start)
        self.anim_backward.finished.connect(self.anim_forward.start)

        # نبدأها أول مرة
        self.anim_forward.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Loader()
    w.show()
    sys.exit(app.exec_())

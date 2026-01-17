import os
import sys
from subprocess import run

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QScrollArea,
    QLabel

    # مسار الملف الرئيسي (عدّل المسار حسب مكانه الحقيقي)
)
from PyQt5.QtCore import QPropertyAnimation, QRect, QSize,QEasingCurve
from PyQt5.QtGui import QIcon,QFont

main_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Downor.py")
)

# لو الملف الحالي مش هو الملف الرئيسي
if os.path.basename(sys.argv[0]) != "Downor.py":

    run([sys.executable, main_path])
    sys.exit()

app = QApplication([])

Home_tab = QWidget()





new_btn = QPushButton("+", Home_tab)
new_btn.setBaseSize(QSize(50, 50))
new_btn.setObjectName("new-btn")
new_btn.setGeometry(+755, 350, 60, 60)
new_btn.setToolTip("New Download")
new_btn.raise_()


video_btn = QPushButton(icon=QIcon("Assests\\VideoIcon.png"), parent=Home_tab)
video_btn.setObjectName("new-btn")
video_btn.setGeometry(+755, 285, 60, 60)
video_btn.setIconSize(QSize(20, 20))
video_btn.setToolTip("Download Video")
video_btn.hide()

playlist_btn = QPushButton(icon=QIcon("Assests\\playlistIcon.png"), parent=Home_tab)
playlist_btn.setObjectName("new-btn")
playlist_btn.setGeometry(+755, 285, 60, 60)
playlist_btn.setIconSize(QSize(20, 20))
playlist_btn.setToolTip("Download Playlist")
playlist_btn.hide()

AudioBtn = QPushButton(icon=QIcon("Assests\\micIcon.png"), parent=Home_tab)
AudioBtn.setObjectName("new-btn")
AudioBtn.setGeometry(+755, 285, 60, 60)
AudioBtn.setIconSize(QSize(20, 20))
AudioBtn.setToolTip("Download Audio")
AudioBtn.hide()

anims = []
c = False
def show_btns (targets :list, duration ,start : QRect, end : QRect ) :
    global c
    if c == False :
        for i , a in zip(targets,end) :
            anim = QPropertyAnimation(i, b"geometry")
            anim.setDuration(duration)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setStartValue(start)
            anim.setEndValue(a)
            anims.append(anim)
            anim.start()
            i.show()
            c = True 
    else :
        for i , a in zip(targets,end) :
            anim = QPropertyAnimation(i, b"geometry")
            anim.setDuration(duration)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setStartValue(a)
            anim.setEndValue(start)
            anims.append(anim)
            anim.start()
            anim.finished.connect(i.hide)
            c = False

new_btn.clicked.connect(lambda _ :show_btns(
 [video_btn
 ,playlist_btn
 ,AudioBtn]
 ,300,
 QRect(+755, 350, 60, 60)
,[QRect(+755, 285, 60, 60)
,QRect(755,220,60,60)
,QRect(755,155,60,60)]))




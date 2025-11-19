from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTabWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
)

from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import QTimer, QSize
from tabs.Home import Home_tab
from tabs.SplaSh import SplashScreen
app = QApplication([])
with open("stylesheet.qss", "r") as r:
    app.setStyleSheet(r.read())

window = QWidget()
window.setGeometry(150, 150, 900, 500)
window.setMinimumSize(310, 400)
window.setWindowTitle("Downor")
window.setWindowIcon(QIcon("tabs\\Our_Logo.png"))
layout = QVBoxLayout()
layout.setContentsMargins(0, 0, 0, 0)  # يلغى الـ margin
layout.setSpacing(0)

tab_widget = QTabWidget(window)
tab_widget.setVisible(False)
tab_widget.setGeometry(0, 2, window.width(), window.height())
tab_widget.setMovable(True)
tab_widget.setIconSize(QSize(25, 15))
protected_tabs = []


def make_close_button(index, deletable):
    btn = QPushButton(parent=tab_widget,icon=QIcon("Assests\\cross.png"))
    btn.setFixedSize(5, 5)
    btn.setObjectName("close-tab-button")
    btn.setToolTip("Close Tab")

    if deletable:
        btn.clicked.connect(lambda _, i=index: tabs.removeTab(i))
    else:
        pass
    return btn


def add_custom_tab(widget, title, deletable=True):
    index = tab_widget.addTab(widget, title)
    if not deletable:
        protected_tabs.append(index)
    tab_widget.tabBar().setTabButton(
        index, tab_widget.tabBar().RightSide, make_close_button(index, deletable)
    )


add_custom_tab(Home_tab, "Home", False)
tab_widget.setTabIcon(
    0,
    QIcon(
        "Assests\\HomeIcon.png",
    ),
)

splash_screen = SplashScreen(window)

def show_main():
    splash_screen.deleteLater()
    tab_widget.setVisible(True)


QTimer.singleShot(6000, show_main)
layout.addWidget(tab_widget)
window.setLayout(layout)

window.show()

app.exec_()

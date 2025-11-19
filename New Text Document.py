from tabs.SplaSh import SplashScreen
from PyQt5.QtWidgets import QApplication, QWidget
app = QApplication([])
win = QWidget()
s = SplashScreen(win)
print("has bar:", hasattr(s, "bar"))
print("bar geometry:", s.bar.geometry().getRect())
print("block geometry:", s.block.geometry().getRect())
print("bar visible:", s.bar.isVisible())
win.show()
app.exec_()
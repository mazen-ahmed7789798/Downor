from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtCore import Qt
import sys

app = QApplication(sys.argv)

# النافذة الرئيسية
window = QWidget()
window.setWindowTitle("Tabs Example")
window.resize(700, 500)

main_layout = QVBoxLayout(window)

# عنصر التابات
tabs = QTabWidget()
tabs.setTabsClosable(True)  # اجعل التابات قابلة للإغلاق
tabs.tabCloseRequested.connect(lambda index: tabs.removeTab(index))

# تاب ثابت (Home)
home_tab = QWidget()
home_layout = QVBoxLayout(home_tab)
home_layout.addWidget(QLabel("محتوى التاب الرئيسي (Home)"))
tabs.addTab(home_tab, "Home")

# تاب يحتوي على ScrollArea (مثال لصفحة طويلة)
scroll_tab = QWidget()
scroll_layout = QVBoxLayout(scroll_tab)
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
content = QWidget()
content_layout = QVBoxLayout(content)
for i in range(30):
    content_layout.addWidget(QLabel(f"سطر محتوى {i+1}"))
scroll_area.setWidget(content)
scroll_layout.addWidget(scroll_area)
tabs.addTab(scroll_tab, "Scrollable")

main_layout.addWidget(tabs)

# زر لإضافة تاب جديد ديناميكيًا
def add_new_tab():
    new_tab = QWidget()
    layout = QVBoxLayout(new_tab)
    layout.addWidget(QLabel(f"تاب جديد رقم {tabs.count()+1}"))
    tabs.addTab(new_tab, f"Tab {tabs.count()+1}")
    tabs.setCurrentWidget(new_tab)  # انتقل للتاب الجديد فورًا

add_btn = QPushButton("Add New Tab")
add_btn.clicked.connect(add_new_tab)
main_layout.addWidget(add_btn)

window.show()
sys.exit(app.exec_())
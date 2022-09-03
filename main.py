import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel('Hello Word!')
label.show()
app.exec_()

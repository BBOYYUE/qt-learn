import sys
from PySide6.QtWidgets import QApplication, QWidget
from myUiLearn import MyUiLearn

class MyWidgetLearn (QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        ui = MyUiLearn()
        ui.setupUi(self)
        ui.button.setText("close")
        ui.button.clicked.connect(self.close)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWidgetLearn()
    myWindow.show()
    sys.exit(app.exec())

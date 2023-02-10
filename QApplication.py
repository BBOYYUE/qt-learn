import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class QApplicationLearn(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi()
        self.button.clicked.connect(self.bellAlert)
    
    def setupUi(self):
        self.setWindowTitle('Hello')
        self.resize(300, 150)

        self.label = QLabel(self)
        self.label.setText('Welcome sollad')
        self.label.setGeometry(80, 50, 150, 20)
        
        self.button = QPushButton(self)
        self.button.setText('alert')
        self.button.setGeometry(90, 100,100, 20)

    def bellAlert(self):
        try:
            QApplication.beep()
            QApplication.alert(win, duration=0)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationDisplayName('welcome')
    app.setEffectEnabled(Qt.UI_AnimateCombo)
    # app.setWindowIcon(QPixmap())
    win = QWidget()
    win.show()
    myWindow = QApplicationLearn()
    myWindow.show()
    sys.exit(app.exec())

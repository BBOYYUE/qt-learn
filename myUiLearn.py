from PySide6.QtWidgets import QLabel,QPushButton

class MyUiLearn(object):
    def setupUi(self, window):
        window.setWindowTitle('Sollado')
        window.resize(300, 150)

        self.label = QLabel(window)
        self.label.setText('Welcome Sollado')
        self.label.setGeometry(80, 50, 150, 20)

        self.button = QPushButton(window)
        self.button.setText('close')
        self.button.setGeometry(120, 100, 50, 20)
import sys
from PySide6.QtWidgets import QApplication,QWidget,QLabel,QPushButton

app = QApplication(sys.argv)
myWindow = QWidget()
myWindow.setWindowTitle('sollado')
myWindow.resize(300,150)

myLabel = QLabel(myWindow)
string = 'Welcome Sollado'
myLabel.setText(string)
myLabel.setGeometry(80,50,150,20)

myButton = QPushButton(myWindow)
myButton.setText('close')

myButton.setGeometry(120,100,50,20)
myButton.clicked.connect(myWindow.close)

myWindow.show()
n = app.exec()
print(n)
try:
    sys.exit(n)
except SystemExit:
    print('closeing')
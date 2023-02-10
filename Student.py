import sys
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog
from PySide6.QtCore import Slot, Signal
from ui.StudentUi import Ui_Student
from subprocess import Popen
import os


class Student(QWidget):
    uuidSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Student()
        self.ui.setupUi(self)
        self.__count = 0
        self.__score = list()
        self.__student = dict()
        self.fileDiaLog = QFileDialog(self)
        
        self.uuidSignal.connect(self.is_uuid_existing)

    
    @Slot()
    def     on_pushButtonCalculation_clicked(self):
        s = self.ui.spinBoxLanguage.value() + self.ui.spinBoxMath.value() + \
            self.ui.spinBoxEnglish.value()
        self.ui.spinBoxTotal.setValue(int(s))
        template = "{:.1f}".format(s/3)
        self.ui.doubleSpinBoxAverage.setValue(float(template))
        self.__count = self.__count + 1

        temp = list()
        temp.append(self.__count)
        temp.append(self.ui.lineEditName.text())
        temp.append(self.ui.lineEditUuid.text())
        temp.append(self.ui.spinBoxLanguage.value())
        temp.append(self.ui.spinBoxMath.value())
        temp.append(self.ui.spinBoxEnglish.value())
        temp.append(s)
        temp.append(float(template))
        self.__score.append(temp)
        self.__student[self.ui.lineEditUuid.text()] = temp

    @Slot()
    def on_pushButtonSave_clicked(self):
        # template = "{}: 语文{} 数学{} 总成绩{} 平均分{}\n"
        template = "{}: 姓名{} 学号{} 语文{} 数学{} 总成绩{} 平均分{}\n"
        # self.fileDiaLog.setFileMode(QFileDialog.FileMode.Directory)
        # name,fil = self.fileDiaLog.getSaveFileName(self, "save as ...", os.path.expanduser('~'), '')
        filePath = self.fileDiaLog.getExistingDirectory()
        try:
            fp = open(filePath + os.path.sep +
                      "成绩.txt", "w", encoding='UTF-8')
        except Exception as e:
            QMessageBox.information(self, "失败信息", "保存失败" + str(e))
        else:
            for i in self.__student.values():
                score = template.format(
                    i[0], i[1], i[2], i[3], i[4], i[5], i[6])
                fp.write(score)

            fp.close()
            QMessageBox.information(self, "成功信息", "保存成功, 文件路径为\n" + filePath + os.path.sep +
                                    "成绩.txt")

    @Slot()
    def on_lineEditUuid_editingFinished(self):
        self.uuidSignal.emit(self.ui.lineEditUuid.text())


    def bell_alert(self):
        try:
            QApplication.beep()
            QApplication.alert(myWindow, duration=0)
        except Exception as e:
            print(e)

    def is_uuid_existing(self, value):
        if value in self.__student:
            self.bell_alert()
            existing = QMessageBox.question(
                self, "确认信息", "该学号已经存在,是否覆盖?", QMessageBox.Yes | QMessageBox.No)
            if existing == QMessageBox.No:
                self.ui.lineEditUuid.setText('')
                self.ui.lineEditUuid.setFocus()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Popen('./Information')
    myWindow = Student()
    myWindow.show()
    sys.exit(app.exec())

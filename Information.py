import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog, QMenuBar
from PySide6.QtCore import Slot, Signal, QStringListModel
from ui.StudentUi import Ui_Student
from ui.InformationUi import Ui_MainWindow
from subprocess import Popen, call
import os
import oss2
import sqlite3



"""
这里为了便于不懂QT的人能比较方便的阅读代码， 记录一些QT的约定

1. @Slot 修饰函数表示这个类方法是组件信号触发后的回调， 回调函数的命名用下划线做分割。第一个单词是信号的类型， 第二个单词是这个信号绑定的组件的名称， 第三个单词表示信号的名称。 这里组件名称如果是多个单词就可能会出现类函数命名 驼峰蛇形混写的问题， 这是不得已的， 不要介意。
2. connect 方法总是用来信号和回调函数的绑定， 信号有内置信号，菜单选项按钮动作信号，自定义信号等。 
"""

class Information(QMainWindow):
    uuidSignal = Signal(str)
    dbName = "information.db"
    auth = oss2.Auth('yourAccessKeyId', 'yourAccessKeySecret')
    bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'examplebucket')

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.__count = 0
        self.__student = dict()
        self.__infomationList = QStringListModel(self)
        self.__fileDiaLog = QFileDialog(self)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("文件(&F)")
        actionSaveAs = fileMenu.addAction("另存为...")

        helpMenu = menubar.addMenu("帮助(&H)")
        activeInfo = helpMenu.addAction("关于...")


        self.ui.listView.setModel(self.__infomationList)
        self.uuidSignal.connect(self.is_uuid_existing)
        actionSaveAs.triggered.connect(self.action_saveAs_triggered)
        activeInfo.triggered.connect(self.active_info_triggered)
    
    
    @Slot()
    def on_pushButtonCalculation_clicked(self):
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
        self.__student[self.ui.lineEditUuid.text()] = temp
        self.update_informationList()


    @Slot()
    def on_pushButtonNext_clicked(self):
        self.ui.lineEditName.setText('')
        self.ui.lineEditUuid.setText('')
        self.ui.spinBoxLanguage.setValue(0)
        self.ui.spinBoxMath.setValue(0)
        self.ui.spinBoxEnglish.setValue(0)
        self.ui.spinBoxTotal.setValue(0)
        self.ui.doubleSpinBoxAverage.setValue(0.00)

    @Slot()
    def on_lineEditUuid_editingFinished(self):
        self.uuidSignal.emit(self.ui.lineEditUuid.text())


    """
    菜单按钮的信号回调
    """
    def action_saveAs_triggered(self):
        template = "{}: 姓名{} 学号{} 语文{} 数学{} 总成绩{} 平均分{}\n"
        filePath = self.__fileDiaLog.getExistingDirectory()
        if not filePath:
            return 
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

    def active_info_triggered(self):
        QMessageBox.information(self, "关于", "成绩统计1.0版本\n有问题请发送邮件到 bboyxiaoyue@outlook.com\n")




    """
    自定义信号
    """
    def is_uuid_existing(self, value):
        if value in self.__student:
            self.bell_alert()
            existing = QMessageBox.question(
                self, "确认信息", "该学号已经存在,是否覆盖?", QMessageBox.Yes | QMessageBox.No)
            if existing == QMessageBox.No:
                self.ui.lineEditUuid.setText('')
                self.ui.lineEditUuid.setFocus()



    """
    oss 断点上传 下传进度条相关

    代码是直接搬的 oss sdk的示例
    """
    def percentage(consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print('\r{0}% '.format(rate), end='')
            sys.stdout.flush()

    def resumable_download(self, source):
        target = self.__fileDiaLog.getExistingDirectory()
        if not target:
            return 
        oss2.resumable_download(self.bucket, source, target,
                    #   store=oss2.ResumableDownloadStore(root='/tmp'),
                    # 指定当文件长度大于或等于可选参数multipart_threshold（默认值为10 MB, 这里是 100MB）时，则使用断点续传下载。
                      multiget_threshold=100*1000*1024,
                    # 设置分片大小，单位为字节，取值范围为100 KB~5 GB。默认值为100 KB。 这里是 10MB
                      part_size=10*1000*1024,
                    # 设置下载进度回调函数。
                      progress_callback=self.percentage,
                    # 如果使用num_threads设置并发下载线程数，请将oss2.defaults.connection_pool_size设置为大于或等于并发下载线程数。默认并发下载线程数为1。
                      num_threads=4)

    def resumable_upload(self, target):
        source = self.__fileDiaLog.getOpenFileName()
        if not source:
            return 
        oss2.resumable_upload(self.bucket, target, source,
                    #   store=oss2.ResumableStore(root='/tmp'),
                      # 指定当文件长度大于或等于可选参数multipart_threshold（默认值为10 MB）时，则使用分片上传。
                      multipart_threshold=100*1024,
                      # 设置分片大小，单位为字节，取值范围为100 KB~5 GB。默认值为100 KB。
                      part_size=100*1024,
                      # 设置上传回调进度函数。
                      progress_callback=self.percentage,
                      # 如果使用num_threads设置并发上传线程数，请将oss2.defaults.connection_pool_size设置为大于或等于并发上传线程数。默认并发上传线程数为1。
                      num_threads=4)

    
    """
    窗口的一些工具方法
    """
    def bell_alert(self):
        try:
            QApplication.beep()
            QApplication.alert(myWindow, duration=0)
        except Exception as e:
            print(e)

    """
    窗口的业务逻辑
    """
    def update_informationList(self):
        template = "{}: 姓名{} 学号{} 语文{} 数学{} 总成绩{} 平均分{}"
        student = list()

        for i in self.__student.values():
            s = template.format(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
            student.append(s)
        
        self.__infomationList.setStringList(student)
        # save Information
        self.save_informationList(student)

    # def save_informationList(self):
          


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Information()
    myWindow.show()

    sys.exit(app.exec())


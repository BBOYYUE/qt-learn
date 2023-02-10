from PySide6.QtCore import Signal, QThread

class WorkThreadUtil(QThread):   # 创建多个任务可以建多个 WorkThread(QThread) 后面启动
    timer = Signal(str)  # 每隔1秒发送一次信号   str:可以传递参数
    end = Signal(str)  # 计数完成后发送一次信号
    sec = 0
    def run(self):
        while True:
            self.sleep(1)  # 休眠1秒
            if self.sec == 5:
                self.end.emit(str(self.sec))  # 发送end信号  str:可以传递参数
                break
            self.timer.emit(str(self.sec))  # 发送timer信号  str:可以传递参数
import sys
from PySide6.QtWidgets import QApplication, QWizard, QFileDialog, QProgressDialog
from ui.InitializeBootUi import Ui_Wizard
from PySide6.QtCore import Slot, Qt, QTimer
from auth.Certificate import CertificateVaild
from download.DownloadAsset import DownloadAsset
import asyncio
import sqlite3
from os import path

class InitializeBoot(QWizard):

    # 当前页的下一步按钮是否可点的状态
    isCompleteState = False

    # 是否已同意免责条款
    argeeDisclaimer = False
   
    # 设备注册是否成功
    registerSuccess = False
    # 是否已经下载成功
    downloadSuccess = False
    # 
    downloading = False

    __assetInfo = dict()
    __filePath = ''
    __assetPath = ''
    __zipPath = ''

    

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Wizard()
        self.ui.setupUi(self)

        self.init_welcome_page()
        self.init_selectFilePath_page()
        self.init_registerCode_page()
        self.init_download_page()
        self.__fileDiaLog = QFileDialog(self)

        self.download = DownloadAsset()
        self.dbname = path.abspath(path.join(path.dirname(__file__), 'data.db'))
 
    def init_welcome_page(self):
        self.ui.wizardPageWelcome.isComplete = self.isComplete
    
    def init_selectFilePath_page(self):
        self.ui.wizardPageSelectFilePath.isComplete = self.isComplete

    def init_registerCode_page(self):
        self.ui.wizardPageRegisterCode.isComplete = self.isComplete
    
    def init_download_page(self):
        self.ui.wizardPageDownload.isComplete = self.isComplete
    
    # 返回下一步按钮是否可以点击
    def isComplete(self):
        return self.isCompleteState


    @Slot()
    def on_checkBox_stateChanged(self):
        # checkBox 是我同意勾选框, 根据状态的不同修改 下一步按钮的状态
        if(self.ui.checkBox.checkState() == Qt.CheckState.Checked):
            self.argeeDisclaimer = True
            # 修改下一步按钮的状态后, 需要触发当前引导页的 completeChanged 时间
            self.isCompleteState = True
            self.ui.wizardPageWelcome.completeChanged.emit()
            self.isCompleteState = False
        else:
            self.isCompleteState = False
            self.ui.wizardPageWelcome.completeChanged.emit()
    
    @Slot()
    def on_pushButton_clicked(self):
        filePath = str.strip(self.__fileDiaLog.getExistingDirectory())
        if not filePath:
            return 
        else:
            # 选中路径之后, 需要把路径设置到 文本输入框, 并且修改下一步按钮的状态
            self.ui.lineEdit.setText(filePath)
            self.__filePath = filePath
            self.isCompleteState = True
            self.ui.wizardPageSelectFilePath.completeChanged.emit()
            self.isCompleteState = False

    @Slot()
    def on_pushButton_2_clicked(self):
        # TODO show progress bar
        self.ui.pushButton_2.setText('正在激活中!')
        self.ui.pushButton_2.setEnabled(False)

        self.__code = str.strip(self.ui.lineEdit_2.text())
        asyncio.run(self.asyncio_register_hardware())


    @Slot()
    def on_Wizard_currentIdChanged(self):
        if (self.currentPage() == self.ui.wizardPageDownload and self.downloadSuccess == False and self.downloading == False):
            asyncio.run(self.asyncio_download_asset())
        self.check_next_bottom_state()

    def check_next_bottom_state(self):
        if(self.currentPage() == self.ui.wizardPageWelcome and self.argeeDisclaimer):
            self.isCompleteState = True
            self.ui.wizardPageWelcome.completeChanged.emit()
            self.isCompleteState = False
        elif (self.currentPage() == self.ui.wizardPageSelectFilePath and self.__filePath):
            self.isCompleteState = True
            self.ui.wizardPageSelectFilePath.completeChanged.emit()
            self.isCompleteState = False
        elif (self.currentPage() == self.ui.wizardPageRegisterCode and self.registerSuccess):
            self.isCompleteState = True
            self.ui.wizardPageRegisterCode.completeChanged.emit()
            self.isCompleteState = False
        elif (self.currentPage() == self.ui.wizardPageDownload and self.downloadSuccess):
            self.isCompleteState = True
            self.ui.wizardPageDownload.completeChanged.emit()
            self.isCompleteState = False

    async def asyncio_download_asset(self):
        await self.download_asset()

    def re_download_asset(self):
        if self.downloading == False:
            asyncio.run(self.download_asset())

    async def download_asset(self):
        self.downloading = True
        self.__assetInfo = self.download.set_asset_by_code(self.__code)
        self.__zipPath = self.download.resumable_download(self.__filePath, self.download_proccess)
        self.ui.pushButton_3.setText('正在下载...')
        if self.__zipPath == False:
            msg = dict()
            msg['code'] = '400'
            msg['state'] = "error"
            msg['msg'] = "下载失败! "
            msg['poccess'] = 0
            self.download_proccess(msg)
            self.ui.pushButton_3.setText('点击重试')
            self.ui.pushButton_3.clicked.connect(self.re_download_asset)
            self.downloading = False

        self.download.unzip_asset()
        self.save_config()
        self.ui.pushButton_3.setText('下载完成!')
        
  
        
    async def asyncio_register_hardware(self):
        await self.register_hardware()

    async def register_hardware(self):
        vaild = CertificateVaild()
        self.pd = QProgressDialog('激活进度', '取消', 0, 100, self)
        self.pd.setLabelText('正在激活中...')
        self.pd.setAutoClose(True)
        self.pd.setMinimumDuration(0)
        self.pd.show()
        vaild.set_asset_path(self.__filePath)

        if (vaild.check_hardware_valid() == False):
            self.__cpuid = vaild.register(self.__code, self.register_proccess)
            if(self.__cpuid == False):
                self.pd.cancel()
                self.ui.pushButton_2.setText('激活失败!')
            else:
                self.register_hardware_success()

        else:
            self.pd.setValue(100)
            self.register_hardware_success()
    
    def install_asset_success(self):
        self.isCompleteState = True
        self.downloadSuccess = True
        self.ui.wizardPageDownload.completeChanged.emit()
        self.isCompleteState = False

    def register_hardware_success(self):
        self.isCompleteState = True
        self.registerSuccess = True
        self.ui.wizardPageRegisterCode.completeChanged.emit()
        self.isCompleteState = False
        self.ui.pushButton_2.setText('激活成功!')

    def download_proccess(self, data):
        if(int(data.get('poccess')) == 80):
            self.ui.progressBar.setValue(data.get('poccess'))
            text = self.ui.textBrowser.toPlainText()
            self.ui.textBrowser.setText(text + "\n下载完成!"+"\n开始解压...")
        elif(int(data.get('poccess')) == 90):
            self.ui.progressBar.setValue(data.get('poccess'))
            text = self.ui.textBrowser.toPlainText()
            self.ui.textBrowser.setText(text + "\n解压完成!"+"\n开始保存程序配置...")
        elif(int(data.get('poccess')) == 100):
            self.ui.progressBar.setValue(data.get('poccess'))
            text = self.ui.textBrowser.toPlainText()
            self.ui.textBrowser.setText(text + "\n保存成功!"+"\n安装成功!")
            self.install_asset_success()
        else:
            self.ui.progressBar.setValue(data.get('poccess'))
            text = self.ui.textBrowser.toPlainText()
            if data.get('msg') != '':
                self.ui.textBrowser.setText(text + "\n" + data.get('msg'))

    def register_proccess(self, data):
        self.pd.setToolTip(data.get('msg'))
        self.pd.setValue(data.get('poccess'))
    
    def save_config(self):
        try:
            con = sqlite3.connect(self.dbname)
            cur = con.cursor()
            try:
                cur.execute('''
                    DROP TABLE projects;
                ''')
            except:
                print('projects 表不存在')

            cur.execute('''
                CREATE TABLE projects (
                    id INTEGER,
                    name TEXT,
                    address TEXT,
                    phone TEXT,
                    slogan TEXT,
                    code TEXT
                )
            ''')
            sqlInsertProject = "INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)" 
            dataInsertProject = (
                1, 
                self.__assetInfo['name'], 
                self.__assetInfo['address'], 
                self.__assetInfo['phone'], 
                self.__assetInfo['slogan'], 
                self.__code
                )
            print(sqlInsertProject, dataInsertProject)
            cur.execute(sqlInsertProject, dataInsertProject)
            try:
                cur.execute('''
                    DROP TABLE products;
                ''')
            except:
                print('products 表不存在')

            cur.execute('''
                CREATE TABLE products (
                    id INTEGER,
                    name TEXT,
                    assetpath TEXT,
                    zippath TEXT,
                    info TEXT,
                    version TEXT,
                    projectid INTEGER,
                    isvaild INTEGER,
                    createdat TEXT
                )
            ''')
            sqlInsertProduct = "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)" 
            self.__assetPath = self.__filePath + '/' + self.__assetInfo['products'][0]['hash_id']
            dataInsertProduct = (
                1, 
                self.__assetInfo['products'][0]['name'], 
                self.__assetPath, 
                self.__zipPath, 
                self.__assetInfo['products'][0]['info'], 
                self.__assetInfo['products'][0]['hash_id'],
                1,
                1,
                self.__assetInfo['products'][0]['created_at']
                )
            print(sqlInsertProduct, dataInsertProduct)
            cur.execute(sqlInsertProduct, dataInsertProduct)
            try:
                cur.execute('''
                    DROP TABLE configs;
                ''')
            except:
                print('configs 表不存在')
                
            cur.execute('''
                CREATE TABLE configs (
                    id INTEGER,
                    cpuid TEXT,
                    filepath TEXT,
                    times INTEGER
                )
            ''')
            dataInsertConfig = (
                1,
                self.__cpuid,
                self.__filePath,
                30
            )
            sqlInsertConfit = "INSERT INTO configs VALUES (?, ?, ?, ?)"
            print(sqlInsertConfit, dataInsertConfig)
            cur.execute(sqlInsertConfit, dataInsertConfig)

            con.commit()
            con.close()
            msg = dict()
            msg['code'] = '200'
            msg['state'] = "successed"
            msg['msg'] = ""
            msg['poccess'] = 100
            self.download_proccess(msg)
        except Exception as e:
            print(e)
            msg = dict()
            msg['code'] = '400'
            msg['state'] = "error"
            msg['msg'] = e
            msg['poccess'] = 90
            self.download_proccess(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = InitializeBoot()
    myWindow.show()
    sys.exit(app.exec())
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QProgressDialog
from PySide6.QtCore import Slot, Signal, QStringListModel
from PySide6.QtGui import QPixmap
import sys
from ui.UploadProductUi import Ui_MainWindow
import asyncio
import requests
from util.NetworkUtil import NetworkUtil
from os import path
import oss2

class UploadProduct(QMainWindow):

    auth = oss2.Auth('LTAI5tGzTWyXiajVYViDUWgs', 's42GqptOYVUU1wVeURsRTYEEqBfR3y')
    bucket = oss2.Bucket(auth, endpoint='http://oss-cn-zhangjiakou.aliyuncs.com', bucket_name='alpha-serve')

    __projectList = []
    __filePath = ""
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.networkUtil = NetworkUtil()
        self.init_home()
        self.ui.comboBox_2.addItems(('未定义','ue4','web','unity'))
        self.__fileDiaLog = QFileDialog(self)

    def init_home(self):
        asyncio.run(self.async_init_home())
    
    async def async_init_home(self):
        await self.get_project_list()
        await self.set_project_list()

    async def get_project_list(self):
        response = requests.get('http://dev-cn.laravel.com/api/v1/project')
        json = self.networkUtil.checkResponse(response)
        self.__projectList = json['data']['data']
    
    async def set_project_list(self):
        data = ['未选中']
        for project in self.__projectList:
            data.append(project['name'])
        self.ui.comboBox.addItems(data)

    async def upload_product(self, productName, productPath, productInfo, productType, projectid, username, password):
        """"""
        token = await self.login(username, password)
        product = await self.create_product(productName, productInfo, productType, projectid, token)
        await self.upload_asset(product, productPath)

    async def login(self, username, password):
        response = requests.post('http://dev-cn.laravel.com/api/v1/authorizations', params = {
            'username': username, 
            'password': password
        })
        json = self.networkUtil.checkResponse(response)
        return (json['data']['token_type'], json['data']['access_token'])

    async def create_product(self, productName, productInfo, productType, projectid, token):
        response = requests.post('http://dev-cn.laravel.com/api/v1/product', params = {
           'name': productName,
           'type': productType,
           'project_id': projectid,
           'info': productInfo
        }, headers= {
            'Authorization': token[0] + " " + token[1]
        })
        return self.networkUtil.checkResponse(response)

    async def upload_asset(self, product, productPath):
        """"""
        self.resumable_upload(product['data']['file_path'], productPath)
    
    def percentage(self, consumed_bytes, total_bytes):
        """"""

    def set_proccess(self, proccess):
        self.pd.setValue(proccess)

    def resumable_upload(self, target, source):
        self.pd = QProgressDialog('上传进度', '取消', 0, 100, self)
        self.pd.setLabelText('正在上传中...')
        self.pd.show()
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
        self.pd.setValue(100)

    @Slot()
    def on_pushButton_2_clicked(self):
        fileInfo = self.__fileDiaLog.getOpenFileName()
        if fileInfo:
            filePath = str.strip(fileInfo[0])
            self.ui.lineEdit.setText(filePath)
            

    @Slot()
    def on_pushButton_3_clicked(self):
            productName = str.strip(self.ui.lineEdit_2.text())
            productPath = str.strip(self.ui.lineEdit.text())
            productInfo = self.ui.textEdit.toPlainText()
            productType = self.ui.comboBox_2.currentIndex()
            projectIndex = self.ui.comboBox.currentIndex()
            username = str.strip(self.ui.lineEdit_3.text())
            password = str.strip(self.ui.lineEdit_4.text())
            if productName != '' and path.exists(productPath) and productInfo!='' and productType != 0 and projectIndex != 0 and username != '' and password != '':
                projectid = self.__projectList[int(projectIndex) - 1]['hash_id']
                asyncio.run(self.upload_product(productName, productPath, productInfo, productType, projectid, username, password))
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = UploadProduct()
    # apply_stylesheet(app, theme='light_pink.xml', invert_secondary=True)
    # apply_stylesheet(app, theme='light_pink.xml')
    myWindow.show()
    sys.exit(app.exec())
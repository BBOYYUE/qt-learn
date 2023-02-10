import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QListWidgetItem, QInputDialog, QMessageBox
from PySide6.QtCore import Slot, Signal, QStringListModel
from PySide6.QtGui import QPixmap
from ui.ProjectManageUi import Ui_MainWindow
from ui.ProjectListItemUi import Ui_Form as ProjectListItemUi
from ui.ProductListItemUi import Ui_Form as ProductListItemUi
from ui.DownloadProductItemUi import Ui_Form as DownloadProductItemUi
from ui.VerificationDeviceUi import Ui_Dialog as VerificationDeviceUi
from subprocess import Popen, call
from qt_material import apply_stylesheet
import shutil
import sqlite3
import requests
import asyncio
from util.SystemUtil import SystemUtil
from util.NetworkUtil import NetworkUtil
from os import path
from download.DownloadAsset import DownloadAsset

class ProjectManage(QMainWindow):

    __projectList = None
    __downloadList = []
    __dbname = path.abspath(path.join(path.dirname(__file__), 'data.db'))

    def __init__(self, parent = None):
        super().__init__(parent)
        self.__con = sqlite3.connect(self.__dbname)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.networkUtil = NetworkUtil()
        self.init_config()
        self.init_home()
        self.init_menubar()
        self.check_update()
        self.__inputDialog = QInputDialog(self)
    
    def init_home(self):
        asyncio.run(self.async_init_home())
    def init_config(self):
        asyncio.run(self.async_init_config())

    def init_menubar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("文件(&F)")
        actionClearAsset = fileMenu.addAction("清理资源文件")
        helpMenu = menubar.addMenu("帮助(&H)")
        actionCheckoutVaild = helpMenu.addAction("检查更新...")
        actionAbout = helpMenu.addAction("关于")
        actionClearAsset.triggered.connect(self.clear_asset)
        actionCheckoutVaild.triggered.connect(self.check_update)
        actionAbout.triggered.connect(self.show_about)
    
    def clear_asset(self):
        asyncio.run(self.async_clear_asset())
    
    async def async_clear_asset(self):
        try:
            self.statusBar().showMessage("正在清理垃圾...")
            con = self.__con
            cur = con.cursor()
            cur.execute("SELECT * FROM products where isvaild = 0")
            garbageList = cur.fetchall()
            for garbage in garbageList:
                assetPath = garbage[2]
                zipPath = garbage[3]
                zipDirPath = path.dirname(zipPath)
                if path.exists(zipDirPath):
                    shutil.rmtree(zipDirPath)
                if path.exists(assetPath):
                    shutil.rmtree(assetPath)

            con.commit()
            self.statusBar().showMessage("清理完成!", 5000)
        except:
            self.statusBar().showMessage("清理失败!", 5000)
    
    def show_about(self):
        QMessageBox.information(self, "关于", "阿尔法产品管理器2.0版本\n如果在使用中发现问题,请联系阿尔法售后部门\n")

    def check_update(self):
        asyncio.run(self.async_check_update())

    async def async_init_config(self):
        con = self.__con
        cur = con.cursor()
        cur.execute("SELECT * FROM configs")
        config = cur.fetchall()
        con.commit()
        self.__config = config[0]
        

    async def count_project_and_product(self):
        len = []
        con = self.__con
        cur = con.cursor()
        cur.execute("SELECT count(*) FROM projects")
        len.append(cur.fetchall()[0][0])
        cur.execute("SELECT count(*) FROM products")
        len.append(cur.fetchall()[0][0])
        con.commit()
        return len


    async def async_check_update(self):
        self.statusBar().showMessage("检查更新中...", 5000)
        await self.request_last_product_for_projectlist(self.__projectList)

    async def request_last_product_for_projectlist(self, projectList):
        projectIdList = ""
        for project in projectList:
            projectIdList = projectIdList + project[5] + ","

        projectIdList = str.strip(projectIdList, ',')
        try:
            response = requests.get('http://dev-cn.laravel.com/api/v1/project?include=products&filter[id]=' + projectIdList)
            json = self.networkUtil.checkResponse(response)
            if json == False:
                self.statusBar().showMessage("与服务器的网络通信建立失败...", 5000)
                return
        except:
            self.statusBar().showMessage("与服务器的网络通信建立失败...", 5000)
            nextTimes = int(self.__config[3]) - 1
            sqlUpdateConfig = "UPDATE configs SET `times`=?  WHERE id = ?"
            dataUpdateConfig = (nextTimes, 1)
            con = self.__con
            cur = con.cursor()
            cur.execute(sqlUpdateConfig, dataUpdateConfig)
            con.commit()
            return

        newProjectList = json['data']['data']
        updateProjectList = []
        updateProductList = []
        downloadProductList = []
        for project in self.__projectList:
            for newProject in newProjectList:
                if newProject['hash_id'] == project[5]:
                    if (
                        newProject['name'] != project[1] or 
                        newProject['address'] != project[2] or
                        newProject['phone'] != project[3] or
                        newProject['slogan'] != project[4]
                    ):
                        updateProjectList.append({'id': project[0], 'name': newProject['name'], 'address': newProject['address'], 'phone': newProject['phone'], 'slogan':newProject['slogan'] })
                    
                    product = await self.get_first_product_for_projectid(project[0])
                    newProduct = newProject['products'][0]
                    if (
                        newProduct['hash_id'] != product[5]
                    ):
                        downloadProductList.append({'code': project[5], 'id': product[0], 'projectid' :project[0], 'filepath': self.__config[2]})
                    elif(
                        newProduct['name'] != product[1] or
                        newProduct['info'] != product[4] 
                    ):
                        updateProductList.append({
                            'id':product[5],'name':newProduct['name'],'info': newProduct['info']
                        })
        
        self.statusBar().clearMessage()
        if(len(updateProjectList) > 0):
            self.statusBar().showMessage("正在同步项目信息", 5000)
            await self.sync_project_list(updateProjectList)

        if(len(updateProductList) > 0):
            self.statusBar().showMessage("正在同步产品信息", 5000)
            await self.sync_product_list(updateProductList)

        if(len(downloadProductList) > 0):
            self.statusBar().showMessage("正在获取最新安装包", 5000)
            await self.sync_download_list(downloadProductList)

        self.statusBar().showMessage("本地数据已同步至最新...", 5000)
        sqlUpdateConfig = "UPDATE configs SET `times`=?  WHERE id = ?"
        dataUpdateConfig = (30, 1)
        con = self.__con
        cur = con.cursor()
        cur.execute(sqlUpdateConfig, dataUpdateConfig)
        con.commit()
        # self.statusBar().clearMessage()
    
    async def sync_project_list(self, data):
        sqlUpdateProject = "UPDATE projects SET `name`=? ,`address`=? ,`phone`=? ,`slogan`=? ,`code`=? WHERE id = ?" 
        dataUpdateProject = (
            data['name'], 
            data['address'],
            data['phone'],
            data['slogan'], 
            data['code'],
            data['id']
        )
        con = self.__con
        cur = con.cursor()
        cur.execute(sqlUpdateProject, dataUpdateProject)
        con.commit()

    async def sync_product_list(self, data):
        sqlUpdateProduct = "UPDATE products SET `name`=? ,`info`=?  WHERE id = ?" 
        dataUpdateProduct = (
            data['name'], 
            data['info'], 
            data['id']
        )
        con = self.__con
        cur = con.cursor()
        cur.execute(sqlUpdateProduct, dataUpdateProduct)
        con.commit()

    async def sync_download_list(self, data):
        await asyncio.gather(*[self.download_asset(download, isCreate = False) for download in data ])
    
    def re_download_asset(self, data, item, isCreate):
        self.ui.listWidget_3.takeItem(self.ui.listWidget_3.indexFromItem(item).row())
        self.__downloadList.remove(data['code'])
        asyncio.run(self.download_asset(data, isCreate))

    async def download_asset(self, data, isCreate=False):
        download = DownloadAsset()


        # 重复点击直接跳过
        if data['code'] in self.__downloadList:
            return

        self.__downloadList.append(data['code'])
        assetInfo = download.set_asset_by_code(data['code'])

        widget = QWidget()
        downloadProductItemUi = DownloadProductItemUi()
        downloadProductItemUi.setupUi(widget)
        if assetInfo == False:
            self.statusBar().showMessage("获取项目信息失败...", 5000)
            return 

        downloadProductItemUi.label_2.setText(assetInfo['name'])
        downloadProductItemUi.label_3.setText(assetInfo['products'][0]['info'])
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.ui.listWidget_3.insertItem(0, item)
        self.ui.listWidget_3.setItemWidget(item, widget)
        download.set_proccess_ui(downloadProductItemUi.progressBar)
        zipPath = download.resumable_download(data['filepath'], lambda req, progressBar: self.download_proccess(req, progressBar))
        downloadProductItemUi.pushButton.setText('下载中...')
        if zipPath == False:
            downloadProductItemUi.pushButton.clicked.connect(lambda:self.re_download_asset(data, item, isCreate))
            downloadProductItemUi.pushButton.setText('点击重试')
            return

        download.unzip_asset()
        if(isCreate):
            await self.create_project(assetInfo, zipPath)
        else:
            await self.update_project(assetInfo, zipPath, data)
        downloadProductItemUi.progressBar.setValue(100)
        downloadProductItemUi.pushButton.setText('下载完成')
        self.ui.listWidget.clear()
        self.ui.listWidget_2.clear()
        await self.get_home_info()
        await self.set_home_info()
    
    async def create_project(self, assetInfo, zipPath):
        con = self.__con
        cur = con.cursor()
        len = await self.count_project_and_product()
        sqlInsertProject = "INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)" 
        dataInsertProject = (
            int(len[0]) + 1, 
            assetInfo['name'], 
            assetInfo['address'], 
            assetInfo['phone'], 
            assetInfo['slogan'], 
            assetInfo['hash_id']
        )
        sqlInsertProduct = "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)" 
        assetPath = self.__config[2] + '/' + assetInfo['products'][0]['hash_id']
        dataInsertProduct = (
            int(len[1]) + 1, 
            assetInfo['products'][0]['name'], 
            assetPath, 
            zipPath, 
            assetInfo['products'][0]['info'], 
            assetInfo['products'][0]['hash_id'],
            int(len[0]) + 1,
            1,
            assetInfo['products'][0]['created_at']
        )
        
        cur.execute(sqlInsertProject, dataInsertProject)
        cur.execute(sqlInsertProduct, dataInsertProduct)
        con.commit()

    async def update_project(self, assetInfo, zipPath, data):


        sqlUpdateProject = "UPDATE projects SET `name`=? ,`address`=? ,`phone`=? ,`slogan`=? ,`code`=?  WHERE id = ?"
        dataUpdateProject = (
            assetInfo['name'],
            assetInfo['address'],
            assetInfo['phone'],
            assetInfo['slogan'],
            assetInfo['hash_id'],
            data['projectid']
        )

        len = await self.count_project_and_product()
        sqlInsertProduct = "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)" 
        assetPath = self.__config[2] + '/' + assetInfo['products'][0]['hash_id']
        dataInsertProduct = (
            int(len[1]) + 1, 
            assetInfo['products'][0]['name'], 
            assetPath, 
            zipPath, 
            assetInfo['products'][0]['info'], 
            assetInfo['products'][0]['hash_id'],
            data['projectid'],
            1,
            assetInfo['products'][0]['created_at']
        )

        sqlUpdateProduct = "UPDATE products SET `isvaild`= ? WHERE id = ?" 
        assetPath = data['filepath'] + '/' + assetInfo['products'][0]['hash_id']
        dataUpdateProduct = (0, data['id'])
        con = self.__con
        cur = con.cursor()
        cur.execute(sqlUpdateProject, dataUpdateProject)
        cur.execute(sqlInsertProduct, dataInsertProduct)
        cur.execute(sqlUpdateProduct, dataUpdateProduct)
        con.commit()

    async def async_init_home(self):
        await self.get_home_info()
        await self.set_home_info()
    
    async def get_home_info(self):
        await self.get_project_list()
        await self.get_product_list()
    
    async def set_home_info(self):
        await self.set_project_list()
        await self.set_product_list(self.__activeProject, self.__productList)


    # 通过项目ID获取产品信息
    async def get_project_for_projectid(self, id):
        try:
            con = self.__con
            cur = con.cursor()
            cur.execute("SELECT * FROM projects where id = " + str(id))
            project = cur.fetchall()
            con.commit()
            return project[0]
        except:
            return False

    # 获取根据项目ID获取最新的产品信息
    async def get_first_product_for_projectid(self, id):
        try:
            con = self.__con
            cur = con.cursor()
            cur.execute("SELECT * FROM products where isvaild = 1 AND projectid = " + str(id) + " ORDER BY id DESC")
            product = cur.fetchall()
            con.commit()
            return product[0]
        except:
            return False

    # 获取项目列表
    async def get_project_list(self):
        con = self.__con
        cur = con.cursor()
        cur.execute('''SELECT * FROM projects''')
        self.__projectList = cur.fetchall()
        con.commit()
        self.__activeProject = self.__projectList[0]

    # 获取产品列表, 获取产品列表时总是获取当前选中的项目的产品列表
    async def get_product_list(self):
        con = self.__con
        cur = con.cursor()
        sql = "SELECT * FROM products WHERE isvaild = 1 AND projectid = " + str(self.__activeProject[0])
        cur.execute(sql)
        self.__productList = cur.fetchall()
        con.commit()


    # 展示产品列表
    async def set_product_list(self, project, product, is_init = True):
        try:
            self.ui.listWidget_2.clear()
        except Exception: pass 
        for data in product:
            widget = QWidget()
            productListItemUi = ProductListItemUi()
            productListItemUi.setupUi(widget)
            productListItemUi.pushButtonStart.clicked.connect(self.on_start_clicked)
            productListItemUi.label.setPixmap(QPixmap(data[2] + '/' +'logo.jpg'))
            productListItemUi.label_2.setText(data[1])
            productListItemUi.label_3.setText(project[4])
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.ui.listWidget_2.addItem(item)
            self.ui.listWidget_2.setItemWidget(item, widget)

        if is_init and self.__config[3] > 0:
            self.ui.listWidget_2.clicked.connect(lambda x: self.on_listWidget_2_itemClicked(x))

    # 展示项目列表
    async def set_project_list(self, is_init = True):
        try:
            self.ui.listWidget.clear()
        except Exception: pass
        for data in self.__projectList:
            product = await self.get_first_product_for_projectid(data[0])
            widget = QWidget()
            projectListItemUi = ProjectListItemUi()
            projectListItemUi.setupUi(widget)
            projectListItemUi.label.setPixmap(QPixmap(product[2] + '/' +'logo.jpg'))
            projectListItemUi.label_2.setText(data[1])
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.ui.listWidget.addItem(item)
            self.ui.listWidget.setItemWidget(item, widget)

        if is_init:
            self.ui.listWidget.clicked.connect(lambda x: self.on_listWidget_itemClicked(x))

    @Slot()
    def on_pushButton_clicked(self):
        self.__inputDialog.setWindowTitle("添加项目")
        self.__inputDialog.setLabelText("请输入激活码：")
        self.__inputDialog.setInputMode(QInputDialog.TextInput)
        self.__inputDialog.setOkButtonText("确定")
        self.__inputDialog.setCancelButtonText("取消")
        self.__inputDialog.textValueSelected.connect(self.add_project)
        self.__inputDialog.exec()

    def add_project(self, text):
        asyncio.run(self.async_add_project(text))

    async def async_add_project(self, projectid):
        isRepeat = await self.get_project_for_projectid(projectid)
        if isRepeat == False:
            data = dict() 
            data['filepath'] = self.__config[2]
            data['code'] = projectid
            await self.download_asset(data, True)
        else: 
            self.statusBar().showMessage("此激活码已使用", 5000)

    def on_start_clicked(self, item):
        data = self.__productList[item]
        exepath = data[2] + '/MirageWork.exe'
        Popen(exepath)


    def on_listWidget_itemClicked(self, item):
        index = item.row()
        self.__activeProject = self.__projectList[index]
        asyncio.run(self.checkout_project())
        
    def on_listWidget_2_itemClicked(self, item):
        print(item)

    async def checkout_project(self):
        await self.get_product_list()
        await self.set_product_list(self.__activeProject, self.__productList, is_init= False)

   
    def download_proccess(self, data, progressBar):
        progressBar.setValue(data.get('poccess'))
     


  
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = ProjectManage()
    # apply_stylesheet(app, theme='light_pink.xml', invert_secondary=True)
    # apply_stylesheet(app, theme='light_pink.xml')
    myWindow.show()
    sys.exit(app.exec())
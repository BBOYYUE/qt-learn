import oss2
import os
import requests
import zipfile
from util.NetworkUtil import NetworkUtil
import time

class DownloadAsset():

    auth = oss2.Auth('LTAI5tGzTWyXiajVYViDUWgs', 's42GqptOYVUU1wVeURsRTYEEqBfR3y')
    bucket = oss2.Bucket(auth, endpoint='http://oss-cn-zhangjiakou.aliyuncs.com', bucket_name='alpha-serve')
    unziping = False
    downloaderror = False
    progressBar = None

    def __init__(self):
        self.networkUtil = NetworkUtil()

    def set_asset_by_code(self, code):
        try:
            self.code = code
            response = requests.get(
                "http://dev-cn.laravel.com/api/v1/project?include=products&filter[id]=" + code)
            json = self.networkUtil.checkResponse(response)
            self.source = json['data']['data'][0]['products'][0]['file_path']
            return json['data']['data'][0]
        except Exception as e:
          print(e)
          return False

    def progress_callback(self, consumed_bytes, total_bytes):
        proccess = (consumed_bytes / total_bytes) * 100
        self.proccess = proccess * .8
        msg = dict()
        msg['code'] = '200'
        msg['state'] = "pedding"
        msg['msg'] = ""
        msg['poccess'] = self.proccess
        msg['project'] = self.code
        if self.progressBar != None:
          self.callback(msg,self.progressBar)
        else:
          self.callback(msg)
    
    def set_proccess_ui(self, progressBar):
        self.progressBar = progressBar

    def unzip_asset(self):
        if self.unziping == True:
                return
        self.unziping == True
        try:
          print(self.assetpath)
          if not os.path.isdir(self.assetpath):
                os.makedirs(self.assetpath)
          zf = zipfile.ZipFile(self.filepath)
          zf.extractall(self.assetpath)
          zf.close()
          self.proccess = 90
          msg = dict()
          msg['code'] = '200'
          msg['state'] = "successed"
          msg['msg'] = ""
          msg['poccess'] = self.proccess
          msg['project'] = self.code
          if self.progressBar != None:
              self.callback(msg, self.progressBar)
          else:
              self.callback(msg)
          return self.target
        except Exception as e:
          print(e)
          self.proccess = 90
          msg = dict()
          msg['code'] = '400'
          msg['state'] = "error"
          msg['msg'] = "解压失败"
          msg['poccess'] = self.proccess
          msg['project'] = self.code
          if self.progressBar != None:
              self.callback(msg, self.progressBar)
          else:
              self.callback(msg)

    def resumable_download(self, target, callback):
        self.proccess = 0
        self.callback = callback
        try:
            source = self.source
            self.filepath = target + '/' + source
            self.target = target
            self.assetpath = target + '/' + os.path.splitext(os.path.basename(self.filepath))[0]
            # 这里判断文件保存位置的文件夹是否存在, 如果不存在的话需要创建文件夹
            dirname = os.path.dirname(self.filepath)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
                msg = dict()
                msg['code'] = '200'
                msg['state'] = "pedding"
                msg['msg'] = "已获取到资源地址"
                msg['poccess'] = 0
                msg['project'] = self.code
                if self.progressBar != None:
                    self.callback(msg, self.progressBar)
                else:
                    self.callback(msg)
            elif self.downloaderror == True:
                msg = dict()
                msg['code'] = '200'
                msg['state'] = "pedding"
                msg['msg'] = "正在从中断处重新下载..."
                msg['poccess'] = self.proccess
                msg['project'] = self.code
                if self.progressBar != None:
                    self.callback(msg, self.progressBar)
                else:
                    self.callback(msg)
            else:
                msg = dict()
                msg['code'] = '200'
                msg['state'] = "pedding"
                msg['msg'] = "开始下载..."
                msg['poccess'] = 0
                msg['project'] = self.code
                if self.progressBar != None:
                    self.callback(msg, self.progressBar)
                else:
                    self.callback(msg)
            print(source)
            oss2.resumable_download(self.bucket, source, self.filepath,
                    #   store=oss2.ResumableDownloadStore(root='/tmp'),
                    # 指定当文件长度大于或等于可选参数multipart_threshold（默认值为10 MB, 这里是 100MB）时，则使用断点续传下载。
                      multiget_threshold=100*1000*1024,
                    # 设置分片大小，单位为字节，取值范围为100 KB~5 GB。默认值为100 KB。 这里是 10MB
                      part_size=10*1000*1024,
                    # 设置下载进度回调函数。
                      progress_callback=self.progress_callback,
                    # 如果使用num_threads设置并发下载线程数，请将oss2.defaults.connection_pool_size设置为大于或等于并发下载线程数。默认并发下载线程数为1。
                      num_threads=4)
            return self.filepath

        except Exception as e:
            print(e)
            msg = dict()
            msg['code'] = '400'
            msg['state'] = "error"
            msg['msg'] = "下载中断, 五秒后重试... "
            msg['poccess'] = self.proccess
            msg['project'] = self.code
            self.downloaderror = True
            if self.progressBar != None:
                self.callback(msg, self.progressBar)
            else:
                self.callback(msg)
            return False
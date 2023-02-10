from ProjectManage import ProjectManage
from InitializeBoot import InitializeBoot
from PySide6.QtWidgets import QApplication
import sys
import sqlite3
from os import path
from util.SystemUtil import SystemUtil

"""
打包命令
pyinstaller.exe -F .\InitializeBoot.py --add-data "E:\code\qt-learn\data.db;.\"
pyinstaller.exe -w .\setup.py --add-data "E:\code\qt-learn\data.db;.\"
"""
def is_not_first_boot():
    try:
        dbname = path.abspath(path.join(path.dirname(__file__), 'data.db'))
        con = sqlite3.connect(dbname)
        print(dbname)
        cur = con.cursor()
        cur.execute('''SELECT * FROM projects''')
        projects = cur.fetchall()
        print(projects)
        cur.execute('''SELECT * FROM products''')
        products = cur.fetchall()
        print(products)
        cur.execute('''SELECT * FROM configs''')
        configs = cur.fetchall()
        print(configs)
        con.close()
        # print(projects, products)
        pempath = configs[0][2] + '/' + 'public.pem'
        print(pempath)
        if path.exists(pempath) == False:
            return False
        system = SystemUtil()
        cpuid = system.uuid()
        print(configs, cpuid)
        return configs[0][1] == cpuid
    except:
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    isNotFirstBoot = is_not_first_boot() 
    if isNotFirstBoot :
        myWindow = ProjectManage()
    else:
        myWindow = InitializeBoot()
    # myWindow = ProjectManage()
    # apply_stylesheet(app, theme='light_tea.xml', invert_secondary=True)
    # apply_stylesheet(app, theme='light_pink.xml')
    myWindow.show()
    sys.exit(app.exec())
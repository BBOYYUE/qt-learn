# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'initializeBoot.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget,
    QWizard, QWizardPage)

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.setWindowModality(Qt.NonModal)
        Wizard.resize(540, 360)
        Wizard.setMinimumSize(QSize(540, 360))
        Wizard.setMaximumSize(QSize(720, 540))
        Wizard.setBaseSize(QSize(540, 360))
        Wizard.setLayoutDirection(Qt.LeftToRight)
        Wizard.setAutoFillBackground(False)
        Wizard.setSizeGripEnabled(False)
        Wizard.setModal(False)
        Wizard.setWizardStyle(QWizard.NStyles)
        self.wizardPageWelcome = QWizardPage()
        self.wizardPageWelcome.setObjectName(u"wizardPageWelcome")
        self.groupBox = QGroupBox(self.wizardPageWelcome)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 500, 140))
        self.groupBox.setMinimumSize(QSize(500, 0))
        self.groupBox.setMaximumSize(QSize(500, 140))
        self.groupBox.setBaseSize(QSize(680, 200))
        self.groupBox.setLayoutDirection(Qt.LeftToRight)
        self.groupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser_3 = QTextBrowser(self.groupBox)
        self.textBrowser_3.setObjectName(u"textBrowser_3")

        self.verticalLayout.addWidget(self.textBrowser_3)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout.addWidget(self.checkBox)

        Wizard.setPage(0, self.wizardPageWelcome)
        self.wizardPageSelectFilePath = QWizardPage()
        self.wizardPageSelectFilePath.setObjectName(u"wizardPageSelectFilePath")
        self.groupBox_2 = QGroupBox(self.wizardPageSelectFilePath)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 80, 500, 70))
        self.groupBox_2.setMinimumSize(QSize(500, 0))
        self.groupBox_2.setMaximumSize(QSize(500, 16777215))
        self.groupBox_2.setBaseSize(QSize(500, 0))
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.groupBox_2)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        Wizard.setPage(1, self.wizardPageSelectFilePath)
        self.wizardPageRegisterCode = QWizardPage()
        self.wizardPageRegisterCode.setObjectName(u"wizardPageRegisterCode")
        self.groupBox_3 = QGroupBox(self.wizardPageRegisterCode)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 60, 500, 80))
        self.groupBox_3.setMinimumSize(QSize(500, 0))
        self.groupBox_3.setMaximumSize(QSize(680, 16777215))
        self.groupBox_3.setBaseSize(QSize(500, 0))
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEdit_2 = QLineEdit(self.groupBox_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.pushButton_2 = QPushButton(self.groupBox_3)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        Wizard.setPage(2, self.wizardPageRegisterCode)
        self.wizardPageDownload = QWizardPage()
        self.wizardPageDownload.setObjectName(u"wizardPageDownload")
        self.groupBox_4 = QGroupBox(self.wizardPageDownload)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 30, 500, 120))
        self.groupBox_4.setMinimumSize(QSize(500, 0))
        self.groupBox_4.setMaximumSize(QSize(680, 16777215))
        self.groupBox_4.setBaseSize(QSize(500, 0))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.textBrowser = QTextBrowser(self.groupBox_4)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_3.addWidget(self.textBrowser)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.progressBar = QProgressBar(self.groupBox_4)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.horizontalLayout_4.addWidget(self.progressBar)

        self.pushButton_3 = QPushButton(self.groupBox_4)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_4.addWidget(self.pushButton_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        Wizard.setPage(3, self.wizardPageDownload)
        self.wizardPageSuccess = QWizardPage()
        self.wizardPageSuccess.setObjectName(u"wizardPageSuccess")
        Wizard.setPage(4, self.wizardPageSuccess)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"\u5f15\u5bfc\u7a0b\u5e8f", None))
#if QT_CONFIG(tooltip)
        Wizard.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.wizardPageWelcome.setTitle(QCoreApplication.translate("Wizard", u"\u6b22\u8fce!", None))
        self.groupBox.setTitle(QCoreApplication.translate("Wizard", u"\u514d\u8d23\u6761\u6b3e:", None))
        self.textBrowser_3.setHtml(QCoreApplication.translate("Wizard", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.\u672c\u5ba3\u4f20\u8d44\u6599\u6587\u5b57\u3001\u6570\u636e\u3001\u89c6\u9891\u3001\u56fe\u7247\u4ec5\u4f9b\u53c2\u8003\uff0c\u4e0d\u4f5c\u4e3a\u9080\u7ea6\u6216\u627f\u8bfa\uff0c\u4e70\u5356\u53cc\u65b9\u6743\u5229\u3001\u4e49\u52a1\u4ee5\u5408\u540c\u4e3a\u51c6\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent"
                        ":0px;\">2.\u672c\u5ba3\u4f20\u8d44\u6599\u7cfb\u516c\u53f8\u5173\u4e8e\u9879\u76ee\u89c4\u5212\u610f\u5411\u7684\u6982\u5ff5\u5c55\u793a\uff0c\u975e\u6700\u7ec8\u89c4\u5212\u65b9\u6848\uff0c\u5bf9\u4e70\u5356\u53cc\u65b9\u6ca1\u6709\u7ea6\u675f\u529b\uff0c\u56e0\u5c55\u793a\u5de5\u827a\u3001\u6750\u8d28\u3001\u6bd4\u4f8b\u548c\u5e45\u9762\u9650\u5236\u7b49\u6761\u4ef6\u6240\u9650\uff0c\u4e0e\u5b9e\u666f\u53ef\u80fd\u5b58\u5728\u4e00\u5b9a\u5dee\u5f02\uff0c\u656c\u8bf7\u7559\u610f\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3.\u672c\u5ba3\u4f20\u8d44\u6599\u5efa\u7b51\u7acb\u9762\u3001\u56ed\u533a\u666f\u89c2\u56ed\u6797\u4ee5\u6211\u516c\u53f8\u73b0\u9636\u6bb5\u89c4\u5212\u65b9\u6848\u4e3a\u4f9d\u636e\u8fdb\u884c\u5236\u4f5c\uff0c\u4ec5\u4f5c\u4e3a\u9879\u76ee\u89c4\u5212\u793a\u610f\uff0c\u4e0e\u6700\u7ec8\u4ea4\u4ed8\u6807\u6807\u51c6\u4e0d\u540c\uff0c\u6700\u7ec8\u4ea4\u4ed8\u7ed3\u679c\u4ee5\u653f\u5e9c\u90e8\u95e8\u6838"
                        "\u51c6\u6587\u4ef6\u53ca\u4e70\u5356\u53cc\u65b9\u8ba2\u7acb\u7684\u5546\u54c1\u623f\u4e70\u5356\u5408\u540c\u7ea6\u5b9a\u4e3a\u51c6\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4.\u672c\u5ba3\u4f20\u8d44\u6599\u5bf9\u9879\u76ee\u5916\u5468\u56f4\u73af\u5883\u3001\u4ea4\u901a\u3001\u516c\u5171\u8bbe\u65bd\u7684\u5730\u7406\u5173\u7cfb\u4ec5\u4e3a\u793a\u610f\uff0c\u4e0d\u610f\u5473\u672c\u516c\u53f8\u5bf9\u6b64\u505a\u51fa\u4efb\u4f55\u627f\u8bfa\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5.\u672c\u5ba3\u4f20\u8d44\u6599\u56ed\u533a\u666f\u89c2\u56ed\u6797\u3001\u697c\u68af\u5916\u7acb\u9762\u989c\u8272\u3001\u88c5\u9970\u7ed3\u6784\u7ebf\u6761\u3001\u7a7a\u8c03\u673a\u7b49\u5747\u4e0e\u6700\u7ec8\u4ea4\u4ed8\u6807\u51c6\u4e0d\u540c\uff0c\u6700\u7ec8\u4ea4\u4ed8\u7ed3\u679c\u4ee5\u653f\u5e9c\u90e8\u95e8\u6838\u51c6\u6587\u4ef6\u53ca"
                        "\u4e70\u5356\u53cc\u65b9\u8ba2\u7acb\u7684\u5546\u54c1\u623f\u4e70\u5356\u5408\u540c\u7ea6\u5b9a\u4e3a\u51c6\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6.\u533a\u4f4d\u6559\u80b2\u914d\u5957\uff1a\u672c\u5e7f\u544a\u5bf9\u5468\u8fb9\u5b66\u6821\u7684\u8868\u8ff0\uff0c\u4ec5\u4f9b\u53c2\u8003\u4fe1\u606f\u6765\u6e90\u4e8e\u767e\u5ea6\u767e\u79d1\uff0c(1)\u5b66\u6821\u7684\u540d\u79f0\u3001\u5efa\u6210\u65f6\u95f4\u3001\u5f00\u529e\u6027\u8d28\u3001\u529e\u5b66\u89c4\u6a21\u3001\u5b66\u4f4d\u8bbe\u7f6e\u3001\u5f00\u5b66\u65f6\u95f4\u3001\u62db\u751f\u6761\u4ef6\u3001\u6536\u8d39\u6807\u51c6\u53ca\u62db\u751f\u533a\u57df\u5212\u5b9a\u7b49\u5747\u5b58\u5728\u672a\u786e\u5b9a\u6216\u8005\u8c03\u6574\u53ef\u80fd\uff0c\u51fa\u5356\u4eba\u5bf9\u6b64\u4e0d\u4f5c\u4efb\u4f55\u627f\u3000\u8bfa\uff0c\u6700\u7ec8\u987b\u4ee5\u653f\u5e9c\u90e8\u95e8\u6216\u76f8\u5173\u6559\u80b2\u5355\u4f4d\u7684\u6700\u65b0\u653f\u7b56\u4e3a\u51c6\uff1b"
                        "(2)\u4ea4\u901a\u3001\u5e02\u653f\u914d\u5957\uff1a\u672c\u5e7f\u544a\u5bf9\u9879\u76ee\u5468\u8fb9\u4ea4\u901a\u60c5\u51b5\u3001\u516c\u56ed\u7b49\u914d\u5957\u8bbe\u65bd\u7b49\u4fe1\u606f\u6765\u6e90\u4e8e2021\u5e7411\u670830\u65e5\uff0c\u5e02\u653f\u914d\u5957\u4fe1\u606f\u6765\u6e90\u4e8e2021\u5e7411\u670830\u65e5\uff0c\u5e02\u653f\u914d\u5957\u8bbe\u7f6e\u4e0d\u6392\u9664\u56e0\u653f\u5e9c\u89c4\u5212\u3001\u653f\u7b56\u89c4\u5b9a\u3000\u53ca\u51fa\u5356\u4eba\u672a\u80fd\u63a7\u5236\u7684\u539f\u56e0\u800c\u53d1\u751f\u53d8\u5316\uff0c\u672c\u9875\u4e2d\u5bf9\u9879\u76ee\u5468\u56f4\u73af\u5883\u3001\u4ea4\u901a\u53ca\u5176\u5b83\u516c\u5171\u8bbe\u65bd\u7684\u4ecb\u7ecd\uff0c\u65e8\u5728\u63d0\u4f9b\u76f8\u5173\u53c2\u8003\u4fe1\u606f\uff0c\u4e0d\u89c6\u4e3a\u672c\u516c\u53f8\u5bf9\u6b64\u4f5c\u51fa\u4e86\u8981\u7ea6\u6216\u627f\u8bfa\u3002(3)\u8ddd\u79bb\u7684\u4fe1\u606f\u8868\u8ff0\uff1a\u8be5\u8ddd\u79bb\u67e5\u8be2\u6765\u6e90\u4e8e\u767e\u5ea6\u5730\u56fe\uff0c\u6240\u793a\u8ddd\u79bb\u660e\u786e\u4e3a"
                        "\u76f4\u7ebf\u8ddd\u79bb\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7.\u56fe\u7247\u4fe1\u606f\uff1a\u672c\u5ba3\u4f20\u8d44\u6599\u4e2d\u90e8\u5206\u56fe\u7247\u7d20\u6750\u6765\u6e90\u4e8e\u7f51\u7edc\uff0c\u65e0\u6cd5\u6838\u5b9e\u771f\u5b9e\u51fa\u5904\uff0c\u5982\u6d89\u53ca\u4fb5\u6743\u8bf7\u8054\u7cfb\u5f00\u53d1\u5546\u6211\u4eec\u5c06\u53ca\u65f6\u5220\u9664\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">8.\u672c\u5ba3\u4f20\u8d44\u6599\u4e00\u5207\u672a\u6709\u4f8b\u4e3e\u4e8b\u9879\u6216\u66f4\u6539\uff0c\u6055\u4e0d\u53e6\u884c\u901a\u77e5\u3002</p></body></html>", None))
        self.checkBox.setText(QCoreApplication.translate("Wizard", u"\u6211\u540c\u610f", None))
        self.wizardPageSelectFilePath.setTitle(QCoreApplication.translate("Wizard", u"\u9009\u62e9\u7a0b\u5e8f\u6587\u4ef6\u4f4d\u7f6e", None))
        self.wizardPageSelectFilePath.setSubTitle("")
        self.groupBox_2.setTitle(QCoreApplication.translate("Wizard", u"\u7a0b\u5e8f\u6587\u4ef6\u9700\u8981\u81f3\u5c1120GB\u7684\u5b58\u50a8\u7a7a\u95f4", None))
        self.pushButton.setText(QCoreApplication.translate("Wizard", u"\u9009\u62e9\u8def\u5f84...", None))
        self.wizardPageRegisterCode.setTitle(QCoreApplication.translate("Wizard", u"\u6fc0\u6d3b\u8bbe\u5907", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Wizard", u"\u6fc0\u6d3b\u8fc7\u7a0b\u4e2d\u8bf7\u4fdd\u6301\u8054\u7f51", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"\u6fc0\u6d3b\u7801\uff1a", None))
        self.pushButton_2.setText(QCoreApplication.translate("Wizard", u"\u6fc0\u6d3b\u8bbe\u5907", None))
        self.wizardPageDownload.setTitle(QCoreApplication.translate("Wizard", u"\u4e0b\u8f7d\u8d44\u6e90\u6587\u4ef6", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Wizard", u"\u6b63\u5728\u4e0b\u8f7d\u8d44\u6e90\u6587\u4ef6", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Wizard", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Ubuntu'; font-size:11pt;\">\u6b63\u5728\u4e0b\u8f7d\u7a0b\u5e8f\u8d44\u6e90\u6587\u4ef6\uff0c\u4e0b\u8f7d\u901f\u5ea6\u548c\u60a8\u7684\u7f51\u901f\u6709\u5173\u3002\u4e0b\u8f7d\u53ef\u80fd\u4f1a\u6301\u7eed\u8f83\u957f\u65f6\u95f4\uff0c\u8bf7\u8010\u5fc3\u7b49\u5f85\u3002</span></p></body></html>", None))
        self.pushButton_3.setText(QCoreApplication.translate("Wizard", u"\u6b63\u5728\u4e0b\u8f7d", None))
        self.wizardPageSuccess.setTitle(QCoreApplication.translate("Wizard", u"\u5b89\u88c5\u5b8c\u6210!", None))
    # retranslateUi


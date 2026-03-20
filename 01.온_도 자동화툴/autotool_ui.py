# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'autotool.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QListView, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(789, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stacked_main = QStackedWidget(self.centralwidget)
        self.stacked_main.setObjectName(u"stacked_main")
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.layoutWidget = QWidget(self.page_main)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(220, 50, 311, 471))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.order_collect_btn = QPushButton(self.layoutWidget)
        self.order_collect_btn.setObjectName(u"order_collect_btn")
        self.order_collect_btn.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(50)
        sizePolicy1.setHeightForWidth(self.order_collect_btn.sizePolicy().hasHeightForWidth())
        self.order_collect_btn.setSizePolicy(sizePolicy1)
        self.order_collect_btn.setMinimumSize(QSize(0, 100))
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.order_collect_btn.setFont(font)

        self.verticalLayout.addWidget(self.order_collect_btn)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.order_check_btn = QPushButton(self.layoutWidget)
        self.order_check_btn.setObjectName(u"order_check_btn")
        sizePolicy.setHeightForWidth(self.order_check_btn.sizePolicy().hasHeightForWidth())
        self.order_check_btn.setSizePolicy(sizePolicy)
        self.order_check_btn.setMinimumSize(QSize(0, 100))
        self.order_check_btn.setFont(font)
        self.order_check_btn.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.verticalLayout.addWidget(self.order_check_btn)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.invoice_send_btn = QPushButton(self.layoutWidget)
        self.invoice_send_btn.setObjectName(u"invoice_send_btn")
        sizePolicy1.setHeightForWidth(self.invoice_send_btn.sizePolicy().hasHeightForWidth())
        self.invoice_send_btn.setSizePolicy(sizePolicy1)
        self.invoice_send_btn.setMinimumSize(QSize(0, 100))
        self.invoice_send_btn.setFont(font)

        self.verticalLayout.addWidget(self.invoice_send_btn)

        self.stacked_main.addWidget(self.page_main)
        self.page_check = QWidget()
        self.page_check.setObjectName(u"page_check")
        self.verticalLayoutWidget = QWidget(self.page_check)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(40, 120, 158, 331))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stock_file = QPushButton(self.verticalLayoutWidget)
        self.stock_file.setObjectName(u"stock_file")
        self.stock_file.setMinimumSize(QSize(0, 80))
        font1 = QFont()
        font1.setPointSize(14)
        self.stock_file.setFont(font1)

        self.verticalLayout_2.addWidget(self.stock_file)

        self.customer_file = QPushButton(self.verticalLayoutWidget)
        self.customer_file.setObjectName(u"customer_file")
        sizePolicy.setHeightForWidth(self.customer_file.sizePolicy().hasHeightForWidth())
        self.customer_file.setSizePolicy(sizePolicy)
        self.customer_file.setMinimumSize(QSize(0, 80))
        self.customer_file.setFont(font1)

        self.verticalLayout_2.addWidget(self.customer_file)

        self.verticalLayoutWidget_2 = QWidget(self.page_check)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(220, 40, 371, 511))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.check_list = QListView(self.verticalLayoutWidget_2)
        self.check_list.setObjectName(u"check_list")

        self.verticalLayout_3.addWidget(self.check_list)

        self.verticalLayoutWidget_5 = QWidget(self.page_check)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(620, 80, 158, 401))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.stock_btn = QPushButton(self.verticalLayoutWidget_5)
        self.stock_btn.setObjectName(u"stock_btn")
        self.stock_btn.setMinimumSize(QSize(0, 80))
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        self.stock_btn.setFont(font2)

        self.verticalLayout_7.addWidget(self.stock_btn)

        self.costomer_btn = QPushButton(self.verticalLayoutWidget_5)
        self.costomer_btn.setObjectName(u"costomer_btn")
        sizePolicy.setHeightForWidth(self.costomer_btn.sizePolicy().hasHeightForWidth())
        self.costomer_btn.setSizePolicy(sizePolicy)
        self.costomer_btn.setMinimumSize(QSize(0, 80))
        self.costomer_btn.setFont(font2)

        self.verticalLayout_7.addWidget(self.costomer_btn)

        self.Back_btn2 = QPushButton(self.verticalLayoutWidget_5)
        self.Back_btn2.setObjectName(u"Back_btn2")
        sizePolicy.setHeightForWidth(self.Back_btn2.sizePolicy().hasHeightForWidth())
        self.Back_btn2.setSizePolicy(sizePolicy)
        self.Back_btn2.setMinimumSize(QSize(0, 80))
        font3 = QFont()
        font3.setPointSize(14)
        font3.setBold(False)
        self.Back_btn2.setFont(font3)

        self.verticalLayout_7.addWidget(self.Back_btn2)

        self.stacked_main.addWidget(self.page_check)
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.login_card = QFrame(self.page_login)
        self.login_card.setObjectName(u"login_card")
        self.login_card.setGeometry(QRect(180, 120, 420, 320))
        self.login_card.setMinimumSize(QSize(420, 320))
        self.login_card.setMaximumSize(QSize(420, 320))
        self.login_card.setFrameShape(QFrame.Shape.StyledPanel)
        self.login_card.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayoutWidget_8 = QWidget(self.login_card)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(110, 60, 221, 141))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.code = QLabel(self.verticalLayoutWidget_8)
        self.code.setObjectName(u"code")
        self.code.setMinimumSize(QSize(0, 50))
        font4 = QFont()
        font4.setPointSize(18)
        self.code.setFont(font4)
        self.code.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.code.setStyleSheet(u"")
        self.code.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.code)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_6)

        self.code_name = QLineEdit(self.verticalLayoutWidget_8)
        self.code_name.setObjectName(u"code_name")
        font5 = QFont()
        font5.setPointSize(12)
        self.code_name.setFont(font5)
        self.code_name.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.verticalLayout_10.addWidget(self.code_name)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_5)

        self.login_btn = QPushButton(self.login_card)
        self.login_btn.setObjectName(u"login_btn")
        self.login_btn.setGeometry(QRect(140, 230, 151, 51))
        font6 = QFont()
        font6.setPointSize(20)
        font6.setBold(False)
        self.login_btn.setFont(font6)
        self.login_btn.setStyleSheet(u"QLabel {\n"
"    background-color: #3A3A3A;\n"
"    color: #FFFFFF;\n"
"    padding: 6px 12px;\n"
"    border-radius: 10px;\n"
"    font-weight: 700;\n"
"}")
        self.stacked_main.addWidget(self.page_login)
        self.page_invoice = QWidget()
        self.page_invoice.setObjectName(u"page_invoice")
        self.verticalLayoutWidget_6 = QWidget(self.page_invoice)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(250, 30, 471, 481))
        self.verticalLayout_8 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.send_list = QListView(self.verticalLayoutWidget_6)
        self.send_list.setObjectName(u"send_list")

        self.verticalLayout_8.addWidget(self.send_list)

        self.verticalLayoutWidget_7 = QWidget(self.page_invoice)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(30, 60, 201, 451))
        self.verticalLayout_9 = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.lotte_upload_btn = QPushButton(self.verticalLayoutWidget_7)
        self.lotte_upload_btn.setObjectName(u"lotte_upload_btn")
        sizePolicy.setHeightForWidth(self.lotte_upload_btn.sizePolicy().hasHeightForWidth())
        self.lotte_upload_btn.setSizePolicy(sizePolicy)
        self.lotte_upload_btn.setMinimumSize(QSize(0, 80))
        self.lotte_upload_btn.setFont(font5)

        self.verticalLayout_9.addWidget(self.lotte_upload_btn)

        self.creat_file_btn = QPushButton(self.verticalLayoutWidget_7)
        self.creat_file_btn.setObjectName(u"creat_file_btn")
        sizePolicy.setHeightForWidth(self.creat_file_btn.sizePolicy().hasHeightForWidth())
        self.creat_file_btn.setSizePolicy(sizePolicy)
        self.creat_file_btn.setMinimumSize(QSize(0, 80))
        self.creat_file_btn.setFont(font1)

        self.verticalLayout_9.addWidget(self.creat_file_btn)

        self.send_invoice_btn = QPushButton(self.verticalLayoutWidget_7)
        self.send_invoice_btn.setObjectName(u"send_invoice_btn")
        self.send_invoice_btn.setMinimumSize(QSize(0, 80))
        self.send_invoice_btn.setFont(font2)

        self.verticalLayout_9.addWidget(self.send_invoice_btn)

        self.Back_btn3 = QPushButton(self.verticalLayoutWidget_7)
        self.Back_btn3.setObjectName(u"Back_btn3")
        sizePolicy.setHeightForWidth(self.Back_btn3.sizePolicy().hasHeightForWidth())
        self.Back_btn3.setSizePolicy(sizePolicy)
        self.Back_btn3.setMinimumSize(QSize(0, 80))
        self.Back_btn3.setFont(font1)

        self.verticalLayout_9.addWidget(self.Back_btn3)

        self.stacked_main.addWidget(self.page_invoice)
        self.page_collect = QWidget()
        self.page_collect.setObjectName(u"page_collect")
        self.horizontalLayoutWidget = QWidget(self.page_collect)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(80, 60, 451, 451))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listView = QListView(self.horizontalLayoutWidget)
        self.listView.setObjectName(u"listView")

        self.horizontalLayout_2.addWidget(self.listView)

        self.frame = QFrame(self.page_collect)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(550, 140, 221, 101))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayoutWidget_2 = QWidget(self.frame)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(20, 10, 191, 81))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.start_order_btn = QPushButton(self.horizontalLayoutWidget_2)
        self.start_order_btn.setObjectName(u"start_order_btn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.start_order_btn.sizePolicy().hasHeightForWidth())
        self.start_order_btn.setSizePolicy(sizePolicy2)
        font7 = QFont()
        font7.setPointSize(18)
        font7.setBold(True)
        self.start_order_btn.setFont(font7)

        self.horizontalLayout_3.addWidget(self.start_order_btn)

        self.frame_2 = QFrame(self.page_collect)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(550, 330, 221, 101))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayoutWidget_3 = QWidget(self.frame_2)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(20, 10, 191, 81))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.Back_btn1 = QPushButton(self.horizontalLayoutWidget_3)
        self.Back_btn1.setObjectName(u"Back_btn1")
        sizePolicy2.setHeightForWidth(self.Back_btn1.sizePolicy().hasHeightForWidth())
        self.Back_btn1.setSizePolicy(sizePolicy2)
        font8 = QFont()
        font8.setPointSize(18)
        font8.setBold(False)
        self.Back_btn1.setFont(font8)

        self.horizontalLayout_4.addWidget(self.Back_btn1)

        self.stacked_main.addWidget(self.page_collect)

        self.horizontalLayout.addWidget(self.stacked_main)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stacked_main.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.order_collect_btn.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\ubb38\uc218\uc9d1", None))
        self.order_check_btn.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\ubb38\uac80\uc218", None))
        self.invoice_send_btn.setText(QCoreApplication.translate("MainWindow", u"\uc1a1\uc7a5 \uc0dd\uc131/\uc804\uc1a1", None))
        self.stock_file.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\uc7ac\uace0 \uac80\uc218\ud30c\uc77c", None))
        self.customer_file.setText(QCoreApplication.translate("MainWindow", u"\uc218\ub839\uc778 \uac80\uc218\ud30c\uc77c", None))
        self.stock_btn.setText(QCoreApplication.translate("MainWindow", u"\uc2e4\uc7ac\uace0 \uac80\uc218", None))
        self.costomer_btn.setText(QCoreApplication.translate("MainWindow", u"\uc218\ub839\uc778 \uac80\uc218", None))
        self.Back_btn2.setText(QCoreApplication.translate("MainWindow", u"\ub4a4\ub85c\uac00\uae30", None))
        self.code.setText(QCoreApplication.translate("MainWindow", u"\ucf54\ub4dc", None))
        self.login_btn.setText(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8\uc778", None))
        self.lotte_upload_btn.setText(QCoreApplication.translate("MainWindow", u"\ub86f\ub370\ud0dd\ubc30 \ud30c\uc77c \uc5c5\ub85c\ub4dc", None))
        self.creat_file_btn.setText(QCoreApplication.translate("MainWindow", u"\ub4f1\ub85d\ud30c\uc77c \uc0dd\uc131", None))
        self.send_invoice_btn.setText(QCoreApplication.translate("MainWindow", u"\uc1a1\uc7a5 \uc804\uc1a1", None))
        self.Back_btn3.setText(QCoreApplication.translate("MainWindow", u"\ub4a4\ub85c\uac00\uae30", None))
        self.start_order_btn.setText(QCoreApplication.translate("MainWindow", u"\uc8fc\ubb38\uc218\uc9d1 \uc2dc\uc791", None))
        self.Back_btn1.setText(QCoreApplication.translate("MainWindow", u"\ub4a4\ub85c\uac00\uae30", None))
    # retranslateUi


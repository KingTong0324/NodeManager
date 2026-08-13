# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NodeManager.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QWidget)

class Ui_NodeManager(object):
    def setupUi(self, NodeManager):
        if not NodeManager.objectName():
            NodeManager.setObjectName(u"NodeManager")
        NodeManager.resize(933, 500)
        NodeManager.setMinimumSize(QSize(750, 500))
        icon = QIcon()
        icon.addFile(u"NodeManager.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        NodeManager.setWindowIcon(icon)
        self.centralwidget = QWidget(NodeManager)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.inputFrame = QFrame(self.centralwidget)
        self.inputFrame.setObjectName(u"inputFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputFrame.sizePolicy().hasHeightForWidth())
        self.inputFrame.setSizePolicy(sizePolicy)
        self.inputFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.inputFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.inputFrame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.inputBox = QPlainTextEdit(self.inputFrame)
        self.inputBox.setObjectName(u"inputBox")

        self.gridLayout_4.addWidget(self.inputBox, 1, 0, 1, 3)

        self.clearInputButton = QPushButton(self.inputFrame)
        self.clearInputButton.setObjectName(u"clearInputButton")
        font = QFont()
        font.setPointSize(11)
        self.clearInputButton.setFont(font)

        self.gridLayout_4.addWidget(self.clearInputButton, 2, 0, 1, 1)

        self.organizeButton = QPushButton(self.inputFrame)
        self.organizeButton.setObjectName(u"organizeButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.organizeButton.sizePolicy().hasHeightForWidth())
        self.organizeButton.setSizePolicy(sizePolicy1)
        self.organizeButton.setMinimumSize(QSize(100, 32))
        self.organizeButton.setFont(font)

        self.gridLayout_4.addWidget(self.organizeButton, 2, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_2, 2, 1, 1, 1)

        self.inputLabel = QLabel(self.inputFrame)
        self.inputLabel.setObjectName(u"inputLabel")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.inputLabel.setFont(font1)

        self.gridLayout_4.addWidget(self.inputLabel, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.inputFrame, 1, 0, 1, 1)

        self.outputFrame = QFrame(self.centralwidget)
        self.outputFrame.setObjectName(u"outputFrame")
        sizePolicy.setHeightForWidth(self.outputFrame.sizePolicy().hasHeightForWidth())
        self.outputFrame.setSizePolicy(sizePolicy)
        self.outputFrame.setMinimumSize(QSize(0, 0))
        self.outputFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.outputFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.outputFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.clearOutputButton = QPushButton(self.outputFrame)
        self.clearOutputButton.setObjectName(u"clearOutputButton")
        self.clearOutputButton.setFont(font)

        self.gridLayout.addWidget(self.clearOutputButton, 2, 0, 1, 1)

        self.saveNodeButton = QPushButton(self.outputFrame)
        self.saveNodeButton.setObjectName(u"saveNodeButton")
        self.saveNodeButton.setFont(font)

        self.gridLayout.addWidget(self.saveNodeButton, 2, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 2, 1, 1, 1)

        self.outputBox = QPlainTextEdit(self.outputFrame)
        self.outputBox.setObjectName(u"outputBox")

        self.gridLayout.addWidget(self.outputBox, 1, 0, 1, 5)

        self.copyOutputButton = QPushButton(self.outputFrame)
        self.copyOutputButton.setObjectName(u"copyOutputButton")
        self.copyOutputButton.setFont(font)

        self.gridLayout.addWidget(self.copyOutputButton, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 2, 3, 1, 1)

        self.outputLabel = QLabel(self.outputFrame)
        self.outputLabel.setObjectName(u"outputLabel")
        font2 = QFont()
        font2.setPointSize(10)
        self.outputLabel.setFont(font2)
        self.outputLabel.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.gridLayout.addWidget(self.outputLabel, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.outputFrame, 1, 1, 1, 1)

        self.savedFrame = QFrame(self.centralwidget)
        self.savedFrame.setObjectName(u"savedFrame")
        sizePolicy.setHeightForWidth(self.savedFrame.sizePolicy().hasHeightForWidth())
        self.savedFrame.setSizePolicy(sizePolicy)
        self.savedFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.savedFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.savedFrame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.savedList = QListWidget(self.savedFrame)
        self.savedList.setObjectName(u"savedList")

        self.gridLayout_2.addWidget(self.savedList, 1, 0, 1, 4)

        self.libraryLabel = QLabel(self.savedFrame)
        self.libraryLabel.setObjectName(u"libraryLabel")
        self.libraryLabel.setFont(font2)

        self.gridLayout_2.addWidget(self.libraryLabel, 0, 0, 1, 1)

        self.copyLibraryButton = QPushButton(self.savedFrame)
        self.copyLibraryButton.setObjectName(u"copyLibraryButton")
        self.copyLibraryButton.setFont(font)

        self.gridLayout_2.addWidget(self.copyLibraryButton, 3, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 3, 1, 1, 1)

        self.deleteNodeButton = QPushButton(self.savedFrame)
        self.deleteNodeButton.setObjectName(u"deleteNodeButton")
        self.deleteNodeButton.setFont(font)

        self.gridLayout_2.addWidget(self.deleteNodeButton, 3, 3, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 3, 2, 1, 1)


        self.gridLayout_3.addWidget(self.savedFrame, 1, 2, 1, 1)

        self.topFrame = QFrame(self.centralwidget)
        self.topFrame.setObjectName(u"topFrame")
        self.topFrame.setMinimumSize(QSize(0, 40))
        self.topFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.topFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.topFrame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.themeButton = QPushButton(self.topFrame)
        self.themeButton.setObjectName(u"themeButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.themeButton.sizePolicy().hasHeightForWidth())
        self.themeButton.setSizePolicy(sizePolicy2)
        self.themeButton.setMinimumSize(QSize(25, 25))

        self.gridLayout_5.addWidget(self.themeButton, 0, 2, 1, 1)

        self.label = QLabel(self.topFrame)
        self.label.setObjectName(u"label")
        self.label.setFont(font2)

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.topFrame, 0, 0, 1, 3)

        NodeManager.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(NodeManager)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 933, 33))
        NodeManager.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(NodeManager)
        self.statusbar.setObjectName(u"statusbar")
        NodeManager.setStatusBar(self.statusbar)

        self.retranslateUi(NodeManager)

        QMetaObject.connectSlotsByName(NodeManager)
    # setupUi

    def retranslateUi(self, NodeManager):
        NodeManager.setWindowTitle(QCoreApplication.translate("NodeManager", u"NodeManager 0.02.0", None))
        self.clearInputButton.setText(QCoreApplication.translate("NodeManager", u"\u6e05\u7a7a\u8f93\u5165", None))
        self.organizeButton.setText(QCoreApplication.translate("NodeManager", u"\u6574\u7406", None))
        self.inputLabel.setText(QCoreApplication.translate("NodeManager", u"\u8f93\u5165\u5185\u5bb9", None))
        self.clearOutputButton.setText(QCoreApplication.translate("NodeManager", u"\u6e05\u7a7a\u8f93\u51fa", None))
        self.saveNodeButton.setText(QCoreApplication.translate("NodeManager", u"\u4fdd\u5b58\u8282\u70b9", None))
        self.copyOutputButton.setText(QCoreApplication.translate("NodeManager", u"\u590d\u5236", None))
        self.outputLabel.setText(QCoreApplication.translate("NodeManager", u"\u8f93\u51fa\u5185\u5bb9", None))
        self.libraryLabel.setText(QCoreApplication.translate("NodeManager", u"\u8282\u70b9\u5e93", None))
        self.copyLibraryButton.setText(QCoreApplication.translate("NodeManager", u"\u590d\u5236", None))
        self.deleteNodeButton.setText(QCoreApplication.translate("NodeManager", u"\u5220\u9664", None))
        self.themeButton.setText(QCoreApplication.translate("NodeManager", u"\u989c\u8272", None))
        self.label.setText(QCoreApplication.translate("NodeManager", u"\u6ce8\uff1a\u4e2a\u4eba\u81ea\u7528\u5de5\u5177\uff0c\u8bf7\u52ff\u7528\u4e8e\u5546\u4e1a\u7528\u9014\u3002", None))
    # retranslateUi


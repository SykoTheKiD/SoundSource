# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manageLibrariesDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QStandardItemModel, QStandardItem)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget, QFileDialog)

class Ui_ManageFoldersDialog(object):
    def setupUi(self, ManageFoldersDialog, currentLibraries=set()):
        if not ManageFoldersDialog.objectName():
            ManageFoldersDialog.setObjectName(u"ManageFoldersDialog")
        ManageFoldersDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ManageFoldersDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.folderListView = QListWidget(ManageFoldersDialog)
        self.folderListView.setObjectName(u"folderListView")
        self.folderListView.setAcceptDrops(True)
        self.folderListView.setDragEnabled(True)
        self.folderListView.setDragDropMode(QAbstractItemView.DropOnly)
        self.verticalLayout.addWidget(self.folderListView)

        self.addFolderButton = QPushButton(ManageFoldersDialog)
        self.addFolderButton.setObjectName(u"addFolderButton")
        self.addFolderButton.clicked.connect(self.addFolderPrompt)

        self.verticalLayout.addWidget(self.addFolderButton)

        self.removeFolderButton = QPushButton(ManageFoldersDialog)
        self.removeFolderButton.setObjectName(u"removeFolderButton")
        self.removeFolderButton.setDisabled(True)
        self.removeFolderButton.clicked.connect(self.removeFolder)

        self.folderListView.itemSelectionChanged.connect(self.disableRemoveButton)

        self.verticalLayout.addWidget(self.removeFolderButton)
        self.retranslateUi(ManageFoldersDialog)

        self.currentLibraries = currentLibraries

        QMetaObject.connectSlotsByName(ManageFoldersDialog)
    # setupUi
    def addFolderPrompt(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file not in self.currentLibraries:
            self.folderListView.addItem(file)
            self.currentLibraries.add(file)
    
    def disableRemoveButton(self):
        self.removeFolderButton.setDisabled(len(self.folderListView.selectedItems()) == 0)
    
    def removeFolder(self):
        self.folderListView.takeItem(self.folderListView.currentRow())

    def retranslateUi(self, ManageFoldersDialog):
        ManageFoldersDialog.setWindowTitle(QCoreApplication.translate("ManageFoldersDialog", u"Manage Libraries", None))
        self.addFolderButton.setText(QCoreApplication.translate("ManageFoldersDialog", u"Add Folder", None))
        self.removeFolderButton.setText(QCoreApplication.translate("ManageFoldersDialog", u"Remove Folder", None))
    # retranslateUi


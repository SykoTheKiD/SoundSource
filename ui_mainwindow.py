# -*- coding: utf-8 -*-

from operator import index
from PySide6.QtCore import (QCoreApplication,
    QMetaObject, QRect, QUrl,
    QSize, Qt, QSortFilterProxyModel, Signal)
from PySide6.QtGui import (QAction, QDrag)
from PySide6.QtWidgets import (QLabel, QLineEdit,
    QMenu, QMenuBar, QProgressBar,
    QStatusBar, QTableView, QVBoxLayout,
    QWidget, QAbstractItemView)
import os
from audioplayer import AudioPlayer

class SampleLibraryTableView(QTableView):
    dragSignal = Signal(object)
    def __init__(self, parent = None) -> None:
        super(SampleLibraryTableView, self).__init__(parent)
        self.setDragDropMode(QAbstractItemView.DragOnly)
    
    def startDrag(self, event):
        self.dragSignal.emit(event)

class CustomQueryFilterModel(QSortFilterProxyModel):
    def __init__(self, parent=None) -> None:
        super(CustomQueryFilterModel, self).__init__(parent)
        self.queryString = None
    
    def setFilterFixedString(self, pattern: str) -> None:
        self.queryString = pattern.lower()
        return super().setFilterFixedString(pattern)
    
    def filterAcceptsRow(self, source_row, source_parent) -> bool:
        if self.queryString is None:
            return True
        queryParts = self.queryString.split(" ")
        library_index = self.sourceModel().index(source_row, 0, source_parent)
        category_index = self.sourceModel().index(source_row, 1, source_parent)
        sample_index = self.sourceModel().index(source_row, 2, source_parent)
        for queryPart in queryParts:
            if not (
                queryPart in self.sourceModel().data(library_index, Qt.ItemDataRole.DisplayRole).lower() or
                queryPart in self.sourceModel().data(category_index, Qt.ItemDataRole.DisplayRole).lower() or
                queryPart in self.sourceModel().data(sample_index, Qt.ItemDataRole.DisplayRole).lower()):
                return False
        return True

        
class Ui_mainWindow(object):
    def __init__(self) -> None:
        self.sampleTableView = None

    def setupUi(self, mainWindow):
        if not mainWindow.objectName():
            mainWindow.setObjectName(u"mainWindow")
        mainWindow.resize(800, 600)
        self.actionAdd_Directory = QAction(mainWindow)
        self.actionAdd_Directory.setObjectName(u"actionAdd_Directory")
        self.actionOptions = QAction(mainWindow)
        self.actionOptions.setObjectName(u"actionOptions")
        self.actionClose = QAction(mainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionKeep_On_Top = QAction(mainWindow)
        self.actionKeep_On_Top.setObjectName(u"actionKeep_On_Top")
        self.actionHide_Frame = QAction(mainWindow)
        self.actionHide_Frame.setObjectName(u"actionHide_Frame")
        self.actionEdit_Columns = QAction(mainWindow)
        self.actionEdit_Columns.setObjectName(u"actionEdit_Columns")
        self.actionAbout = QAction(mainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setObjectName(u"mainLayout")
        self.searchField = QLineEdit(self.centralwidget)
        self.searchField.setObjectName(u"searchField")
        self.searchField.setMinimumSize(QSize(0, 25))
        self.searchField.setMaximumSize(QSize(16777215, 16777215))
        self.searchField.setClearButtonEnabled(True)

        self.mainLayout.addWidget(self.searchField)

        self.sampleTableView = SampleLibraryTableView(self.centralwidget)
        self.sampleTableView.setObjectName(u"sampleTableView")
        
        self.sampleTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.sampleTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sampleTableView.horizontalHeader().setStretchLastSection(True) 
        self.sampleTableView.horizontalHeader().setHighlightSections(False)
        self.sampleTableView.verticalHeader().setVisible(False)

        self.mainLayout.addWidget(self.sampleTableView)

        self.messageLabel = QLabel(self.centralwidget)
        self.messageLabel.setObjectName(u"messageLabel")

        self.mainLayout.addWidget(self.messageLabel)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.mainLayout.addWidget(self.progressBar)

        self.verticalLayout_5.addLayout(self.mainLayout)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 43))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName(u"statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionAdd_Directory)
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionAbout)
        self.menuOptions.addAction(self.actionKeep_On_Top)
        self.menuOptions.addAction(self.actionHide_Frame)
        self.menuOptions.addAction(self.actionEdit_Columns)

        self.retranslateUi(mainWindow)

        self.audioplayer = None
        self.playAudio = True

        QMetaObject.connectSlotsByName(mainWindow)
    # setupUi

    def processDrag(self, event):
        indexes = self.sampleTableView.selectedIndexes()
        row = indexes[0].row()
        if row < len(self.model._data):
            drag = QDrag(self)
            mime = self.sampleTableView.model().mimeData(indexes)
            urlList = []
            urlList.append(QUrl.fromLocalFile(self.model._data[row].filePath))
            mime.setUrls(urlList)
            drag.setMimeData(mime)
            drag.exec_(event)

    def on_selectionChanged(self, row, des):
        selected = self.proxy_model.mapToSource(row)
        row = selected.row()
        if row < len(self.model._data):
            if self.playAudio:
                if self.audioplayer is not None:
                    self.audioplayer.stop()
                self.audioplayer = AudioPlayer(os.path.join(self.model._data[row].libraryPath, self.model._data[row].filePath))
                self.audioplayer.play()


    def setTableViewModel(self, model):
        self.proxy_model = CustomQueryFilterModel()
        self.proxy_model.setFilterKeyColumn(-1) # Search all columns.
        self.proxy_model.setSourceModel(model)
        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.model = model
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.sampleTableView.setModel(self.proxy_model)
        selection_model = self.sampleTableView.selectionModel()
        selection_model.currentChanged.connect(self.on_selectionChanged)
        self.searchField.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.searchField.textChanged.connect(self.disconnect_audio)
        self.searchField.editingFinished.connect(self.connect_audio)
        self.sampleTableView.dragSignal.connect(self.processDrag)
    
    def disconnect_audio(self):
        self.playAudio = False
    
    def connect_audio(self):
        self.playAudio = True

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"SoundSource", None))
        self.actionAdd_Directory.setText(QCoreApplication.translate("mainWindow", u"Add Directory", None))
        self.actionOptions.setText(QCoreApplication.translate("mainWindow", u"Options", None))
        self.actionClose.setText(QCoreApplication.translate("mainWindow", u"Close", None))
        self.actionKeep_On_Top.setText(QCoreApplication.translate("mainWindow", u"Keep On Top", None))
        self.actionHide_Frame.setText(QCoreApplication.translate("mainWindow", u"Hide Frame", None))
        self.actionEdit_Columns.setText(QCoreApplication.translate("mainWindow", u"Edit Columns", None))
        self.actionAbout.setText(QCoreApplication.translate("mainWindow", u"About", None))
        self.searchField.setPlaceholderText(QCoreApplication.translate("mainWindow", u"Search...", None))
        self.messageLabel.setText(QCoreApplication.translate("mainWindow", u"TextLabel", None))
        self.menuFile.setTitle(QCoreApplication.translate("mainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("mainWindow", u"Help", None))
        self.menuOptions.setTitle(QCoreApplication.translate("mainWindow", u"Options", None))
import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt, Signal
from ui_mainwindow import Ui_mainWindow
from manageLibrariesDialog import Ui_ManageFoldersDialog
import os
import re
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, libraries):
        super(TableModel, self).__init__()
        self.libraries = libraries
        data = self.processLibraries(libraries)
        self._data = data

    def headerData(self, index, QtOrientation, role=None):
        if role == Qt.DisplayRole and QtOrientation==Qt.Horizontal:
            header = ['Library', 'Category', 'Sample']
            return header[index]
        else:
            return QtCore.QAbstractTableModel.headerData(self, index, QtOrientation, role)

    def processLibraries(self, libraries):
        ret = []
        audio_regex = re.compile(r'.mp3|.wav|.flac|.midi')
        for library in libraries:
            for (dirpath, _, filenames) in os.walk(library):
                for file in filenames:
                    if audio_regex.search(file):
                        path = os.path.join(dirpath, file)
                        path = re.sub(library + "/", "", path)
                        pathParts = path.split("/")
                        if len(pathParts) > 1:
                            libraryName = pathParts[0]
                            category = "/".join(pathParts[1:-1])
                            sampleName = file.split('.')[0]
                            sample = SampleFile(library=libraryName, sample=sampleName, filePath=path, libraryPath=library, category=category)
                            ret.append(sample)
        return ret


    def flags(self, index) -> Qt.ItemFlags:
        flags = super().flags(index)
        if index.isValid():
            flags |= Qt.ItemIsDragEnabled
        return flags

    def data(self, index, role):
        row = index.row()
        if role == Qt.ItemDataRole.DisplayRole and row < len(self._data):
            sampleFile = self._data[row]
            column = index.column()
            if column == 0:
                return sampleFile.library
            elif column == 1:
                return sampleFile.category
            else:
                return sampleFile.sample
    
    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 3
    
class SampleFile:
    def __init__(self, library, sample, filePath, libraryPath, category="-") -> None:
        self.library = library
        self.category = category
        self.sample = sample
        self.filePath = filePath
        self.libraryPath = libraryPath
    
    def __repr__(self) -> str:
        return self.library + " " + self.category + " " + self.sample

data = ["/Users//Downloads/son"]

model = TableModel(data)

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setTableViewModel(model)
        self.actionAdd_Directory.triggered.connect(self.launchManageLibrariesDialog)
    
    def launchManageLibrariesDialog(self):
        dlg = ManageLibrariesDialog();
        dlg.closeSignal.connect(self.addLibraries)
        dlg.exec()
    
    def addLibraries(self, libraries):
        print(libraries)

class ManageLibrariesDialog(QtWidgets.QDialog, Ui_ManageFoldersDialog):
    closeSignal = Signal(object)
    def __init__(self) -> None:
        super(ManageLibrariesDialog, self).__init__()
        self.setupUi(self)
    
    def closeEvent(self, event):
        self.closeSignal.emit(self.currentLibraries)
        event.accept()

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
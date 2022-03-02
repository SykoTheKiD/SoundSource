import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from ui_mainwindow import Ui_mainWindow

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.setHeaderData(0, Qt.Horizontal, "Library")
        self.setHeaderData(1, Qt.Horizontal, "Category")
        self.setHeaderData(2, Qt.Horizontal, "Sample")

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
    def __init__(self, library, sample, filePath, category="-") -> None:
        self.library = library
        self.category = category
        self.sample = sample
        self.filePath = filePath

data = [
SampleFile("jim", "jones", "capo", "path1"),
SampleFile("drizzy", "drake", "dre", "path2"),
SampleFile("abel", "abe", "test", "path3"),
SampleFile("tess", "jimmy", "cartman", "path4"),
SampleFile("carter", "capol", "draker", "path5"),
]

model = TableModel(data)

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setTableViewModel(model)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from ui_mainwindow import Ui_mainWindow

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


data = [
["jim", "jones", "capo"],
["drizzy", "drake", "dre"],
["abel", "abe", "test"],
["tess", "jimmy", "cartman"],
["carter", "capol", "draker"],
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
app.exec_()
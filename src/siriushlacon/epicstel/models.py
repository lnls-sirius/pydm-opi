from bson.objectid import ObjectId
from qtpy import QtCore


class TableModel(QtCore.QAbstractTableModel):
    data_changed = QtCore.Signal(object, str, ObjectId)

    def __init__(self, data, header):
        super(TableModel, self).__init__()
        self._data = data
        self._header = header

    def setHeader(self, index, new_value):
        self._header[index] = new_value

    def deleteHeader(self, index, new_value):
        self._header.pop(index)
        for data_row in self._data:
            data_row.pop(index)

        self.layoutChanged.emit()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._header[section]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self._data[index.row()][index.column()]

    def getRow(self, index):
        return self._data[index.row()]

    def deleteRow(self, index):
        return self._data.pop(index.row())

    def deleteRows(self, indexes):
        indexes = [i.row() for i in indexes]
        self._data = [v for i, v in enumerate(self._data) if i not in indexes]

    def getHeaders(self):
        return self._header

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.data_changed.emit(
                value, self._header[index.column()], self._data[index.row()][0]
            )
            return True

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsEditable
        )

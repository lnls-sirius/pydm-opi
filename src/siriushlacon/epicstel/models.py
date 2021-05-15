from PyQt5 import QtCore


class PvTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, header, parent_table):
        super(PvTableModel, self).__init__()
        self._data = data
        self._header = header
        self._p_table = parent_table

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._header[section]

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self._data[index.column()][index.row()]

    def setData(self, index, value, role, edit_all=False):
        if role == QtCore.Qt.EditRole:
            p_index = self._p_table.selectedIndexes()[0]
            p_model = self._p_table.model()

            self._data[index.column()][index.row()] = value
            if edit_all:
                p_model.setData(
                    p_index.siblingAtColumn(3),
                    ";".join(self._data[1]),
                    QtCore.Qt.EditRole,
                )
                p_model.setData(
                    p_index.siblingAtColumn(2),
                    ";".join(self._data[1]),
                    QtCore.Qt.EditRole,
                )
            elif p_index.column() != 1:
                p_model.setData(p_index, ";".join(self._data[1]), QtCore.Qt.EditRole)

            p_model.setData(
                p_index.siblingAtColumn(1), ";".join(self._data[0]), QtCore.Qt.EditRole
            )

            p_model.layoutChanged.emit()
            return True

    def rowCount(self, index):
        return len(self._data[0])

    def columnCount(self, index):
        return len(self._data)

    def flags(self, index):
        return (
            QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsEditable
        )


class TableModel(QtCore.QAbstractTableModel):
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

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self._data[index.row()][index.column()] = value
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

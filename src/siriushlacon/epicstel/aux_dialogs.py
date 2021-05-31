import logging

from qtpy import QtCore, QtWidgets, uic

from siriushlacon.epicstel.consts import EPICSTEL_GROUP_UI, EPICSTEL_LOGIN_UI

logger = logging.getLogger()


class Login(QtWidgets.QDialog):
    logged_in = QtCore.Signal(tuple)

    def __init__(self, parent=None, macros=None, args=None):
        super(Login, self).__init__()
        uic.loadUi(EPICSTEL_LOGIN_UI, self)
        self.show()

        self.button_box.accepted.connect(self.handle_login)
        self.button_box.rejected.connect(self.destroy)

    def handle_login(self):
        self.logged_in.emit((self.username.text(), self.password.text()))


class EditGroup(QtWidgets.QDialog):
    group_edited = QtCore.Signal(str)
    group_deleted = QtCore.Signal(str)

    def __init__(self, group, parent=None, macros=None, args=None):
        super(EditGroup, self).__init__()
        uic.loadUi(EPICSTEL_GROUP_UI, self)
        self.show()

        self.group_edit.setText(group)

        self.button_box.accepted.connect(self.handle_edit_group)
        self.button_box.rejected.connect(self.destroy)
        self.delete_btn.clicked.connect(self.handle_delete_group)

    def handle_edit_group(self):
        self.group_edited.emit(self.group_edit.text())

    def handle_delete_group(self):
        self.group_deleted.emit(self.group_edit.text())
        self.destroy()

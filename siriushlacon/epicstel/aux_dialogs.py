from qtpy import QtWidgets, QtCore, uic

from qtpy.QtWidgets import QMessageBox

import logging
import requests

from siriushlacon.epicstel.consts import (
    EPICSTEL_LOGIN_UI,
    EPICSTEL_GROUP_UI,
)

logger = logging.getLogger()


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None, macros=None, args=None):
        super(Login, self).__init__()
        uic.loadUi(EPICSTEL_LOGIN_UI, self)
        self.show()

        self.button_box.accepted.connect(self.handle_login)
        self.button_box.rejected.connect(self.destroy)

    def handle_login(self):
        try:
            response = requests.post(
                "https://10.0.38.42/mgmt/bpl/login",
                data={
                    "username": self.username.text(),
                    "password": self.password.text(),
                },
                verify=False,
            )
        except ConnectionError:
            QMessageBox.critical(
                self,
                "Could not authenticate",
                "The program could not connect itself to the remote authentication server.",
                QMessageBox.Ok,
            )

            logger.error("Could not connect to authentication server.")

        if "authenticated" in response.text:
            self.accept()
        else:
            QMessageBox.information(
                self,
                "Invalid credentials",
                "Invalid credentials",
                QMessageBox.Ok,
            )
            self.destroy()


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

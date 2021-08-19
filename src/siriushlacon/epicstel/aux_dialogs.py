import logging

from bson.objectid import ObjectId
from PyQt5.QtGui import QIntValidator, QKeySequence
from PyQt5.QtWidgets import QShortcut
from qtpy import QtCore, QtWidgets, uic

from siriushlacon.epicstel.consts import (
    EPICSTEL_ITEMS_UI,
    EPICSTEL_LOGIN_UI,
    EPICSTEL_PV_UI,
    EPICSTEL_TEAM_UI,
    EPICSTEL_USER_UI,
)

logger = logging.getLogger()


class Login(QtWidgets.QDialog):
    logged_in = QtCore.Signal(tuple)

    def __init__(self, parent=None, macros=None, args=None):
        super(Login, self).__init__()
        uic.loadUi(EPICSTEL_LOGIN_UI, self)

        self.button_box.accepted.connect(self.handle_login)
        self.button_box.rejected.connect(self.destroy)
        self.show()

    def handle_login(self):
        self.logged_in.emit((self.username.text(), self.password.text()))


class AddUser(QtWidgets.QDialog):
    add_user = QtCore.Signal(tuple)

    def __init__(self, teams: list):
        super(AddUser, self).__init__()
        uic.loadUi(EPICSTEL_USER_UI, self)

        self.team_combobox.addItems(teams)
        self.id_box.setValidator(QIntValidator())
        self.add_user_btn_box.accepted.connect(self.handle_add_user)
        self.add_user_btn_box.rejected.connect(self.destroy)
        self.show()

    def handle_add_user(self):
        self.add_user.emit(
            (
                self.name_box.text(),
                int(self.id_box.text()),
                self.team_combobox.currentText(),
            )
        )


class AddPV(QtWidgets.QDialog):
    add_pv = QtCore.Signal(tuple)

    def __init__(self, groups: list):
        super(AddPV, self).__init__()
        uic.loadUi(EPICSTEL_PV_UI, self)

        self.group_combobox.addItems(groups)
        self.add_pv_btn_box.accepted.connect(self.handle_add_pv)
        self.add_pv_btn_box.rejected.connect(self.destroy)
        self.show()

    def handle_add_pv(self):
        self.add_pv.emit(
            (
                self.name_box.text(),
                float(self.min_box.text()),
                float(self.max_box.text()),
                float(self.timeout_box.text().split(" ")[0]),
                self.group_combobox.currentText(),
            )
        )


class AddTeam(QtWidgets.QDialog):
    add_team = QtCore.Signal(tuple)

    def __init__(self, users: list):
        super(AddTeam, self).__init__()
        uic.loadUi(EPICSTEL_TEAM_UI, self)
        self.users = users

        self.admin_combobox.addItems(users)
        self.users_combobox.addItems(users)
        self.add_team_btn_box.accepted.connect(self.handle_add_team)
        self.add_team_btn_box.rejected.connect(self.destroy)

        self.del_sc = QShortcut(QKeySequence("Del"), self)
        self.del_sc.activated.connect(self.del_user)

        self.add_btn.clicked.connect(self.add_user)
        self.show()

    def del_user(self):
        new_user_list = [
            self.users_list.item(i).text() for i in range(self.users_list.count())
        ]
        new_user_list.remove(self.users_list.currentItem().text())

        self.users_list.clear()
        self.users_list.addItems(new_user_list)

        self.users_combobox.clear()
        self.users_combobox.addItems(set(self.users) ^ set(new_user_list))

    def add_user(self):
        self.users_list.addItem(self.users_combobox.currentText())

        listed_users_set = set(
            [self.users_list.item(i).text() for i in range(self.users_list.count())]
        )

        self.users_combobox.clear()
        self.users_combobox.addItems(set(self.users) ^ listed_users_set)

    def handle_add_team(self):
        self.add_team.emit(
            (
                self.name_box.text(),
                self.admin_combobox.currentText(),
                [
                    self.users_list.item(i).text()
                    for i in range(self.users_list.count())
                ],
            )
        )


class EditItems(QtWidgets.QDialog):
    edit_items = QtCore.Signal(ObjectId, list, str, str)

    def __init__(
        self, id: ObjectId, prev_items: list, items: list, tab: str, field: str
    ):
        super(EditItems, self).__init__()
        uic.loadUi(EPICSTEL_ITEMS_UI, self)
        self.items, self.tab, self.field, self.id = items, tab, field, id

        self.items_list.addItems(prev_items)
        self.items_combobox.addItems(set(items) ^ set(prev_items))

        self.btn_box.accepted.connect(self.handle_edit_items)
        self.btn_box.rejected.connect(self.destroy)

        self.del_sc = QShortcut(QKeySequence("Del"), self)
        self.del_sc.activated.connect(self.del_item)
        self.add_btn.clicked.connect(self.add_item)
        self.show()

    def del_item(self):
        new_items_list = [
            self.items_list.item(i).text() for i in range(self.items_list.count())
        ]
        new_items_list.remove(self.items_list.currentItem().text())

        self.items_list.clear()
        self.items_list.addItems(new_items_list)

        self.items_combobox.clear()
        self.items_combobox.addItems(set(self.items) ^ set(new_items_list))

    def add_item(self):
        self.items_list.addItem(self.items_combobox.currentText())

        listed_users_set = set(
            [self.items_list.item(i).text() for i in range(self.items_list.count())]
        )

        self.items_combobox.clear()
        self.items_combobox.addItems(set(self.items) ^ listed_users_set)

    def handle_edit_items(self):
        self.edit_items.emit(
            self.id,
            [self.items_list.item(i).text() for i in range(self.items_list.count())],
            self.tab,
            self.field,
        )

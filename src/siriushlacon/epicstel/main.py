import logging
import sys

from aux_dialogs import AddPV, AddTeam, AddUser, EditItems, Login
from models import TableModel
from pydm import Display
from pymongo import MongoClient, errors
from PyQt5.QtGui import QKeySequence, QRegExpValidator
from qtpy.QtCore import QRegExp, Qt, QThread, Signal
from qtpy.QtWidgets import (
    QApplication,
    QComboBox,
    QItemDelegate,
    QMainWindow,
    QMessageBox,
    QShortcut,
)

from siriushlacon.epicstel.consts import EPICSTEL_HOST, EPICSTEL_MAIN_UI, EPICSTEL_TABS

logger = logging.getLogger()


class UpdateTableThread(QThread):
    finished = Signal(dict)

    def __init__(self, db):
        QThread.__init__(self)
        self.db = db

    def __del__(self):
        self.wait()

    def run(self):
        tables = {}
        for table in EPICSTEL_TABS[:3]:
            items = list(self.db[table].find())
            headers = list(items[0].keys())
            data = []

            for doc in items:
                row = []
                for header in headers:
                    item = doc[header]

                    if type(item) == list:
                        if len(item) and type(item[0]) == dict:
                            row.append(
                                ",".join(
                                    [
                                        "{} ({})".format(
                                            (list(i.values())[:2])[0],
                                            (list(i.values())[:2])[1],
                                        )
                                        for i in item
                                    ]
                                )
                            )
                        else:
                            row.append(",".join(item))
                    else:
                        row.append(item)
                data.append(row)

            tables[table] = (headers, data)

        self.finished.emit(tables)


class Delegate(QItemDelegate):
    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices

    def createEditor(self, parent, option, index):
        self.editor = QComboBox(parent)
        self.editor.addItems(self.items)
        return self.editor

    def setEditorData(self, editor, index):
        value = index.data(Qt.DisplayRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class Window(Display, QMainWindow):
    def open(self, credentials):
        client = MongoClient(EPICSTEL_HOST)

        try:
            client.admin.authenticate(credentials[0], credentials[1])
            client.server_info()
            self.db = client.epicstel

            self.update_thread = UpdateTableThread(self.db)
            self.update_thread.finished.connect(self.display_table)

            self.refresh_btn.clicked.connect(self.update_table)
            self.first = True
            self.update_table()
        except errors.OperationFailure:
            QMessageBox.critical(
                self,
                "Could not authenticate",
                "Invalid credentials",
                QMessageBox.Ok,
            )
            self.login_remote()

    def cell_clicked(self, args, tab):
        col = args.column()
        if tab == "pvs" and col == 2:
            self.pvs_table.setItemDelegateForColumn(
                2, Delegate(self.pvs_table.model(), list(self.db.pvs.distinct("group")))
            )
            self.pvs_table.openPersistentEditor(args)
        elif (tab == "users" and col not in [1, 3]) or (tab == "teams" and col != 1):
            model = getattr(self, tab + "_table").model()
            previous_data = list(filter(lambda x: x, model.data(args).split(",")))
            mongo_id = model.data(model.index(args.row(), 0))

            if (tab == "users" and col == 5) or (tab == "teams" and col == 2):
                pvs = [
                    "{} ({})".format(p.get("name"), p.get("group"))
                    for p in self.db.pvs.find()
                ]
                dialog = EditItems(mongo_id, previous_data, pvs, tab, "pvs")
            elif tab == "users" and col == 6:
                dialog = EditItems(
                    mongo_id,
                    previous_data,
                    self.db.teams.distinct("team"),
                    tab,
                    "teams",
                )
            elif tab == "users" and col == 2:
                dialog = EditItems(
                    mongo_id,
                    previous_data,
                    self.db.teams.distinct("team"),
                    tab,
                    "adminof",
                )
            else:
                dialog = EditItems(
                    mongo_id,
                    previous_data,
                    self.db.pvs.distinct("group"),
                    tab,
                    "groups",
                )

            dialog.edit_items.connect(self.edit_items)
            dialog.show()

    def edit_items(self, id, values, tab, field):
        if field == "pvs":
            pvs = {"pvs": []}
            for pv in values:
                splitted = pv.split(" ")
                name, group = splitted[0], splitted[1][1:-1]
                pv_id = self.db.pvs.find_one({"name": name, "group": group}).get("_id")
                pvs["pvs"].append({"name": name, "group": group, "ext_id": pv_id})

            self.db.users.update_one({"_id": id}, {"$set": pvs})
        else:
            self.db[tab].update_one({"_id": id}, {"$set": {field: values}})
        self.update_table()

    def del_ca_addr(self):
        for index in self.ca_addr_list.selectedIndexes():
            self.ca_addr_list.takeItem(index.row())

        self.update_ca_addr()

    def del_team(self, args):
        indexes = self.teams_table.selectedIndexes()
        model = self.teams_table.model()
        team_i = model.getHeaders().index("team")
        teams = list(set([model.getRow(index)[team_i] for index in indexes]))

        self.db.teams.delete_many({"team": {"$in": teams}})
        self.db.users.update_many(
            {"teams": {"$in": teams}}, {"$pullAll": {"teams": teams, "adminof": teams}}
        )

        self.update_table()

    def del_pv(self, args):
        indexes = self.pvs_table.selectedIndexes()
        model = self.pvs_table.model()
        group_i, name_i = model.getHeaders().index("group"), model.getHeaders().index(
            "name"
        )

        groups, pvs = [], []

        for index in indexes:
            row = model.getRow(index)
            groups.append(row[group_i])
            pvs.append(row[name_i])

        groups, pvs = list(set(groups)), list(set(pvs))

        self.db.pvs.delete_many({"group": {"$in": groups}, "name": {"$in": pvs}})
        self.db.users.update_many(
            {}, {"$pull": {"pvs": {"group": groups, "name": pvs}}}
        )
        self.db.teams.update_many(
            {}, {"$pull": {"pvs": {"group": groups, "name": pvs}}}
        )

        self.update_table()

    def del_user(self, args):
        indexes = self.users_table.selectedIndexes()
        model = self.users_table.model()
        ids = list(set([model.getRow(index)[0] for index in indexes]))

        self.db.users.delete_many({"_id": {"$in": ids}})
        self.update_table()

    def show_add_dialog(self, args):
        if args == "user":
            dialog = AddUser([t.get("team") for t in self.db.teams.find()])
        elif args == "pv":
            dialog = AddPV(self.db.pvs.distinct("group"))
        elif args == "team":
            dialog = AddTeam(
                [
                    "{} ({})".format(u.get("fullname"), u.get("chat_id"))
                    for u in self.db.users.find()
                ]
            )

        add_type = "add_" + args
        getattr(dialog, add_type).connect(lambda c: getattr(self, add_type)(c))
        dialog.show()

    def update_ca_addr(self):
        ips = [
            self.ca_addr_list.item(i).text() for i in range(self.ca_addr_list.count())
        ]
        self.db.configs.update_one(
            {"config": "EPICS_CA_ADDR_LIST"}, {"$set": {"ips": ips}}
        )
        self.update_table()

    def add_ca_addr(self, args):
        self.ca_addr_list.addItem(self.ca_addr_input.text())
        self.update_ca_addr()

    def add_user(self, args):
        if self.db.users.find_one({"chat_id": args[1]}):
            QMessageBox.critical(
                self,
                "Invalid Chat ID",
                "{} already exists in the user database".format(args[1]),
                QMessageBox.Ok,
            )
            self.show_add_dialog("user")
            return

        self.db.users.insert_one(
            {
                "chat_id": args[1],
                "pvs": [],
                "groups": [],
                "adminof": [],
                "teams": [args[2]],
                "fullname": args[0],
                "ignore": [],
            }
        )
        self.update_table()

    def add_pv(self, args):
        if self.db.pvs.find_one({"name": args[0], "group": args[4]}):
            QMessageBox.critical(
                self,
                "Invalid Name/Group",
                "{} already exists under the group {} in the PV database".format(
                    args[0], args[4]
                ),
                QMessageBox.Ok,
            )
            self.show_add_dialog("pv")
            return

        if args[2] < args[1] or args[3] <= 0:
            QMessageBox.critical(
                self,
                "Invalid Min/Max",
                "The maximum limit should be greater than the minimum limit",
                QMessageBox.Ok,
            )
            self.show_add_dialog("pv")
            return

        self.db.pvs.insert_one(
            {
                "name": args[0],
                "group": args[4],
                "max": args[2],
                "min": args[1],
                "timeout": args[3],
                "value": 0,
                "last_alert": 0,
                "d_time": 0,
                "d_count": 0,
            }
        )
        self.update_table()

    def add_team(self, args):
        if self.db.teams.find_one({"team": args[0]}):
            QMessageBox.critical(
                self,
                "Invalid Team Name",
                "{} team already exists".format(args[0]),
                QMessageBox.Ok,
            )
            self.show_add_dialog("team")
            return

        adm = args[1].split("(")
        adm[1] = int(adm[1][:-1])

        users = [[u.split("(")[0], int(u.split("(")[1][:-1])] for u in args[2]]
        users.append(adm)

        for user in users:
            self.db.users.update_one(
                {"chat_id": user[1]},
                {
                    "$setOnInsert": {
                        "pvs": [],
                        "groups": [],
                        "adminof": [],
                        "chat_id": user[1],
                        "fullname": user[0],
                    },
                    "$addToSet": {"teams": args[0]},
                },
                upsert=True,
            )

        self.db.teams.insert_one({"team": args[0], "pvs": [], "groups": []})
        self.db.users.update_one(
            {"chat_id": adm[1]}, {"$addToSet": {"adminof": args[0]}}
        )

        self.update_table()

    def login_remote(self):
        logger.info("Logging in...")
        login = Login()
        login.logged_in.connect(lambda c: self.open(c))

        login.show()

    def update_data(self, value, prop, id):
        col = EPICSTEL_TABS[self.tabWidget.currentIndex()]
        if not (
            (col == "users" and prop not in ["chat_id", "fullname"])
            or (col == "teams" and prop != "team")
        ):
            self.db[col].update_one({"_id": id}, {"$set": {prop: value}})
            self.update_table()

    def display_table(self, tables):
        for tab, table in tables.items():
            view = getattr(self, "{}_table".format(tab))
            model = TableModel(table[1], table[0])
            model.data_changed.connect(self.update_data)

            view.setModel(model)
            view.setColumnHidden(0, True)

        self.ca_addr_list.clear()
        self.ca_addr_list.addItems(
            self.db.configs.find_one({"config": "EPICS_CA_ADDR_LIST"}).get("ips")
        )

    def update_table(self):
        editing = (
            self.pvs_table.state() == 3
            or self.users_table.state() == 3
            or self.teams_table.state() == 3
        )
        if not self.update_thread.isRunning() and not editing:
            self.update_thread.start()

    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=EPICSTEL_MAIN_UI)
        self.login_remote()

        self.delete_pv_btn.clicked.connect(self.del_pv)
        self.delete_user_btn.clicked.connect(self.del_user)
        self.delete_team_btn.clicked.connect(self.del_team)

        self.add_user_btn.clicked.connect(lambda: self.show_add_dialog("user"))
        self.add_pv_btn.clicked.connect(lambda: self.show_add_dialog("pv"))
        self.add_team_btn.clicked.connect(lambda: self.show_add_dialog("team"))

        self.pvs_table.clicked.connect(lambda c: self.cell_clicked(c, "pvs"))
        self.teams_table.clicked.connect(lambda c: self.cell_clicked(c, "teams"))
        self.users_table.clicked.connect(lambda c: self.cell_clicked(c, "users"))

        ip_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

        self.ca_addr_input.setValidator(QRegExpValidator(QRegExp(ip_regex)))
        self.del_sc = QShortcut(QKeySequence("Del"), self)
        self.del_sc.activated.connect(self.del_ca_addr)
        self.add_ca_addr_btn.clicked.connect(self.add_ca_addr)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

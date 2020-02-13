import sys
import redis
import json
import time
import socket
#import os
from qtpy import QtCore, QtGui, QtWidgets, uic
#sys.path.append(os.path.abspath("../.."))
from pydm import Display
from siriushlacon.beaglebones.common.network.utils import NetUtils
from siriushlacon.beaglebones.common.entity.entities import Command
from siriushlacon.beaglebones.consts import BEAGLEBONES_MAIN_UI, INFO_BBB_UI, CHANGE_BBB_UI
from siriushlacon.utils.consts import LNLS_INVISIBLE_IMG, CNPEM_INVISIBLE_IMG

#r = redis.StrictRedis(host = "10.0.38.59", port = 6379, db = 0)
r = redis.StrictRedis(host = "10.128.255.4", port = 6379, db = 0)


room_names_ip = {"All":"", "TL":"21", "Connect.":"22", "PS":"23", "RF":"24"}
for i in range(20):
    room_names_ip["IA-{:02d}".format(i+1)] = "{:02d}".format(i+1)

Ui_MainWindow, QtBaseClass = uic.loadUiType(BEAGLEBONES_MAIN_UI)
Ui_MainWindow_change, QtBaseClass_change = uic.loadUiType(CHANGE_BBB_UI)
Ui_MainWindow_info, QtBaseClass_info = uic.loadUiType(INFO_BBB_UI)


class InfoBBB(QtWidgets.QMainWindow, Ui_MainWindow_info):
    def __init__(self, bbb_name="", bbb_info=""):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow_info.__init__(self)
        self.setupUi(self)
        #super().__init__(parent=parent, args=args, macros=macros, ui_filename=INFO_BBB_UI)

        self.title.setText(bbb_name)
        self.textInfo.setText("{}".format(bbb_info))

        self.closeButton.clicked.connect(self.closeWindow)

    def closeWindow(self):
        self.close()


class ChangeBBB(QtWidgets.QMainWindow, Ui_MainWindow_change):
    def __init__(self, bbb_info=""):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow_change.__init__(self)
        self.setupUi(self)

        self.currentIP_value = bbb_info.split(" ")[0]
        self.currentHostname_value = bbb_info.split(" ")[-1]
        self.title.setText(bbb_info)
        self.currentIP.setText(self.currentIP_value)
        self.currentHostname.setText(self.currentHostname_value)

        self.prefixIP_value = self.currentIP_value.rsplit('.',1)[0] + '.'
        self.suffixIP_value = self.currentIP_value.split('.')[-1]

        self.prefixIP.setText(self.prefixIP_value)
        self.suffixIP.setValue(int(self.suffixIP_value))

        self.modeIP.activated.connect(self.IP_buttons)
        self.keepIP.toggled.connect(self.IP_buttons)
        self.keepHostname.toggled.connect(self.Hostname_buttons)

        self.changeButton.clicked.connect(self.updateBBB)


    def updateBBB(self):
        confirmation = QtWidgets.QMessageBox.question(self, 'Confirmation',
                                            "Are you sure?",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if confirmation == QtWidgets.QMessageBox.Yes:
            if not self.keepHostname.isChecked():
                if self.newHostname.text() != "" and self.newHostname.text() != self.currentHostname_value:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.currentIP_value, 9877))
                    NetUtils.send_command(s, Command.SET_HOSTNAME)
                    NetUtils.send_object(s, self.newHostname.text())
                    s.close()
                    time.sleep(1)

            if not self.keepIP.isChecked():
                if "{}".format(self.suffixIP.value()) != self.suffixIP_value or self.modeIP.currentText() == "DHCP":
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.currentIP_value, 9877))
                    NetUtils.send_command(s, Command.SET_NAMESERVERS)
                    NetUtils.send_object(s, "10.0.0.71")
                    NetUtils.send_object(s, "10.0.0.71")
                    s.close()

                    time.sleep(1)

                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.currentIP_value, 9877))
                    NetUtils.send_command(s, Command.SET_IP)
                    NetUtils.send_object(s, self.modeIP.currentText().lower())
                    if self.modeIP.currentText() == "MANUAL":
                        NetUtils.send_object(s, self.prefixIP_value + "{}".format(self.suffixIP.value()))
                        NetUtils.send_object(s, "255.255.255.0")
                        NetUtils.send_object(s, self.prefixIP_value + "1")
                    s.close()
                    time.sleep(1)


            self.close()

    def Hostname_buttons(self):
        if not self.keepHostname.isChecked():
            self.newHostname.setEnabled(True)
        else:
            self.newHostname.setEnabled(False)

        if self.keepHostname.isChecked() and self.keepIP.isChecked():
            self.changeButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)


    def IP_buttons(self):
        if not self.keepIP.isChecked():
            self.modeIP.setEnabled(True)
            if self.modeIP.currentText() == "MANUAL":
                self.prefixIP.setEnabled(True)
                self.suffixIP.setEnabled(True)
            elif self.modeIP.currentText() == "DHCP":
                self.prefixIP.setEnabled(False)
                self.suffixIP.setEnabled(False)
        else:
            self.prefixIP.setEnabled(False)
            self.suffixIP.setEnabled(False)
            self.modeIP.setEnabled(False)

        if self.keepHostname.isChecked() and self.keepIP.isChecked():
            self.changeButton.setEnabled(False)
        else:
            self.changeButton.setEnabled(True)


#class MonitoringBBB(QtWidgets.QMainWindow, Ui_MainWindow):
class MonitoringBBB(Display):
    def __init__(self, parent=None, macros=None, args=None):
        self.items_info = {}
        self.items_state = {}
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        #self.setupUi(self)
        super().__init__(parent=parent, args=args, macros=macros, ui_filename=BEAGLEBONES_MAIN_UI)

        self.cnpem_image.setPixmap(QtGui.QPixmap(CNPEM_INVISIBLE_IMG))
        self.lnls_image.setPixmap(QtGui.QPixmap(LNLS_INVISIBLE_IMG))

        self.room_number.activated.connect(self.ShowNodes)
        self.find_value.returnPressed.connect(self.ShowNodes)
        self.connected_checkBox.toggled.connect(self.ShowNodes)
        self.disconnected_checkBox.toggled.connect(self.ShowNodes)

        self.deleteButton.clicked.connect(self.DeleteButton)
        self.rebootButton.clicked.connect(self.RebootButton)
        self.changeButton.clicked.connect(self.ChangeButton)
        self.infoButton.clicked.connect(self.InfoButton)

        self.list.setSortingEnabled(True)
        self.list.itemSelectionChanged.connect(self.DisplayButtons)


        self.autoUpdate_timer = QtCore.QTimer(self)
        self.autoUpdate_timer.timeout.connect(self.ShowNodes)
        self.autoUpdate_timer.setSingleShot(False)
        self.autoUpdate_timer.start(1000)

    def DeleteButton(self):
        itemsSelected = self.list.selectedItems()

        for item in itemsSelected:
            item_node_name = ("Ping:Node:" + item.text().split(" ")[0]).encode()

            self.items_info.pop(item_node_name)
            self.items_state.pop(item_node_name)

            item_index = self.list.row(item)
            self.list.takeItem(item_index)

    def RebootButton(self):
        confirmation = QtWidgets.QMessageBox.question(self, 'Confirmation',
                                            "Are you sure about rebooting those nodes?",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if confirmation == QtWidgets.QMessageBox.Yes:
            itemsSelected = self.list.selectedItems()
            for item in itemsSelected:
                host_ip = item.text().split(" ")[0]
                if(self.items_state["Ping:Node:{}".format(host_ip).encode()] == True):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host_ip, 9877))
                    NetUtils.send_command(s, Command.REBOOT)
                    s.close()
                    time.sleep(0.1)

    def ChangeButton(self):
        self.window = ChangeBBB(bbb_info = self.list.selectedItems()[0].text())
        self.window.show()

    def InfoButton(self):
        bbb = self.list.selectedItems()[0].text()
        ip = bbb.split(" ")[0]
        self.window = InfoBBB(bbb_name = bbb, bbb_info = self.items_info[("Ping:Node:"+ip).encode()])
        self.window.show()



    def DisplayButtons(self):
        itemsSelected = self.list.selectedItems()

        if itemsSelected:
            self.rebootButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
            if len(itemsSelected) == 1:
                self.changeButton.setEnabled(True)
                self.infoButton.setEnabled(True)
            else:
                self.changeButton.setEnabled(False)
                self.infoButton.setEnabled(False)
        else:
            self.rebootButton.setEnabled(False)
            self.deleteButton.setEnabled(False)
            self.changeButton.setEnabled(False)
            self.infoButton.setEnabled(False)



    def ShowNodes(self):
        # Clear Node States
        for item in self.items_state.keys():
            self.items_state[item] = False

        # Get connected nodes
        self.items = r.keys(pattern = "Ping:Node:10.128.1{}*".format(room_names_ip[self.room_number.currentText()]))
        for item in self.items:
            info = r.get(item)
            if info is not None:
                self.items_info[item] = json.loads(info.decode().replace("'m"," am").replace("'","\""))
                self.items_state[item] = True

        for item in self.items_info.keys():
            item_ip = item.split(b'Node:')[1].decode()
            item_ip_name = item_ip + " - {}".format(self.items_info[item]['name'])

            if (self.find_value.text() == "" or self.find_value.text() in item_ip_name) and "10.128.1{}".format(room_names_ip[self.room_number.currentText()]) in item_ip:
                i = QtWidgets.QListWidgetItem(item_ip_name)
                if self.items_state[item] == False and self.disconnected_checkBox.isChecked():
                    i.setBackground(QtGui.QColor('red'))
                    if not self.list.findItems(item_ip_name, QtCore.Qt.MatchExactly):
                        self.list.addItem(i)

                elif self.items_state[item] == True and self.connected_checkBox.isChecked():
                    if not self.list.findItems(item_ip_name, QtCore.Qt.MatchExactly):
                        self.list.addItem(i)

        # Remove elements
        list_elements = []
        for row in range (self.list.count()):
            list_elements.append(("Ping:Node:"+self.list.item(row).text().split(" ")[0]).encode())

        for bbb in list_elements:
            item_ip = bbb.split(b'Node:')[1].decode()
            item_ip_name = item_ip + " - {}".format(self.items_info[bbb]['name'])
            qlistitem = self.list.findItems(bbb.split(b'Node:')[1].decode(), QtCore.Qt.MatchStartsWith)
            if len(qlistitem) > 1:
                qlistitem.reverse()
                for i in qlistitem:
                    self.list.takeItem(self.list.row(i))
            elif qlistitem:
                item_index = self.list.row(qlistitem[0])

            # Retira elemento se IP nao esta na faixa selecionada
            if (not "10.128.1{}".format(room_names_ip[self.room_number.currentText()]) in item_ip) or \
               (not bbb in self.items_info.keys()) or \
               (self.find_value.text() != "" and not self.find_value.text() in item_ip_name):
                self.list.takeItem(item_index)

            # Retira elemento de acordo com checkbox - coenctado/nao conectado
            if (self.items_state[bbb] == True and not self.connected_checkBox.isChecked()) or \
               (self.items_state[bbb] == False and not self.disconnected_checkBox.isChecked()):
                self.list.takeItem(item_index)

            else:
                if self.items_state[bbb] == False:
                    backcolor = 'red'
                else:
                    backcolor = 'white'

                try:
                    self.list.item(item_index).setBackground(QtGui.QColor(backcolor))
                except:
                    pass

        self.list.sortItems()

        self.ConnectedNumberLabel.setText("Total nodes: {}".format(len(self.items_info.keys())))
        self.ListedNumberLabel.setText("Listed: {}".format(self.list.count()))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonitoringBBB()
    window.show()
    sys.exit(app.exec_())

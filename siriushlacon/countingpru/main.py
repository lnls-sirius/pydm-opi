#****************Control's Group - MonitoringPRU*******************
#           Author: Robert Willian Polli
#           Last version: 04th April, 2020
#*****************************************************************
import sys, webbrowser, datetime, time, hashlib

from epics import caget, caput, PV
from functools import partial

from pydm import Display
from qtpy.QtGui import QPixmap
from qtpy import QtWidgets, QtCore

from siriushlacon.countingpru.Overview import Overview
from siriushlacon.countingpru.consts import BEFORE_BC_IMAGE, AFTER_BC_IMAGE, LNLS_IMAGE, CNPEM_IMAGE

qtMainFile = "ui/main.ui"

counters = ['C2','C3', 'M1']                                #Positions of conters on storage ring
Det_Location = ['M2','C1','C2','C3','C4']                   #Location of detectors

Password = 'c67ecf999969e683a24c4fbd9339ca5c'

measurement = ['DayAverage', 'WeekAverage', '2WeeksAverage', 'MonthAverage']

link_archiver = 'http://10.0.38.42/archiver-viewer/?{}from={}-{:0>2d}-{:0>2d}T{:0>2d}%3A{:0>2d}%3A01.010Z&to={}-{:0>2d}-{:0>2d}T{:0>2d}%3A{:0>2d}%3A01.010Z'

class MonitoringCountingPRU(Display):
    global qtMainFile, counters, Password

    def __init__(self, parent=None, macros=None, args=None):
        super().__init__(parent=parent, args=args, macros=macros, ui_filename=qtMainFile)

        self.finish_caget = False                                               #Program's variables
        self.isC2orC4 = False                                                   #

        self.gamma_measurement = {"M2":'M1', "C1":"M2", "C2":"C1", "C3":"C2", "C4":"C3", "M1":"C4", "":""}      #{position of sensor:measurement}
        self.Sector_number.valueChanged.connect(partial(self.set_box,'counter'))                                #If value of QComboBox change, call set_box
        self.Archiver_Button.clicked.connect(self.openArchiver)                                                 #Set function of button
        self.SN.returnPressed.connect(self.getPassword)                                                         #Called if serial number has been changed
        self.set_box('counter')                                                                                 #Function to add items to QComboBox

        self.beforeBC_image.setPixmap(QPixmap(BEFORE_BC_IMAGE))
        self.afterBC_image.setPixmap(QPixmap(AFTER_BC_IMAGE))
        self.cnpem_image.setPixmap(QPixmap(CNPEM_IMAGE))
        self.lnls_image.setPixmap(QPixmap(LNLS_IMAGE))

        self.counterBox.currentIndexChanged.connect(partial(self.new_counter, True))                            #True: chosen on QComboBox, False: Wrote by user
        self.gammaBox.currentIndexChanged.connect(partial(self.new_detector, True))                             # ""
        self.Counter_name.returnPressed.connect(self.new_counter)                                               #
        self.Gamma_name.returnPressed.connect(self.new_detector)                                                #Called when user search the names

        self.BT_Button.clicked.connect(self.Set_TimeBase)                                                       #
        self.OverviewButton.clicked.connect(self.overview)                                                      #Set functions to bottons
        self.pulsesAverageButton.clicked.connect(self.plot_average)                                             #
        self.OverviewAverage.clicked.connect(partial(self.plot_average, True))                                  #

    def plot_average(self, overview = False):
        self.checkBox_list = []
        self.Pulse_channel_Label.setText('Channel = ' + self.PV_name_label.text())
        self.LastDayAverage.channel   = 'ca://{}:DayAverage-Mon'.format(self.PV_name_label.text())              #
        self.LastWeekAverage.channel  = 'ca://{}:WeekAverage-Mon'.format(self.PV_name_label.text())             #Connects PVs of Averages
        self.TwoWeeksAverage.channel  = 'ca://{}:2WeeksAverage-Mon'.format(self.PV_name_label.text())           #
        self.LastMonthAverage.channel = 'ca://{}:MonthAverage-Mon'.format(self.PV_name_label.text())            #

        pvs = ''
        for checkBox in range(4):
            if eval('self.checkBox_{}'.format(checkBox)).isChecked():
                if overview: Overview(average = measurement[checkBox])                                                   #Opens Average Graphic
                else: pvs += 'pv={}%3A{}-Mon&'.format((self.Detector_name).replace(':','%3A'),measurement[checkBox])     #Creates the link to archiever
        if pvs != '': self.openArchiver(pvs)

    def overview(self):
        overwiew_Window = Overview()
        overwiew_Window.show()

    def openArchiver(self, pv_link= ''):
        a = time.gmtime()
        now = datetime.datetime(a.tm_year, a.tm_mon, a.tm_mday, a.tm_hour, a.tm_min, a.tm_sec)                 #Date and time of Greenwich
        new = now - datetime.timedelta(minutes = 10)

        if not(pv_link): pv = 'pv={}%3ACount-Mon&'.format((self.Detector_name).replace(':','%3A'))
        else: pv = pv_link

        link = (link_archiver.format(pv,new.year,int(new.month),int(new.day),\
        int(new.hour),int(new.minute),now.year,int(now.month),int(now.day),int(now.hour),int(now.minute)))
        webbrowser.open(link)                                                   #Opens the link

    def set_box(self, typ):                                                     #Same function to edit QComboBox of Counters and Gamma detectors
        if typ == 'counter':
            self.counterBox.clear()
            self.counterBox.addItems([''])
            for i in range(len(counters)):
                if counters[i] != 'M1':
                    self.counterBox.addItems(['SI-{:0>2d}{}:CO-Counter'.format(self.Sector_number.value(), counters[i])])
                elif self.Sector_number.value() != 20:
                    self.counterBox.addItems(['SI-{:0>2d}{}:CO-Counter'.format(self.Sector_number.value()+1, counters[i])])
                else: self.counterBox.addItems(['SI-01{}:CO-Counter'.format(counters[i])])

        elif typ == 'gamma':
            self.gammaBox.clear()
            if self.Counter_name.text() != '':
                for i in range(1,7):
                    add = caget(self.Counter_name.text()+':Ch{}-Cte'.format(str(i)))
                    if add != 'None': self.gammaBox.addItems([add])
                self.finish_caget = True
                self.new_detector(True)

    def new_counter(self, search = False):                                     #Show to user counter chosen
        self.finish_caget = False
        if search: self.Counter_name.setText(self.counterBox.currentText())
        if self.Counter_name.text() != '': self.set_box('gamma')

    def new_detector(self, search = False):                                     #Show to user gamma sensor chosen
        if search and self.finish_caget and (self.Counter_name.text() != ''):
            if self.Counter_name.text()[5:7] != 'M1':                               #
                self.Sector_number.setValue(int(self.Counter_name.text()[3:5]))     #
            elif self.Counter_name.text()[3:5] != '01':                             #Sets Sector Number Value
                self.Sector_number.setValue(int(self.Counter_name.text()[3:5])-1)   #
            else:                                                                   #
                self.Sector_number.setValue(int(20))                                #
            if self.isC2orC4:
                self.gammaBox.setCurrentIndex(1)
                self.isC2orC4 = False
            self.Gamma_name.setText(self.gammaBox.currentText())
            self.plot_info()

        elif self.finish_caget:                                                 #If user writes the gamma monitor name
            self.Counter_name.clear()
            self.plot_info()                                                    #Finds the name of counter
            if (self.Gamma_name.text()[5:7] == 'C2') or (self.Gamma_name.text()[5:7] == 'C4'):
                self.isC2orC4 = True
            self.set_box('gamma')


    def Set_TimeBase(self):
        if self.checkBox_TB.isChecked():                                #Set all time bases
            confirmation= QtWidgets.QMessageBox.question(self, 'Warning',"Do you want set all of Time Bases?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirmation == QtWidgets.QMessageBox.Yes:
                for sector in range(1,21):
                    for counter in counters:
                        caput("SI-{:0>2d}{}:CO-Counter:TimeBase-SP".format(sector, counter), self.BT_SpinBox.value())

        elif self.Counter_name.text() != '':
            confirmation= QtWidgets.QMessageBox.question(self, 'Warning',"Are you sure?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirmation == QtWidgets.QMessageBox.Yes:
                caput(self.Counter_name.text()+":TimeBase-SP", self.BT_SpinBox.value())
                self.plot_info()
        else: text = QtWidgets.QMessageBox.warning(self, 'Attention','Please, select a counter')

    def getPassword(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Attention", "Password?", QtWidgets.QLineEdit.Password)
        if (ok):
            if hashlib.md5(text.encode('utf-8')).hexdigest() == Password:
                caput(self.gamaselected + ':SerialNumber-Cte', int(self.SN.text()))
                changed = QtWidgets.QMessageBox.information(self, 'Changed','Gamma sensor Serial Number changed')
            else:
                error = QtWidgets.QMessageBox.warning(self, 'Attention','Password Incorrect')
        self.SN.setText(str(caget(self.gamaselected + ':SerialNumber-Cte')))

    def plot_info(self, value=''):
        if (self.Counter_name.text() == '' and self.Gamma_name.text() == ''):
            text = QtWidgets.QMessageBox.warning(self, 'Attention','Please, select a counter or detector')
            return()

        if self.Counter_name.text() == '':
            try:
                if self.Gamma_name.text()[-8:] == 'CO-Gamma':                       #Search by measurement, 'XXX:CO-Gamma'
                    self.Detector_name = self.Gamma_name.text()
                    Counter = caget(self.Gamma_name.text()+':Counter-Cte')
                    self.Sector_number.setValue(int(self.Gamma_name.text()[3:5]))

                    self.Counter_name.setText(Counter[:-4])
                    self.Gamma_name.setText(caget(self.Gamma_name.text()+':Sensor-Cte'))

                elif self.Gamma_name.text()[-13:] == 'GammaDetector':               #Search by detector name 'XXX:GammaDetector'
                    if self.Gamma_name.text()[5:7] == 'M1':
                        if self.Gamma_name.text()[3:5] != '01':
                            self.Detector_name = 'SI-{:0>2d}{}{}'.format(int(self.Gamma_name.text()[3:5])-1,\
                            self.gamma_measurement[self.Gamma_name.text()[5:7]],self.Gamma_name.text()[7:16])
                        else:
                            self.Detector_name = 'SI-20{}{}'.format(self.gamma_measurement[self.Gamma_name.text()[5:7]],self.Gamma_name.text()[7:16])
                    else:
                        self.Detector_name = self.Gamma_name.text()[:5]+self.gamma_measurement[self.Gamma_name.text()[5:7]]+self.Gamma_name.text()[7:16]
                    self.Sector_number.setValue(int(self.Detector_name[3:5]))
                    self.Counter_name.setText(caget(self.Detector_name+":Counter-Cte")[:-4])
                else: return()
            except:
                text = QtWidgets.QMessageBox.warning(self, 'Attention','Please, choose a valid gamma detector')
                return()
        else:
            self.Detector_name = 'SI-{:0>2d}{}:CO-Gamma'.format(self.Sector_number.value(),self.gamma_measurement[self.Gamma_name.text()[5:7]])

        self.SN.setEnabled(True)
        self.Archiver_Button.setEnabled(True)
        self.pulsesAverageButton.setEnabled(True)

        self.list_Channels.clear()
        self.PV_name_label.setText(self.Detector_name)
        self.Label_Counter.setText(self.Counter_name.text())

        self.LC.channel = 'ca://{}:Count-Mon'.format(self.Detector_name)               #
        self.TB.channel = 'ca://{}:TimeBase-SP'.format(self.Counter_name.text())       #Connect to PVs of Counting and Time Base

        for sensors in range(1,7):                                                     #Finds which channels are being used
            ins = QtWidgets.QListWidgetItem()
            pv = PV(self.Counter_name.text()+':Ch{}-Cte'.format(sensors))
            time.sleep(0.1)
            if not(pv.connected):
                text = QtWidgets.QMessageBox.warning(self, 'Warning','PV {} is not connected'.format(self.Counter_name.text()+':Ch{}-Cte'.format(sensors)))
            else:
                ins.setText(caget(self.Counter_name.text()+':Ch{}-Cte'.format(sensors)))
                if ins.text() == self.Gamma_name.text():
                    self.gamaselected = ins.text()
                    ins.setBackground(QtCore.Qt.cyan)

                elif self.Gamma_name.text()[-13:] != 'GammaDetector':
                    if self.Gamma_name.text() == '':
                        return()
                    if ins.text() == caget(self.Gamma_name.text()+':Sensor-Cte'):
                        self.gamaselected = ins.text()
                        ins.setBackground(QtCore.Qt.cyan)
                self.list_Channels.addItem(ins)
                self.image_setting()

        self.SN.setText(str(caget(self.gamaselected + ':SerialNumber-Cte')))             #Sets value of Serial Number

    def image_setting(self):                                                         #Changes the images to show which counter and detector are being used
        for gammaclear in ('C1', 'C2', 'C3', 'C4', 'M1'):
            eval('self.bit_Gamma{}'.format(gammaclear)).brush = QtCore.Qt.lightGray
        for counterclear in counters:
            eval('self.bit_Counter{}'.format(counterclear)).brush = QtCore.Qt.lightGray
        eval('self.bit_Gamma{}'.format(self.gamaselected[5:7])).brush = QtCore.Qt.green
        eval('self.bit_Counter{}'.format(self.Counter_name.text()[5:7])).brush = QtCore.Qt.red

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonitoringCountingPRU()
    window.show()
    sys.exit(app.exec_())

#****************Control's Group - MonitoringPRU*******************
#           Author: Robert Willian Polli
#           Last version: 05th February, 2020
#*****************************************************************
from epics import caget, caput
from pydm.widgets.channel import PyDMChannel
from pydm.widgets import PyDMEmbeddedDisplay
from PyQt5 import QtGui, QtWidgets, uic, QtCore
from functools import partial
from pydm import Display, PyDMApplication
import sys, json, webbrowser,datetime, threading, numpy, matplotlib, time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import CheckButtons
from qtpy.QtGui import QPixmap

from siriushlacon.countingpru.consts import OVERVIEW_UI, LAYOUT_OVERVIEW_UI, BEFORE_BC_IMAGE, AFTER_BC_IMAGE, LNLS_IMAGE, CNPEM_IMAGE

qtMainFile = "ui/main.ui"
qtOverViewFile = "ui/overview.ui"

counters = ['C2','C3', 'M1']                                #Positions of conters on storage ring
Det_Location = ['M2','C1','C2','C3','C4']                   #Location of detectors

class MonitoringCountingPRU(Display):
    global qtMainFile, counters

    def __init__(self, parent=None, macros=None, args=None):
        super().__init__(parent=parent, args=args, macros=macros, ui_filename=qtMainFile)

        self.gamma_measurement = {"M2":'M1', "C1":"M2", "C2":"C1", "C3":"C2", "C4":"C3", "M1":"C4", "":""}      #{position of sensor:measurement}

        self.Archiver_Button.clicked.connect(self.openArchiver)                                                 #Set function of button

        self.Sector_number.valueChanged.connect(partial(self.set_box,'counter'))                                #If value of QComboBox change, call set_box
        self.set_box('counter')                                                                                 #Function to add items to QComboBox

        self.beforeBC_image.setPixmap(QPixmap(BEFORE_BC_IMAGE))
        self.afterBC_image.setPixmap(QPixmap(AFTER_BC_IMAGE))
        self.cnpem_image.setPixmap(QPixmap(CNPEM_IMAGE))
        self.lnls_image.setPixmap(QPixmap(LNLS_IMAGE))

        self.counterBox.currentIndexChanged.connect(partial(self.new_counter, True))                            #True: chosen on QComboBox, False: Wrote by user
        self.gammaBox.currentIndexChanged.connect(partial(self.new_detector, True))                             # ""
        self.Counter_name.editingFinished.connect(self.new_counter)                                             #Set function for Counter and Gamma sensor
        self.Gamma_name.editingFinished.connect(self.new_detector)

        self.Plot_Button.clicked.connect(self.plot_info)                                                        #
        self.BT_Button.clicked.connect(self.Set_TimeBase)                                                       #Set functions to Plot, Base Time and Overview botton
        self.OverviewButton.clicked.connect(self.overview)                                                      #
        self.pulsesAverageButton.clicked.connect(self.plot_average)

    def plot_average(self):
        self.checkBox_list = []
        self.Pulse_channel_Label.setText('Channel = ' + self.PV_name_label.text())
        self.LastDayAverage.channel   = 'ca://{}:DayAverage-Mon'.format(self.PV_name_label.text())
        self.LastWeekAverage.channel  = 'ca://{}:WeekAverage-Mon'.format(self.PV_name_label.text())
        self.TwoWeeksAverage.channel  = 'ca://{}:2WeeksAverage-Mon'.format(self.PV_name_label.text())
        self.LastMonthAverage.channel = 'ca://{}:MonthAverage-Mon'.format(self.PV_name_label.text())

        pvs = ''
        measurement = ['DayAverage-Mon', 'WeekAverage-Mon', '2WeeksAverage-Mon', 'MonthAverage-Mon']
        for checkBox in range(4):
            if eval('self.checkBox_{}'.format(checkBox)).isChecked():
                pvs += 'pv={}%3A{}&'.format((self.Detector_name).replace(':','%3A'),measurement[checkBox])
        if pvs != '': self.openArchiver(pvs)

    def overview(self):
        overwiew_Window = Overview()
        overwiew_Window.show()

    def openArchiver(self, pv_link= ''):
        now = datetime.datetime.now() + datetime.timedelta(hours = 3)
        new = now - datetime.timedelta(minutes = 10)

        if not(pv_link): pv = 'pv={}%3ACount-Mon&'.format((self.Detector_name).replace(':','%3A'))
        else: pv = pv_link

        link = ('http://10.0.38.42/archiver-viewer/?{}from={}-{:0>2d}-{:0>2d}T\
{:0>2d}%3A{:0>2d}%3A01.010Z&to={}-{:0>2d}-{:0>2d}T{:0>2d}%3A{:0>2d}%3A01.010Z'.format(pv,new.year,int(new.month),int(new.day),\
        int(new.hour),int(new.minute),now.year,int(now.month),int(now.day),int(now.hour),int(now.minute)))
        webbrowser.open(link)

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
            if self.counterBox.currentText() != '':
                for i in range(1,7):
                    add = caget(self.counterBox.currentText()+':Ch{}-Cte'.format(str(i)))
                    if add != 'None': self.gammaBox.addItems([add])

    def new_counter(self, printar = False):                                     #Show to user counter chosen
        if printar: self.Counter_name.setText(self.counterBox.currentText())
        if self.Counter_name.text() != '': self.set_box('gamma')

    def new_detector(self, printar = False):                                    #Show to user gamma sensor chosen
        if printar: self.Gamma_name.setText(self.gammaBox.currentText())
        else: self.Counter_name.clear()

    def Set_TimeBase(self):
        if self.Counter_name.text() != '':
            confirmation= QtWidgets.QMessageBox.question(self, 'Warning',"Are you sure?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirmation == QtWidgets.QMessageBox.Yes:
                if self.checkBox_TB.isChecked():                                #Set all time bases
                    for sector in range(1,21):
                        for counter in counters:
                            caput("SI-{:0>2d}{}:CO-Counter:TimeBase-SP".format(sector, counter), self.BT_SpinBox.value())
                else: caput(self.Counter_name.text()+":TimeBase-SP", self.BT_SpinBox.value())
                self.plot_info()

    def plot_info(self, value=''):

        if (self.Counter_name.text() == '' and self.Gamma_name.text() == ''): return()
        self.pulsesAverageButton.setEnabled(True)

        if self.Counter_name.text() == '':
            if self.Gamma_name.text()[-8:] == 'CO-Gamma':                       #Search by measurement, 'XXX:CO-Gamma'
                Counter = caget(self.Gamma_name.text()+':Counter-Cte')
                self.Detector_name = self.Gamma_name.text()
                self.Sector_number.setValue(int(self.Gamma_name.text()[3:5]))
                self.Counter_name.setText(Counter[:-4])

            elif self.Gamma_name.text()[-13:] == 'GammaDetector':               #Search by detector name 'XXX:GammaDetector'
                if self.Gamma_name.text()[5:7] == 'M1':
                    self.Detector_name = 'SI-{:0>2d}{}{}'.format(int(self.Gamma_name.text()[3:5])-1,\
                    self.gamma_measurement[self.Gamma_name.text()[5:7]],self.Gamma_name.text()[7:16])
                    print(self.Detector_name)
                else:
                    self.Detector_name = self.Gamma_name.text()[:5]+self.gamma_measurement[self.Gamma_name.text()[5:7]]+self.Gamma_name.text()[7:16]
                self.Sector_number.setValue(int(self.Detector_name[3:5]))
                self.Counter_name.setText(caget(self.Detector_name+":Counter-Cte")[:-4])

            else: return()
        else:
            self.Detector_name = 'SI-{:0>2d}{}:CO-Gamma'.format(self.Sector_number.value(),self.gamma_measurement[self.Gamma_name.text()[5:7]])

        self.Archiver_Button.setEnabled(True)
        self.list_Channels.clear()
        self.PV_name_label.setText(self.Detector_name)
        self.Label_Counter.setText(str(self.Counter_name.text()))

        self.TB.channel = 'ca://{}:TimeBase-SP'.format(self.Counter_name.text())       #Connect to PVs of Counting and Time Base
        self.LC.channel = 'ca://{}:Count-Mon'.format(self.Detector_name)

        for sensors in range(1,7):
            ins = QtWidgets.QListWidgetItem()
            ins.setText(caget(self.Counter_name.text()+':Ch{}-Cte'.format(sensors)))
            if ins.text() == self.Gamma_name.text():
                self.gamaselected = ins.text()
                ins.setBackground(QtCore.Qt.cyan)

            elif self.Gamma_name.text()[-13:] != 'GammaDetector':
                if ins.text() == caget(self.Gamma_name.text()+':Sensor-Cte'):
                    self.gamaselected = ins.text()
                    ins.setBackground(QtCore.Qt.cyan)
            self.list_Channels.addItem(ins)
        self.image_setting()

    def image_setting(self):
        for gammaclear in ('C1', 'C2', 'C3', 'C4', 'M1'):
            eval('self.bit_Gamma{}'.format(gammaclear)).brush = QtCore.Qt.lightGray
        for counterclear in counters:
            eval('self.bit_Counter{}'.format(counterclear)).brush = QtCore.Qt.lightGray
        eval('self.bit_Gamma{}'.format(self.gamaselected[5:7])).brush = QtCore.Qt.green
        eval('self.bit_Counter{}'.format(self.Counter_name.text()[5:7])).brush = QtCore.Qt.red


class Overview(Display):
    global counters, Det_Location,qtOverViewFile

    def __init__(self, parent=None, macros=None, args=None):
        super().__init__(parent=parent, args=args, macros=macros, ui_filename=OVERVIEW_UI)
        self.alpha = [0,0,0,0,0]
        self.groups = ['{:0>2d}'.format(sec) for sec in range(1,21)]
        self.x = numpy.arange(len(self.groups))
        self.width = 0.185

        self.dict_pvs_tb = {}
        self.dict_macro_gamma = {}

        self.gamma_1 = [0]*20
        self.gamma_2 = [0]*20
        self.gamma_3 = [0]*20
        self.gamma_4 = [0]*20
        self.gamma_5 = [0]*20

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95)
        plt.subplots_adjust(left=0.1)
        self.fig.text(0.03,0.25,'Control of\n Graphic', ha = 'center')
        self.ani = FuncAnimation(fig = self.fig, func = self.animate, interval = 10000)
        self.t1 = threading.Thread(target = self.k, args = [], daemon = True)
        plt.show()

        for PV in range(1,21):
            for s_sec in range(3):
                self.dict_pvs_tb['valueTB{}{}'.format(PV,counters[s_sec])] = 'ca://SI-{:0>2d}{}:CO-Counter:TimeBase-SP'.format(PV,counters[s_sec])

        for location in range(1,21):
            for s_sec in range(len(Det_Location)):
                self.dict_macro_gamma['DET{}'.format(s_sec)] = "SI-{:0>2d}{}:CO-Gamma".format(location, Det_Location[s_sec])
                if s_sec < 3: self.dict_macro_gamma['TimeBase{}'.format(s_sec)] = '{}'.format(self.dict_pvs_tb['valueTB{}{}'.format(location,counters[s_sec])])

                a = PyDMChannel(address = 'ca://SI-{:0>2d}{}:CO-Gamma:Count-Mon'.format(location,\
                Det_Location[s_sec]),value_slot=partial(self.plot, location = location, det = s_sec))
                a.connect()

            self.disp = PyDMEmbeddedDisplay(parent=self)
            PyDMApplication.instance().close_widget_connections(self.disp)
            self.disp.macros = json.dumps(self.dict_macro_gamma)
            self.disp.filename = LAYOUT_OVERVIEW_UI
            self.disp.setMinimumWidth(300)
            self.disp.setMinimumHeight(140)
            self.verticalLayout.addWidget(self.disp)

            PyDMApplication.instance().establish_widget_connections(self.disp)

    def k(self):
        visibility = [line.patches[0].get_alpha() == 1 for line in self.graph]

        self.rax = plt.axes(position = [0.005, 0.08, 0.05, 0.15])
        self.labels = ['     '+str(line.get_label()) for line in self.graph]
        self.check = CheckButtons(self.rax, self.labels, visibility)
        self.check.on_clicked(self.hide_show)
        while(True):
            time.sleep(1)

    def hide_show(self,label):
        index = self.labels.index(label)
        if self.graph[index].patches[index].get_alpha() == 1:
            for i in range(20):
                self.graph[index].patches[i].set_alpha(0)
            self.alpha[index] = self.graph[index].patches[index].get_alpha()

        else:
            for i in range(20):
                self.graph[index].patches[i].set_alpha(1)
                self.alpha[index] = self.graph[index].patches[i].get_alpha()
        plt.draw()
        self.animate(i)

    def animate(self,i):
        self.ax.clear()
        self.rects1 = self.ax.bar(self.x - self.width*2, self.gamma_1, self.width, label='M2', alpha = self.alpha[0])
        self.rects2 = self.ax.bar(self.x - self.width  , self.gamma_2, self.width, label='C1', alpha = self.alpha[1])
        self.rects3 = self.ax.bar(self.x               , self.gamma_3, self.width, label='C2', alpha = self.alpha[2])
        self.rects4 = self.ax.bar(self.x + self.width  , self.gamma_4, self.width, label='C3', alpha = self.alpha[3])
        self.rects5 = self.ax.bar(self.x + self.width*2, self.gamma_5, self.width, label='C4', alpha = self.alpha[4])

        self.ax.set_ylabel('Counting - Pulses per second')
        self.ax.set_xlabel('Sectors of Storage Ring')
        self.ax.set_title('Overview of Counters')
        self.ax.set_xticklabels(self.groups)
        self.ax.set_xticks(self.x)
        self.ax.set_yscale('log')
        self.ax.legend()

        self.autolabel(self.rects1, self.alpha[0] == 1)
        self.autolabel(self.rects2, self.alpha[1] == 1)
        self.autolabel(self.rects3, self.alpha[2] == 1)
        self.autolabel(self.rects4, self.alpha[3] == 1)
        self.autolabel(self.rects5, self.alpha[4] == 1)

        self.graph = [self.rects1, self.rects2, self.rects3, self.rects4, self.rects5]

    def autolabel(self,rects, vis):
        for rect in rects:
            height = rect.get_height()
            self.ax.annotate('{}'.format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom', fontsize = 8, rotation = 90, visible = vis)

    def plot(self, value='', location='', det=''):
        eval('self.gamma_{}'.format(det+1)).insert(location-1,round(value,5))
        del(eval('self.gamma_{}'.format(det+1))[location])

        if not(self.t1.is_alive()):
            self.t1.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonitoringCountingPRU()
    window.show()
    sys.exit(app.exec_())

import numpy, json
from pydm import Display, PyDMApplication
import matplotlib.pyplot as plt
from functools import partial

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import CheckButtons

from pydm.widgets.channel import PyDMChannel
from pydm.widgets import PyDMEmbeddedDisplay

from siriushlacon.countingpru.consts import OVERVIEW_UI, LAYOUT_OVERVIEW_UI

counters = ['C2','C3', 'M1']                                #Positions of conters on storage ring
Det_Location = ['M2','C1','C2','C3','C4']                   #Location of detectors

class Overview(Display):
    global counters, Det_Location

    def __init__(self, parent=None, macros=None, args=None, average = 'Gamma Detectors'):
        super().__init__(parent=parent, args=args, macros=macros, ui_filename=OVERVIEW_UI)
        self.setWindowTitle('Overview of Time Bases')
        self.alpha = [0,0,0,0,0]                                                    #Initially doesn't show none graph
        self.average = average
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

        self.fig, self.ax = plt.subplots(figsize=(12, 8))                       #
        self.fig.canvas.set_window_title('Overview')                            #
        self.fig.subplots_adjust(left=0.05, bottom=0.08, right=0.95, top=0.95)  #Adjustments of graphics
        plt.subplots_adjust(left=0.1)                                           #

        self.fig.text(0.03,0.25,'Control of\n Graphic', ha = 'center')
        self.ani = FuncAnimation(fig = self.fig, func = self.animate, interval = 10000)
        self.animate()
        self.checkButtons_setting()
        plt.show()

        if self.average == 'Gamma Detectors':                                   #If user chose 'Counting - Overview'
            for PV in range(1,21):
                for s_sec in range(2):
                    self.dict_pvs_tb['valueTB{}{}'.format(PV,counters[s_sec])] = 'ca://SI-{:0>2d}{}:CO-Counter:TimeBase-SP'.format(PV,counters[s_sec])
                if PV != 20:
                    self.dict_pvs_tb['valueTB{}M1'.format(PV)] = 'ca://SI-{:0>2d}M1:CO-Counter:TimeBase-SP'.format(PV+1)
                else:
                    self.dict_pvs_tb['valueTB{}M1'.format(PV)] = 'ca://SI-01M1:CO-Counter:TimeBase-SP'

            for location in range(1,21):
                for s_sec in range(len(Det_Location)):
                    self.dict_macro_gamma['DET{}'.format(s_sec)] = "SI-{:0>2d}{}:CO-Gamma".format(location, Det_Location[s_sec])
                    if s_sec < 3: self.dict_macro_gamma['TimeBase{}'.format(s_sec)] = '{}'.format(self.dict_pvs_tb['valueTB{}{}'.format(location,counters[s_sec])])

                    a = PyDMChannel(address = 'ca://SI-{:0>2d}{}:CO-Gamma:Count-Mon'.format(location,\
                    Det_Location[s_sec]),value_slot=partial(self.plot, location = location, det = s_sec)) #Connect to Counting PVs
                    a.connect()

                self.disp = PyDMEmbeddedDisplay(parent=self)                    #Creates the window of Time Bases
                PyDMApplication.instance().close_widget_connections(self.disp)
                self.disp.macros = json.dumps(self.dict_macro_gamma)
                self.disp.filename = LAYOUT_OVERVIEW_UI
                self.disp.setMinimumWidth(300)
                self.disp.setMinimumHeight(140)
                self.verticalLayout.addWidget(self.disp)

                PyDMApplication.instance().establish_widget_connections(self.disp)
        else:                                                                   #If user chose some Average
            for location in range(1,21):
                for s_sec in range(len(Det_Location)):
                    a = PyDMChannel(address = 'ca://SI-{:0>2d}{}:CO-Gamma:{}-Mon'.format(location,\
                    Det_Location[s_sec], self.average),value_slot=partial(self.plot, location = location, det = s_sec)) #Connect to Averages PVs
                    a.connect()

    def checkButtons_setting(self):                                             #Configures of check button
        visibility = [line.patches[0].get_alpha() == 1 for line in self.graph]
        self.rax = plt.axes(position = [0.005, 0.08, 0.05, 0.15])
        self.labels = ['     '+str(line.get_label()) for line in self.graph]
        self.check = CheckButtons(self.rax, self.labels, visibility)
        self.check.on_clicked(self.hide_show)

    def hide_show(self,label):                                                  #Set graph Visibilities
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

    def animate(self, *args):                                                   #Function to update the graph
        self.ax.clear()
        self.rects1 = self.ax.bar(self.x - self.width*2, self.gamma_1, self.width, label='M2', alpha = self.alpha[0])
        self.rects2 = self.ax.bar(self.x - self.width  , self.gamma_2, self.width, label='C1', alpha = self.alpha[1])
        self.rects3 = self.ax.bar(self.x               , self.gamma_3, self.width, label='C2', alpha = self.alpha[2])
        self.rects4 = self.ax.bar(self.x + self.width  , self.gamma_4, self.width, label='C3', alpha = self.alpha[3])
        self.rects5 = self.ax.bar(self.x + self.width*2, self.gamma_5, self.width, label='C4', alpha = self.alpha[4])

        self.ax.set_title('Overview of {}'.format(self.average))
        self.ax.set_xlabel('Sectors of Storage Ring')
        self.ax.set_ylabel('Pulses per second')
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

    def autolabel(self,rects, vis):                                             #Sets the visualization of counting above of bars
        for rect in rects:
            height = rect.get_height()
            self.ax.annotate('{}'.format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom', fontsize = 8, rotation = 90, visible = vis)

    def plot(self, value='', location='', det=''):                              #Updates the list of last counts
        eval('self.gamma_{}'.format(det+1)).insert(location-1,round(value,5))
        del(eval('self.gamma_{}'.format(det+1))[location])

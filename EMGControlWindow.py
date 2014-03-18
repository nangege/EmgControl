import sys
from time import sleep
import timer
import threading
import pylab as pl

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QTAgg as NavigationToolbar)
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE

if use_pyside:
    from PySide.QtCore import *
    from PySide.QtGui import *
else:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

from PyQt4 import QtCore

from ui_qt import Ui_MainWindow
from devDaq import Daq

class DaqThread(QObject,threading.Thread):
    daqCompleted = QtCore.pyqtSignal(int)
    def __init__(self,devName = "Dev1/ai0:3",sampleNum = 800,sampleRate = 800.0,channelNum = 4,parent = None):
        super(QObject,self).__init__(parent)
        threading.Thread.__init__(self)
        self.devName = devName
        self.sampleNum = sampleNum
        self.sampleRate = sampleRate
        self.channelNum = channelNum;
        self.daq = Daq()
        self.data = []
        self.num = 0
        self.runFlag = 1
        
    def startDev(self):
        self.daq.initDev(self.devName,self.sampleNum,self.sampleRate,num = self.channelNum)
        self.daq.devStart()
    
    def startDaq(self):
        self.runFlag = 1
    
    def stopDaq(self):
        self.runFlag = 0
    
    def stopDev(self):
        self.daq.devStop()
        self.stopDaq()
    
    def getNum(self):
        return self.num
    
    def getData(self):
        return self.data
        
    def run(self):
        while(True):
            if(self.runFlag):
                (self.data,self.num) = self.daq.acquireData()
                self.daqCompleted.emit(self.num)
            else:
                sleep(0.5)
     
    @QtCore.pyqtSlot(int)        
    def printData(self,num):
        print self.getData()
            
class EMGMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(EMGMainWindow,self).__init__(parent = None)
        self.setupUi(self)
        
        self.fig = Figure((8.0, 8.0), dpi= 80,tight_layout = True)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.frame)
        self.canvas.setFocusPolicy(Qt.StrongFocus)   
        self.fig.clear()
        self.fig.set_facecolor('mediumseagreen')
        self.axes = self.fig.add_subplot(111)  
        #self.axes.axis('off')
 
        self.canvas.draw()
   
        self.daq = DaqThread()
        self.daq.setDaemon(True)
        self.daq.startDev()
        
        self.numPerChannel = self.daq.sampleNum/self.daq.channelNum
        
        self.numToShow = 1600
        
        self.data = [[] for i in range(self.daq.channelNum)]        
        self.allData = [[] for i in range(self.daq.channelNum)]  
        
        QObject.connect(self.pushButton,SIGNAL("clicked()"),self.start)
        QObject.connect(self.pushButton_2,SIGNAL("clicked()"),self.daq.stopDaq)
        QObject.connect(self.daq,SIGNAL("daqCompleted(int)"),self.acquireData)
        QObject.connect(self.fullDataButton,SIGNAL("clicked()"),self.showFullData)
        
    def start(self):
        self.daq.start()
        QObject.disconnect(self.pushButton,SIGNAL("clicked()"),self.start)
        QObject.connect(self.pushButton,SIGNAL("clicked()"),self.daq.startDaq)
        
    def acquireData(self,num):
        data = self.daq.getData()
        
        for i in range(len(self.data)):
            if len(self.data[i]) >= self.numToShow:
                self.data[i] = self.data[i][self.numPerChannel:self.numToShow]
            self.data[i].extend(data[i*self.numPerChannel:(1 + i)*self.numPerChannel])
            self.allData[i].extend(data[i*self.numPerChannel:(1 + i)*self.numPerChannel])
            
        if len(self.data[0]) >= self.numToShow:
            self.upDataFig()
            
    def showFullData(self):
        print "Show Full Data"
        for i in range(len(self.allData)):
            pl.plot(range(len(self.allData[i])),self.allData[i])
        pl.show()
            
    def upDataFig(self):
        
        num = len(self.data)
        #num = 1
        self.axes.cla()
        
        self.axes.set_ylim(0,num)
        self.axes.set_xlim(0,self.numToShow/4)
        
        for i in range(num):
            self.axes.plot(range(len(self.data[i])/4),[i + data/3.5 for data in self.data[i][0:len(self.data[i]):4]],color = 'red')
        
        #for i in range(num - 1):
            #self.axes.plot([1,self.numToShow],[ i + 1  for t in range(2)],color = 'black',linewidth = 2)
        
        #for i,axes in enumerate(self.axesTuple):
            #axes.cla()
            #axes.set_ylim(0,3.5)
            #axes.set_xlim(0,self.numToShow/4)
            #axes.plot(range(len(self.data[i])/4),[data for data in self.data[i][0:len(self.data[i]):4]],color = 'red')

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EMGMainWindow()
    window.show()
    app.exec_()
    
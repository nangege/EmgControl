import ctypes
import numpy as np
import threading
from time import sleep

class Daq():
    def __init__(self):
        self.daq = ctypes.cdll.LoadLibrary('libNIDaq.dll')
        self.daq.getData.restype = ctypes.c_double
        self.daq.getNext.restype = ctypes.c_double 
        self.daq.acquireData.restype = ctypes.c_int
        self.devName = 0
        self.sampleNum = 500
        self.data = []
    
    def initDev(self,devName = "Dev1/ai0",sampleNum = 500,sampleRate = 1000.0,num = 1):
        self.devName = devName
        self.sampleNum = sampleNum
        self.daq.init(self.devName,self.sampleNum,ctypes.c_double(sampleRate),ctypes.c_int(num))
        
    def devStart(self):
        self.daq.start()
    
    def acquireData(self):
        num = self.daq.acquireData()
        return map(self.daq.getData,range(self.sampleNum)),num
    
    def devStop(self):
        self.daq.stop()
    
    def finish(self):
        self.daq.finish()
            
if __name__ == "__main__":
    daq = Daq()
    daq.initDev()
    daq.devStart()
    (data,num) = daq.acquireData()
    print data
    daq.finish()
        
        
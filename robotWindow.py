import sys
import vtk

try:
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtCore import *
except ImportError:
    try:
        from PySide import QtCore, QtGui
        from PySide.QtCore import *
    except ImportError:
        raise ImportError("Cannot load either PyQt or PySide")

from QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from  ui_robot import Ui_robotWidget
from robotHandModel import robotModel,palmModel

class robotWindow(QtGui.QWidget,Ui_robotWidget):
    setAllAngle = QtCore.pyqtSignal(int)
    def __init__(self,parent = None):
        super(robotWindow,self).__init__(parent = None)
        self.setupUi(self)
        
        self.robot = palmModel()
               
        self.vtkWidget = QVTKRenderWindowInteractor(self.robotWidget)
        self.ren = vtk.vtkRenderer()
        
        lightPosition = [0,0,1]
        lightFocalPoint = [0,0,0]
        light = vtk.vtkLight()
        light.SetLightTypeToSceneLight()
        light.SetPosition(lightPosition[0], lightPosition[1], lightPosition[2])
        light.SetPositional(True) 
        light.SetConeAngle(10)
        light.SetFocalPoint(lightFocalPoint[0], lightFocalPoint[1], lightFocalPoint[2])
        light.SetDiffuseColor(1,0,0)
        light.SetAmbientColor(0,1,0)
        light.SetSpecularColor(0,0,1)
       

        lightActor = vtk.vtkLightActor()
        lightActor.SetLight(light)
        self.ren.AddViewProp(lightActor)
    
        self.ren.SetBackground(0, 0.6, 0.9)
        self.renderWindow = self.vtkWidget.GetRenderWindow()
        self.renderWindow.AddRenderer(self.ren)
        self.style = vtk.vtkInteractorStyleTrackballCamera()  
        self.vtkWidget.SetInteractorStyle(self.style)
        
        self.checkBox = [self.thumbChectBox,self.foreCheckBox,self.middleCheckBox,
                         self.ringCheckBox,self.littleCheckBox]

        if not self.thumbChectBox.isChecked():
            self.robot = robotModel()
            self.setArmConnect()
        
        self.finger = [self.robot.thumb.finger,self.robot.fingerOne,self.robot.fingerTwo,
                       self.robot.fingerThree,self.robot.fingerFour] 
        
        self.fingerSender = [self.thumbYSlide,self.thumbSlide,self.foreSlide,
                       self.middleSlide,self.ringSlide,self.littleSlide]
        self.setPalmConnect()     
        
        map(self.connectFun,self.checkBox,
            [self.changeCheckBoxConnect for i in range(len(self.checkBox))],
            [SIGNAL("clicked()") for i in range(len(self.checkBox))]) 
        
        self.fingerTogether = []
        self.slideTogether = []
        
        self.connect(self.palmModelCheckBox,SIGNAL("stateChanged(int)"),self.changeRobotModel)
        
        self.ren.AddActor(self.robot.getAssembly())
        self.axes = vtk.vtkAxesActor()
        self.axes.SetTotalLength(100,100,100)
        center = self.ren.GetCenter()
        self.axes.SetPosition(0,0,0)
        #self.ren.AddActor(self.axes)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        
    def changeRobotModel(self,isChecked):
        self.ren.RemoveActor(self.robot.getAssembly())
        if isChecked:
            self.robot = palmModel()
            self.robot.setPosition(-20,-450,0)
        else:
            self.robot = robotModel()
            self.setArmConnect()
        self.ren.AddActor(self.robot.getAssembly())
  
        self.finger = [self.robot.thumb.finger,self.robot.fingerOne,self.robot.fingerTwo,
                       self.robot.fingerThree,self.robot.fingerFour] 
         
        self.setPalmConnect() 
        self.renderWindow.Render()
            
    def changeCheckBoxConnect(self):
        for slide in self.slideTogether:
            self.disconnect(slide,SIGNAL("valueChanged(int)"),self.setTogether)
        flag = map((lambda checkBox:checkBox.isChecked()),self.checkBox)
        sender = [self.thumbSlide,self.foreSlide,self.middleSlide,self.ringSlide,self.littleSlide]
        self.fingerTogether = []
        self.slideTogether  = []
        for f,s,fin in zip(flag,sender,self.finger):
            if f:
                self.connectFun(s,self.setTogether)
                self.slideTogether.append(s)
                if s not in self.fingerTogether:
                    self.fingerTogether.append(fin)
    
    def setTogether(self,angle):
        for finger in self.fingerTogether:
            finger.rotateAll(angle)
        self.renderWindow.Render()
            
    def connectFun(self,sender,slot,signal = SIGNAL("valueChanged(int)")):
        self.connect(sender,signal,slot)
        
    def setArmConnect(self):
        sender = [self.shoulderXSlide,self.shoulderZSlide,self.armYSlide,self.armXSlide,
                  self.foreArmXSlide,self.palmXSlide,self.palmZSlide]
        slot = [self.robot.rotateShoulderX,self.robot.rotateShoulderZ,self.robot.rotateArmY,
                self.robot.rotateArmX,self.robot.rotateLittleArmX,self.robot.rotateHandX,self.robot.rotateHandZ]
        map(self.connectFun,sender,slot)
        map(self.connectFun,sender,[self.renderWindow.Render for i in range(7)])
        
    def setPalmConnect(self):
        slot = [finger.rotateAll for finger in self.finger]
        slot.insert(0,self.robot.rotateThumb)
        
        map(self.connectFun,self.fingerSender,slot)
        map(self.connectFun,self.fingerSender,[self.renderWindow.Render for i in range(6)])        
                   
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = robotWindow()
    window.show()
    app.exec_()    


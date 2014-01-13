import sys
import vtk
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
#from QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from  ui_robot import Ui_robotWidget
from robotHandModel import robotModel,palmModel

class robotWindow(QtGui.QWidget,Ui_robotWidget):
    def __init__(self,parent = None):
        super(robotWindow,self).__init__(parent = None)
        self.setupUi(self)
        
        #self.robot = robotModel()
               
        #self.vtkWidget = QVTKRenderWindowInteractor(self.robotWidget)
        #self.ren = vtk.vtkRenderer()
        
        ##self.ren.SetBackground(0.2, 0.4, 0.6)
        ##self.ren.SetBackground(0, 0.6, 0.7)
        #self.ren.SetBackground(0, 0.6, 0.9)
        #self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        #self.style = vtk.vtkInteractorStyleTrackballCamera()  
        #self.vtkWidget.SetInteractorStyle(self.style)
        
        #self.ren.AddActor(self.robot.getAssembly())
        #self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        #self.iren.Initialize()
        
        #self.setConnect()
        
    #def setConnect(self):
        #QObject.connect(self.shoulderXSlide,SIGNAL("valueChanged(int)"),self.robot.rotateShoulderX)
        #QObject.connect(self.shoulderZSlide,SIGNAL("valueChanged(int)"),self.robot.rotateShoulderZ)
        #QObject.connect(self.armYSlide,SIGNAL("valueChanged(int)"),self.robot.rotateArmY)
        #QObject.connect(self.armXSlide,SIGNAL("valueChanged(int)"),self.robot.rotateArmX)
        #QObject.connect(self.palmXSlide,SIGNAL("valueChanged(int)"),self.robot.rotateHandX)
        #QObject.connect(self.palmZSlide,SIGNAL("valueChanged(int)"),self.robot.rotateHandZ)
        
        #QObject.connect(self.foreSlide,SIGNAL("valueChanged(int)"),self.robot.palm.fingerOne.rotateAll)
        #QObject.connect(self.middleSlide,SIGNAL("valueChanged(int)"),self.robot.palm.fingerTwo.rotateAll)
        #QObject.connect(self.ringSlide,SIGNAL("valueChanged(int)"),self.robot.palm.fingerThree.rotateAll)
        #QObject.connect(self.littleSlide,SIGNAL("valueChanged(int)"),self.robot.palm.fingerFour.rotateAll)  

        #QObject.connect(self.shoulderXSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        #QObject.connect(self.shoulderZSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        #QObject.connect(self.armYSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        #QObject.connect(self.armXSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        #QObject.connect(self.palmXSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        #QObject.connect(self.palmZSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        
        #QObject.connect(self.foreSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        #QObject.connect(self.middleSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        #QObject.connect(self.ringSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render)
        #QObject.connect(self.littleSlide,SIGNAL("valueChanged(int)"),self.vtkWidget.GetRenderWindow().Render) 
        
        #QObject.connect(self.foreSlide,SIGNAL("valueChanged(int)"),self.robot.fingerOne.rotateAll)
        #QObject.connect(self.middleSlide,SIGNAL("valueChanged(int)"),self.robot.fingerTwo.rotateAll)
        #QObject.connect(self.ringSlide,SIGNAL("valueChanged(int)"),self.robot.fingerThree.rotateAll)
        #QObject.connect(self.littleSlide,SIGNAL("valueChanged(int)"),self.robot.fingerFour.rotateAll)            
        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = robotWindow()
    window.show()
    app.exec_()    


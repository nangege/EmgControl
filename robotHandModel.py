import vtk

class assemblyModel():
    def __init__(self,axesOn = True):
        self.assembly = vtk.vtkAssembly()
        self.axes = vtk.vtkAxesActor() 
        self.assembly.AddPart(self.axes)
        self.length = 20
        self.setAxesOn(axesOn)
    
    def setOrigin(self,x,y,z):
        self.assembly.SetOrigin(x,y,z)
        self.axes.SetPosition(self.assembly.GetOrigin()) 
    
    def setAxesOn(self,axesOn = True):
        if axesOn:
            self.axes.SetTotalLength(self.length,self.length,self.length)
        else:
            self.axes.SetTotalLength(0,0,0)
            
    def setAxesLength(self,length):
        self.length = length
        self.setAxesOn()
            
    def translate(self,x = 0,y = 0,z = 0):
        self.assembly.AddPosition(x,y,z)
        
    def setPosition(self,x = 0,y = 0,z = 0):
        self.assembly.SetPosition(x,y,z)
        
    def RotateX(self,angle):
        self.assembly.RotateX(angle)
        
    def RotateY(self,angle):
        self.assembly.RotateY(angle)

    def RotateZ(self,angle):
        self.assembly.RotateZ(angle)
        
    def getAssembly(self):
        return self.assembly
    
    def AddModel(self,model):
        self.assembly.AddPart(model)
       
class partModel(assemblyModel):
    def __init__(self,fileName ,axesOn = True,parent = None):
        assemblyModel.__init__(self,axesOn)
        self.actor = self.getPartActor(fileName)
        self.AddModel(self.actor)
        
    def getPartActor(self,fileName):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(fileName)
     
        polyDataOutput = reader.GetOutput()
     
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
     
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        return actor    
    
    def setTexture(self,fileName = None,fileReader = vtk.vtkPNGReader()):
        reader = fileReader
        reader.SetFileName(fileName) 
        texture = vtk.vtkTexture()
        texture.SetInput(reader.GetOutput())
        self.actor.SetTexture(texture)
        
    def setColor(self,r = 1,g = 1,b = 1):
        self.actor.GetProperty().SetColor(r,g,b)

class fingerModel(assemblyModel):
    def __init__(self,axesOn = False):
        assemblyModel.__init__(self,axesOn)
        self.foreFinger = partModel("robot/foreFinger.stl")
        
        
        self.middleFinger = partModel("robot/middleFinger.stl")
        self.middleFinger.AddModel(self.foreFinger.getAssembly())
        
        self.afterFinger = partModel("robot/afterFinger.stl")
        self.afterFinger.AddModel(self.middleFinger.getAssembly())
        
        self.AddModel(self.afterFinger.getAssembly())
        
        self.setOrigin(15,113,15)
        self.afterFinger.setOrigin(15,113,15)
        self.afterFinger.actor.RotateZ(-5)
        self.middleFinger.setOrigin(15,145,15)
        self.middleFinger.actor.RotateZ(-5)
        self.foreFinger.setOrigin(15,172,22)
        self.foreFinger.actor.RotateZ(-5)
        
        #self.afterFinger.setColor(1.0,0,0)
        #self.middleFinger.setColor(0,1.0,0)
        #self.foreFinger.setColor(0,0,1.0)
        
        self.angleAfter = 0
        self.angleMiddle = 0
        self.angleFore = 0
        
    def rotateAfterFinger(self,angle):
        deltaAngle = angle - self.angleAfter
        self.angleAfter  = angle
        self.afterFinger.RotateX(deltaAngle)
    
    def rotateMiddleFinger(self,angle):
        deltaAngle = angle - self.angleMiddle
        self.angleMiddle = angle
        self.middleFinger.RotateX(deltaAngle)    

    def rotateForeFinger(self,angle):
        deltaAngle = angle - self.angleFore
        self.angleFore = angle
        self.foreFinger.RotateX(deltaAngle)  
        
    def rotateAll(self,angleA,angleB,angleC):
        self.rotateAfterFinger(angleA)
        self.rotateForeFinger(angleB)
        self.rotateMiddleFinger(angleC)        
        
    def rotateAll(self,angle):
        self.rotateAfterFinger(angle)
        self.rotateForeFinger(angle)
        self.rotateMiddleFinger(angle)
        
class thumbModel(assemblyModel):
    def __init__(self,axesOn = True):
        assemblyModel.__init__(self,axesOn)
        self.thumbDrive = partModel("robot/thumbDrive.stl",True)
        self.finger = fingerModel(True)
        self.finger.setPosition(-63,-72,12)
        self.finger.RotateY(90)
        self.finger.RotateX(-30)
        
        self.thumbDrive.setAxesLength(20)
        self.thumbDrive.setOrigin(6,12,22)
        
        self.thumbDrive.AddModel(self.finger.getAssembly())
        
        self.AddModel(self.thumbDrive.getAssembly())
        
        
class palmModel(assemblyModel):
    def __init__(self ,axesOn = False,parent = None):
        assemblyModel.__init__(self,axesOn)
        self.fingerOne = fingerModel()
        self.fingerTwo = fingerModel()
        self.fingerThree = fingerModel()
        self.fingerFour = fingerModel()
        self.thumb = thumbModel()
        
        self.palm = partModel("robot/palm.stl")
        
        self.fingerOne.setPosition(-10,0,0)
        self.fingerOne.RotateZ(5)
        self.fingerTwo.setPosition(12.5,0,0)
        self.fingerThree.setPosition(37,0,0)
        self.fingerThree.RotateZ(-5)
        self.fingerFour.setPosition(61,0,0)
        self.fingerFour.RotateZ(-10)

        self.palm.AddModel(self.thumb.getAssembly())
        self.palm.AddModel(self.fingerOne.getAssembly())
        self.palm.AddModel(self.fingerTwo.getAssembly())
        self.palm.AddModel(self.fingerThree.getAssembly())
        self.palm.AddModel(self.fingerFour.getAssembly())
        
        self.AddModel(self.palm.getAssembly()) 
        
        self.setOrigin(45,-15,5)
        #self.palm.setColor(0.5,0.6,0.2)
        
        self.thumbAngle = 0
        
    def setFingerAngle(self,angle):
        self.fingerOne.rotateAll(angle)
        
    def rotateThumb(self,angle):
        deltaAngle = angle - self.thumbAngle
        self.thumbAngle = angle        
        self.thumb.RotateY(deltaAngle)
            
class robotModel(assemblyModel):
    def __init__(self,axesOn = False):
        assemblyModel.__init__(self,axesOn)
        
        self.shoulder  = partModel("robot/shoulder.stl")
        self.afterArm  = partModel("robot/afterArm.stl")
        self.middleArm = partModel("robot/middleArm.stl")
        self.foreArm   = partModel("robot/foreArm.stl")  
        self.littleArm   = partModel("robot/littleArm.stl")  
        self.palm = palmModel()
        
        self.palm.setPosition(580,25,0)
        self.palm.RotateZ(-90)  
        self.palm.RotateY(90)
        
        self.shoulder.setAxesLength(100)
        
        self.AddModel(self.shoulder.getAssembly())
        self.shoulder.AddModel(self.afterArm.getAssembly())
        self.afterArm.AddModel(self.middleArm.getAssembly())
        self.middleArm.AddModel(self.foreArm.getAssembly())
        self.foreArm.AddModel(self.littleArm.getAssembly())
        self.littleArm.AddModel(self.palm.getAssembly())
        
        self.shoulder.setOrigin(8,8,8)
        self.afterArm.setOrigin(8,8,8)
        self.middleArm.setOrigin(300,8,8)
        self.foreArm.setAxesLength(100)
        self.foreArm.setOrigin(342,8,8)
        self.littleArm.setOrigin(342,8,8)
        
        self.RotateZ(-90)
        
        self.thumb = self.palm.thumb
        self.fingerOne = self.palm.fingerOne
        self.fingerTwo = self.palm.fingerTwo
        self.fingerThree = self.palm.fingerThree
        self.fingerFour = self.palm.fingerFour
        
    
        self.rotateThumb = self.palm.rotateThumb
        
        self.shoulderX = 0
        self.shoulderZ = 0
        self.armX      = 0
        self.armY      = 0
        self.littleArmX = 0
        self.handX     = 0
        self.handZ     = 0
        
#from left ,front,up watch the scence,positive        
    def rotateShoulderX(self,angle):
        deltaAngle = (-angle) - self.shoulderX
        self.shoulderX = (-angle)
        self.shoulder.RotateY(deltaAngle)
        
    def rotateShoulderZ(self,angle):
        deltaAngle = self.shoulderZ - angle
        self.shoulderZ = angle
        self.afterArm.RotateZ(deltaAngle)
    
    def rotateArmY(self,angle):
        deltaAngle = (-angle) - self.armY
        self.armY = -angle
        self.middleArm.RotateX(deltaAngle)
    
    def rotateArmX(self,angle):
        deltaAngle = -angle - self.armX
        self.armX = -angle
        self.foreArm.RotateY(deltaAngle)
        
    def rotateLittleArmX(self,angle):
        deltaAngle = -angle - self.littleArmX
        self.littleArmX = -angle
        self.littleArm.RotateX(deltaAngle)    
    
    def rotateHandZ(self,angle):
        deltaAngle = -angle - self.handZ
        self.handZ = (-angle)
        self.palm.RotateX(deltaAngle)
    
    def rotateHandX(self,angle):
        deltaAngle = angle - self.handX
        self.handX = angle
        self.palm.RotateZ(deltaAngle)  
        
    def rotateFinger(self,num = [0,1,2,3,4],angle = [0,0,0,0,0]):
        fingerTuple = (self.thumb.finger,self.fingerOne,
                       self.fingerTwo,self.fingerThree,self.fingerFour)
        map(lambda finger,angle:finger.rotateAll(angle),[fingerTuple[i] for i in num ],angle)
        
        
    def controlArm(self,angle):
        rotateFun = [self.rotateShoulderX,self.rotateShoulderZ,self.rotateArmY,
                self.rotateArmX,self.rotateLittleArmX,self.rotateHandX,self.rotateHandZ]
        map((lambda x,y:x(y)),rotateFun,angle)
        
        
class objMoveInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
 
    def __init__(self,parent=None):
        self.AddObserver("RightButtonPressEvent",self.rightButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent",self.rightButtonReleaseEvent)
        
        self.AddObserver("MiddleButtonPressEvent",self.OnRightButtonDown)
        self.AddObserver("MiddleButtonReleaseEvent",self.OnRightButtonUp)
        
        #self.AddObserver("MouseMoveEvent",self.mouseMove)
    
    def mouseMove(self,obj,event):
        print "Move"
 
    def rightButtonPressEvent(self,obj,event):
        print "Right Button pressed"
        pos = obj.GetInteractor().GetEventPosition()
        
        return 0
    
    def rightButtonReleaseEvent(self,obj,event):
        print "Right Button released"
        #self.OnRightButtonUp()
        return  0 

if __name__ == "__main__":
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.5, 0, 1)
    part = robotModel()
    part.controlArm([30 for i in range(7)])
    renderer.AddActor(part.getAssembly())
     
    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(renderer)
     
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renwin)
    style = objMoveInteractorStyle()
    interactor.SetInteractorStyle(style)
     
    interactor.Initialize()
    interactor.Start()
import pickle as pkl

class Axis:
    def __init__(self,x:str,y:str):
        self.x=x
        self.y=y
        self.xlabel=self.x
        self.ylabel=self.y
    def setUnits(self,xUnit:str,yUnit:str):
        self.xUnit=xUnit
        self.yUnit=yUnit
        self.xlabel=self.x+'('+self.xUnit+')'
        self.ylabel=self.y+'('+self.yUnit+')'
def saveToPkl(value):
    with open(f'{value}.pkl','wb') as f:
        pkl.dump(value,f)
def openPkl(fileName:str):
    with open(fileName,'rb') as f:
        res=pkl.load(f)
    return res
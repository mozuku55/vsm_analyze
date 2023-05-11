import pandas as pd
import numpy as np
import sampledata as spl
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
class Data:
    #Dataの用意
    def __init__(self,df:pd.DataFrame,axis:Axis,sampleName):
        self.sampleName=sampleName
        self.df = df
        self.axis = axis
    def __selectAxis(self):
        #Xが左側，yが右側に来る
        self.df=self.df.loc[:,[self.axis.xlabel,self.axis.ylabel]]
    def __parseInt(self,columnHeader:str):
        if np.any(self.df.columns.values==columnHeader):
            self.df[columnHeader]=self.df[columnHeader].map(lambda value:float(value))
    def __parseIntAll(self,columnHeaders:list):
        for header in columnHeaders:
            self.__parseInt(header)
    def makeFigData(self):
        self.__selectAxis()
        self.__parseIntAll([self.axis.xlabel,self.axis.ylabel])
    #解析
    def changeYunitToPerCC(self):
        for key in list(spl.sampleData.keys()):
            if key in self.sampleName:
                V=spl.sampleData[key].width*spl.sampleData[key].length*spl.sampleData[key].height
                self.changeYunit(self.axis.ylabel+'/cc',1/V)
    def changeXunit(self,newunit, c):
        self.df[self.axis.xlabel]=self.df[self.axis.xlabel]*c
        self.axis.xUnit=newunit
        self.df.rename(columns={self.axis.xlabel:self.axis.x+'('+self.axis.xUnit+')'},inplace=True)
        self.axis.xlabel=self.axis.x+'('+self.axis.xUnit+')'
    def changeYunit(self,newunit, c):
        self.df[self.axis.ylabel]=self.df[self.axis.ylabel]*c
        self.axis.yUnit=newunit
        self.df.rename(columns={self.axis.ylabel:self.axis.y+'('+self.axis.yUnit+')'},inplace=True)
        self.axis.ylabel=self.axis.y+'('+self.axis.yUnit+')'
        print(f'yl={self.axis.ylabel}\n')
    def diffential(self):
        self.df[f"{self.axis.ylabel}_diff"]=self.df[self.axis.ylabel].diff()/self.df[self.axis.xlabel].diff()
    def getSampledf(self,width):
        headSample:pd.DataFrame=self.df.head(width)
        tailSample:pd.DataFrame=self.df.tail(width)
        turnIdxs=self.df.loc[self.df[self.axis.xlabel].diff().diff().abs()>1500].index
        midSampleIdxs=[]
        for tIdx in turnIdxs:
            midSampleIdxs+=list(range(max(0,tIdx-width),min(len(self.df.columns.values),tIdx+width)))
        midSample=self.df.iloc[midSampleIdxs,:]
        self.dfSample=pd.concat([headSample,midSample,tailSample])
    def makeDiamagFig(self):
        self.grad=self.dfSample[self.axis.ylabel+"_diff"].mean()
        self.df["deMag("+self.axis.yUnit+")"]=self.df[self.axis.xlabel]*self.grad
    def removeDIamag(self):
        self.df[self.axis.ylabel+'_pure']=self.df[self.axis.ylabel]-self.df["deMag("+self.axis.yUnit+")"]
#面積の導出
def calcArea(df:pd.DataFrame,axis:Axis):
    go_area=0
    back_area=0
    for i in range(len(df[axis.xlabel].to_list())-1):
        d_area=abs(df[axis.ylabel].to_list()[i]+df[axis.ylabel].to_list()[i+1])*abs(df[axis.xlabel].to_list()[i+1]-df[axis.xlabel].to_list()[i])*0.5
        if df[axis.xlabel].to_list()[i+1]-df[axis.xlabel].to_list()[i]>0 and df[axis.xlabel].to_list()[i]>=0:
            go_area+=d_area
        elif df[axis.xlabel].to_list()[i+1]-df[axis.xlabel].to_list()[i]<0 and df[axis.xlabel].to_list()[i]>=0:
           back_area+=d_area
        else:
            continue
    return go_area, back_area
def calc_AreaDiff(indf,outdf,axis:Axis):
    dfin_go, dfin_back=calcArea(indf,axis)
    dfout_go, dfout_back=calcArea(outdf,axis)
    return dfout_go-dfin_go
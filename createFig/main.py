import useCalc as uc
import useFiles as uf
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import sampledata as spl
import statistics as stat
import sys

def main():
    pwd=os.getcwd()
    inputPath = pwd+'/'+sys.argv[1]
    outputPath = pwd+'/'+sys.argv[1]+'-out'
    os.mkdir(outputPath)
    axis=uc.Axis('H','M')
    axis.setUnits('Oe','emu')
    
    axis=createCSV(axis,inputPath,outputPath)
    createFigAndArea(axis, outputPath,outputPath)
    createCompFig(outputPath,outputPath)

def makeFigs(df:pd.DataFrame, samplestr:str, outputPath:str):
    print('called\n')
    plt.scatter(df[df.index.str.contains(samplestr+'-')]['thickness'].to_list()*(10**7), df[df.index.str.contains(samplestr+'-')]['area'].to_list()*(10**6))
    print('picked\n')
    plt.xlabel('thickness(nm)')
    plt.ylabel('K_eff(J/m**3)')
    plt.legend()
    plt.savefig(outputPath+'/thickness-Keff-'+samplestr+'.png')
    print('saved\n')
    plt.close()
    plt.scatter(df[df.index.str.contains(samplestr+'-')]['thickness'].to_list()*(10**7), df[df.index.str.contains(samplestr+'-')]['Ms'].to_list())
    plt.xlabel('thickness(nm)')
    plt.ylabel('Ms(T)')
    plt.legend()
    plt.savefig(outputPath+'/thickness-Ms-'+samplestr+'.png')
    print('saved\n')
    plt.close()

def createCSV(axis:uc.Axis, input_path, output_path):
    inputPath=input_path
    outputPath=output_path
    header='Date,H(Oe),M(emu),Angle(degree)'
    width=2
    files = glob.glob(inputPath+'/*.VSM')
    cnt=0
    
    for f in files:
        filename=f.split('/')[-1].split('_')[0].replace('.VSM','')
        axis.setUnits('Oe','emu')
        for key in list(spl.sampleData.keys()):
            if key in  filename:
                samplename=key
        data=uc.Data(uf.getData(f,header),axis,samplename)
        data.makeFigData()
        data.changeYunitToPerCC()
        data.changeXunit('T',1/10000)
        data.changeYunit('T',4*3.141592653589/10000)
        data.diffential()
        data.getSampledf(width)
        data.makeDiamagFig()
        data.removeDIamag()
        if '-in' in filename:
            uf.overWriteCSV(outputPath,samplename+'-in',data.df)
        elif '-out' in filename:
            uf.overWriteCSV(outputPath,samplename+'-out',data.df)
        cnt+=1
        print(f"{cnt} files have finished\n")
    return data.axis

def createFigAndArea(axis:uc.Axis, input_path:str, output_path:str):
    outputPath=output_path
    inFiles = glob.glob(output_path+'/*-in.csv')
    outFiles = glob.glob(output_path+'/*-out.csv')
    area_dict={}
    for inF in inFiles:
        if inF.replace('-in','-out') in outFiles:
            fileName=inF.split('/')[-1].replace('-in','').replace('.csv','')
            inDf = pd.read_csv(inF)
            outDf = pd.read_csv(inF.replace('-in','-out'))
            fig =plt.figure()
            ax=fig.add_subplot(111)
            ax.plot(inDf[axis.xlabel].to_list(),inDf[axis.ylabel+'_pure'].to_list(),color='red',label='in')
            ax.plot(outDf[axis.xlabel].to_list(),outDf[axis.ylabel+'_pure'].to_list(),color='blue',label='out')
            ax.grid()
            ax.legend()
            ax.set_title(f'{fileName}')
            ax.set_xlabel("$\it{\mu}_0\it{H}$(T)" , fontsize=15)
            ax.set_ylabel("$\it{M}$(T)", fontsize=15)
            fig.tight_layout()
            fig.savefig(outputPath+'/'+fileName+'.png')
            plt.close()
            inaxis=uc.Axis(axis.x,axis.y)
            inaxis.setUnits(axis.xUnit,axis.yUnit)
            outaxis=uc.Axis(axis.x,axis.y)
            outaxis.setUnits(axis.xUnit,axis.yUnit)
            indata=uc.Data(inDf,inaxis,fileName+'=in')
            outdata=uc.Data(outDf,outaxis,fileName+'=out')
            indata.changeXunit('A/m',1/(4*3.141592653589*10**(-7)))
            outdata.changeXunit('A/m',1/(4*3.141592653589*10**(-7)))
            print(f"file={fileName} inmax={inDf[axis.ylabel].max()} outmax={outDf[axis.ylabel].max()}\n")
            area_dict[fileName]=[uc.calc_AreaDiff(indata.df,outdata.df,inaxis),spl.compData[fileName],stat.mean([inDf[axis.ylabel+'_pure'].max(),outDf[axis.ylabel+'_pure'].max()])]
    areadf=pd.DataFrame(area_dict.values(), index=list(area_dict.keys()), columns=['area','thickness','Ms'])
    uf.overWriteCSV(outputPath,'Keff_area',areadf)

def createKeffThickFig(df:pd.DataFrame, name:str, outputPath:str):
    plotx=list(map(lambda x: x*10**7, df[df.index.str.contains(f'{name}-')]['thickness'].to_list()))
    ploty=list(map(lambda y: y*10**(-6), df[df.index.str.contains(f'{name}-')]['area'].to_list()))
    plt.scatter(plotx, ploty)
    plt.xlabel('thickness(nm)',fontsize=15)
    plt.ylabel("$\it{K}_\mathrm{eff}\mathrm{(MJ/m^3)}$",fontsize=15)
    plt.tight_layout()
    plt.savefig(outputPath+f'/thickness-Keff-{name}.png')
    plt.close()
def createMsThickFig(df:pd.DataFrame, name:str, outputPath:str):
    plotx=list(map(lambda x: x*10**7, df[df.index.str.contains(f'{name}-')]['thickness'].to_list()))
    ploty=list(map(lambda y: y, df[df.index.str.contains(f'{name}-')]['Ms'].to_list()))
    plt.scatter(plotx, ploty)
    plt.xlabel('thickness(nm)',fontsize=15)
    plt.ylabel('$\it{M}_\mathrm{s}$(T)',fontsize=15)
    plt.tight_layout()
    plt.savefig(outputPath+f'/thickness-Ms-{name}.png')
    plt.close()

def createCompFig(input_path:str,output_path:str):
    inputPath=input_path
    outputPath=output_path
    df = pd.read_csv(inputPath+'/Keff_area.csv', index_col=0)
    createKeffThickFig(df, 'a', outputPath)
    createMsThickFig(df, 'a', outputPath)
    createKeffThickFig(df, 'b', outputPath)
    createMsThickFig(df, 'b', outputPath)
    createKeffThickFig(df, 'c', outputPath)
    createMsThickFig(df, 'c', outputPath)
main() 
        
        
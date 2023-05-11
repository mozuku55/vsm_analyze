import pandas as pd
import glob
import os
import codecs as cs
def getData(fileName:str,dataHeader:str):
    with cs.open(fileName,'r', 'utf-8', 'ignore') as f:
        lines = f.read().replace('\r','').split("\n")
    f.close()
    print(f"{lines}")
    if not dataHeader in lines:
        return pd.DataFrame([])
    else:
        d_org = pd.Series(lines[lines.index(dataHeader)+1:-1]).str.split(",",expand=True)
        d_org.columns=dataHeader.split(",")
        return d_org
def overWriteCSV(folderPath:str,fileName:str,df:pd.DataFrame):
    file=fileName+'.csv'
    anotherFile = glob.glob(folderPath+'/'+file)
    if len(anotherFile)>0:
        os.remove(folderPath+'/'+file)
        overWriteCSV(folderPath,fileName,df)
    else:
        df.to_csv(folderPath+'/'+file)
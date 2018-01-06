# Selection criterior:
# Each SN in the sample must have at least one observation within 5 days before
# the light curve maximum, and at least one observation within 5 days after the maximum
# This python function is used to calculate the maximum date for all the band
import snpy
from os import listdir
from os.path import isfile,join
import numpy as np

mypath = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/FormatedBVRI/"
outpath = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/DataSelection/Tmax.csv" 

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath,f))]

FilterName = ["B","V","r","i"]
headname = "SN,B,V,r,i,\n"

fout = open(outpath,'w')
fout.write(headname)

for f in range(1,len(onlyfiles)):
    print(f)
    filepath = mypath + onlyfiles[f]
    s = snpy.get_sn(filepath)
    s.fit()
    currLine = onlyfiles[f] + ","
    for I in range(0,len(FilterName)):
        currLine  = currLine + str(s.get_max(FilterName[I])[0]) + "," 
    currLine  = currLine + "\n"
    fout.write(currLine)
fout.close()
    

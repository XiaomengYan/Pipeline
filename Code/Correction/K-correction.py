import snpy
import matplotlib

# ubertemp.py: module to pick  the CSP or Prieto files
## Here: we pick prieto filters
snpy.ubertemp.template_bands = ['Bs', 'Vs', "Rs", 'Is']

#Input variable:
##       s: object obtained by get_sn()
##       ks: s.ks dictionary: a dictionary of computed k-corrections. The index
##                           is the filter name, the calue is an array of k-corrections
##                           one for each observed epoch
##       kspath: store k-corrected data into this path

def kcorr_output(s, ks, kspath):
    ks_keys = ks.keys()
    fout = open(kspath, 'w')
    fout.write("Filter,MJD,Mag,Sigma,Code\n")
    for filterI in range(0, len(ks_keys)):
        ckey = ks_keys[filterI]
        lkey = len(ckey)
        filterName = ckey[0]
        filterCode = ckey[1:lkey]
        ksdata = ks.get(ks_keys[filterI])
        lc = s.data.get(ks_keys[filterI])
        for lineI in range(0, len(ksdata)):
            currLine = filterName + ","
            currLine = currLine + str(lc.MJD[lineI]) + "," + \
                str(lc.magnitude[lineI] - ksdata[lineI]) + "," + \
                str(lc.e_mag[lineI]) + "," + filterCode + "\n"
            fout.write(currLine)
    fout.close()

# s = snpy.get_sn("./data/data_raw_python/SN1998de_LOSS_main.txt")
# s.restbands
# s.replot = 0
# s.fit()
# s.summary()
# s.kcorr()
# s.plot_kcorrs()
# s.plot()
# matplotlib.pyplot.savefig("tmp2.png")

from os import listdir
from os.path import isfile, join


figfolder = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Figs/004kcorr/" # Figure output path
mypath = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/DataSelection/" # Read in path
ksfolder = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/kCorrected/" # File output path

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


for f in range(1, len(onlyfiles)):
    try:
        print f
        filepath = mypath + onlyfiles[f]
        s = snpy.get_sn(filepath)
        s.replot = 0
        s.fit()
        figpath = figfolder + onlyfiles[f] + "lc.png"
        s.plot()
        matplotlib.pyplot.savefig(figpath)
        figpath = figfolder + onlyfiles[f] + "kcorr.png"
        #s.plot_kcorrs()
        #matplotlib.pyplot.savefig(figpath)
        kspath = ksfolder + onlyfiles[f] 
        kspath = kspath.replace("txt", "csv")
        kcorr_output(s, s.ks, kspath)
    except:
        print "ERROR in file: " + str(f)


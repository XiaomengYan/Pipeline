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
# def kcorr_output(s, ks, kspath):
#     ks_keys = ks.keys()
#     fout = open(kspath, 'w')
#     fout.write("Filter,MJD,Mag,Sigma,Code\n")
#     for filterI in range(0, len(ks_keys)):
#         ckey = ks_keys[filterI]
#         lkey = len(ckey)
#         if ckey == "V0":
#            filterName = "V"
#             filterCode = "CSP3014"
#         elif ckey == "V1":
#             filterName = "V"
#             filterCode = "CSP3009"
#         else:
#             filterName = ckey
#             filterCode = "CSP9844"
#         ksdata = ks.get(ks_keys[filterI])
#         lc = s.data.get(ks_keys[filterI])
#         for lineI in range(0, len(ksdata)):
#             currLine = filterName + ","
#             currLine += str(lc.MJD[lineI]) + "," + \
#                 str(lc.magnitude[lineI] - ksdata[lineI]) + "," + \
#                 str(lc.e_mag[lineI]) + "," + \
#                 filterCode + "\n"
#             fout.write(currLine)
#     fout.close()


from os import listdir
from os.path import isfile, join


########## Customer set ##################################################

figfolder = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Figs/ThirdReleaseData/004kcorr/" # Figure output path
mypath = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/ThirdReleaseData/FormateBVRI/" # Read in path
ksfolder = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/ThirdReleaseData/kCorrected/" # File output path
###########################################################################


onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

f = 17
print f
filepath = mypath + onlyfiles[f]
s = snpy.get_sn(filepath)
s.restbands['B'] = 'Bs'
s.restbands['r'] = 'Rs'
s.restbands['i'] = 'Is'
s.restbands['V0'] = 'V'
s.restbands['V'] = 'V'
s.fit()
figpath = figfolder + onlyfiles[f] + "lc.png"
s.plot()
matplotlib.pyplot.savefig(figpath)


# for f in range(0, len(onlyfiles)):
#     f = 17
#     try:
#         print f
#         filepath = mypath + onlyfiles[f]
#         s = snpy.get_sn(filepath)
#         s.replot = 0
#         s.fit()
#         figpath = figfolder + onlyfiles[f] + "lc.png"
#         s.plot()
#         matplotlib.pyplot.savefig(figpath)
#         figpath = figfolder + onlyfiles[f] + "kcorr.png"
#         #s.plot_kcorrs()
#         #matplotlib.pyplot.savefig(figpath)
#         kspath = ksfolder + onlyfiles[f]
#         kspath = kspath.replace("txt", "csv")
#         kcorr_output(s, s.ks, kspath)
#     except:
#         print "ERROR in file: " + str(f)


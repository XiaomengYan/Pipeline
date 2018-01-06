import snpy
import matplotlib

snpy.ubertemp.template_bands = ['Bs', 'Vs', "Rs", 'Is']
filepath = "/Users/yanxiaomeng/Dropbox/project/snoopy/SN1981D.txt"

s = snpy.get_sn(filepath)
s.fit()
ks = s.ks
ks_keys = ks.keys()
kspath = filepath.replace("txt","csv")
fout = open(kspath, 'w')
fout.write("Filter,MJD,Mag,Sigma\n")
for filterI in range(0, len(ks_keys)):
    ckey = ks_keys[filterI]
    lkey = len(ckey)
    filterName = ckey
    #if ckey[1] == "'":
    #    filterName = ckey[0:2]
    #   filterCode = ckey[2:lkey]
    #else:
    #   filterName = ckey[0]
    #    filterCode = ckey[1:lkey]
    ksdata = ks.get(ks_keys[filterI])
    lc = s.data.get(ks_keys[filterI])
    for lineI in range(0, len(ksdata)):
        currLine = filterName + ","
        currLine = currLine + str(lc.MJD[lineI]) + "," + \
            str(lc.magnitude[lineI] - ksdata[lineI]) + "," + \
            str(lc.e_mag[lineI]) + "\n"
         #   filterCode + "\n"
        fout.write(currLine)
fout.close()


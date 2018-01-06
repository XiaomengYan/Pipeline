## Convert Z_helio to Z_cmb
## Using API from https://ned.ipac.caltech.edu


from urllib import urlopen
import ssl
import re
import pandas as pd
import math

df = pd.read_csv("./data/model_v2/coresne_table_withZ.csv")
df['Zcmb_asiago'] = pd.Series(index=df.index)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for rowI in range(0,len(df.index)):
    print rowI
    if math.isnan(df.Zhelio_asiago[rowI]):
        df.Zcmb_asiago[rowI] = -1
        continue
    #if df.kind[rowI] == 'cmb':
    #    df.z_convert[rowI] =df.redshift[rowI]
    #    continue
    speed = 299792.458 * df.Zhelio_asiago[rowI]
    https_path = 'https://ned.ipac.caltech.edu/cgi-bin/velc?lon=' + df.RAX[rowI]
    https_path += '&in_csys=Equatorial&lat=' + df.DECX[rowI]
    https_path += '&in_equinox=J2000.0&vel=' + str(speed)
    https_path += '&vfrom=Heliocentric&vto=3K'
    html = urlopen(https_path, context=ctx)
    html_text = html.read()
    tmp = re.search(r"Output: </strong>(\d+?\.\d+?)",
                    html_text)
    if tmp:
        df['Zcmb_asiago'][rowI] = float(tmp.group(1))/299792.458
    else:
        df['Zcmb_asiago'][rowI] = -1


df.to_csv("./data/model_v2/coresne_table_withZ2.csv", index=False)

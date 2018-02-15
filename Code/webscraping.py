## Generate a supernova table
## This is from a folder of light curves.
## Webscraping from https://ned.ipac.caltech.edu

from urllib.request import urlopen
import ssl
import re
from os import listdir
import pandas as pd


################### Customer setting######################################
myPath = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/ThirdReleaseData/kCorrected/"
outputfile = "/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/ThirdReleaseData/model_v2/coresne_table.csv"
##############################################################################












onlyFiles = [f for f in listdir(myPath) if re.search(r'csv', f)]
nFiles = len(onlyFiles)
colNames = ['SN', 'Survey','snetype', 'Type', 'AB', 'AV',
            'AR', 'AI', 'sdssr', 'sdssi',
            'RAX','DECX','Zcmb']

df = pd.DataFrame(index=range(0, nFiles),
                  columns=colNames,
                  dtype='object')

redshiftdf = pd.read_csv("/Users/yanxiaomeng/Dropbox/project/snoopy/pipeline/Data/ThirdReleaseData/Redshift.csv")

for rowI in range(0, nFiles):
    print(onlyFiles[rowI].replace(".csv", "").split("_"))
    sneName = onlyFiles[rowI].replace(".csv", "").split("_")[0]
    survey = onlyFiles[rowI].replace(".csv", "").split("_")[1]
    snetype = onlyFiles[rowI].replace(".csv", "").split("_")[2]
    df['SN'][rowI] = sneName
    df['Survey'][rowI] = survey
    df['snetype'][rowI] = snetype
    df['SN'][rowI] = sneName
    df['Survey'][rowI] = survey
    df['snetype'][rowI] = snetype
    print(rowI)
    print(sneName)
    # connection
    objName = sneName
    https_path = 'https://ned.ipac.caltech.edu/cgi-bin/objsearch?objname='''
    https_path += objName
    https_path += '&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&'
    https_path += 'obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    html = urlopen(https_path,context=ctx)
    html_text = html.read().decode('utf-8')
    #SNE Type
    tmp = re.search(r"SuperNova Type\s+?:\s*?(\w+)",html_text)
    if tmp:
      df['Type'][rowI] = tmp.group(1)
    else:
      df['Type'][rowI] = "-1"
    
    # extinction
    tmp = re.search(r"<td>Landolt</td><td>B</td><td>.*?</td><td>\s*?(\d*?\.\d*?)\s*?</td>",
                    html_text)
    if tmp:
        df['AB'][rowI] = tmp.group(1)
    else:
        df['AB'][rowI] = -1
    tmp = re.search(r"<td>Landolt</td><td>V</td><td>.*?</td><td>\s*?(\d*?\.\d*?)\s*?</td>",
                    html_text)
    if tmp:
        df['AV'][rowI] = tmp.group(1)
    else:
        df['AV'][rowI] = -1
        
    tmp = re.search(r"<td>Landolt</td><td>R</td><td>.*?</td><td>\s*?(\d*?\.\d*?)\s*?</td>",
                    html_text)
    if tmp:
        df['AR'][rowI] = tmp.group(1)
    else:
        df['AR'][rowI] = -1

    tmp = re.search(r"<td>Landolt</td><td>I</td><td>.*?</td><td>\s*?(\d*?\.\d*?)\s*?</td>",
                        html_text)
    if tmp:
        df['AI'][rowI] = tmp.group(1)
    else:
        df['AI'][rowI] = -1

    tmp = re.search(r"<td>SDSS</td><td>r</td><td>.*?</td><td>\s*?(\d*?\.\d*?)\s*?</td>",
                        html_text)
    if tmp:
        df['sdssr'][rowI] = tmp.group(1)
    else:
        df['sdssr'][rowI] = -1

    tmp = re.search(r"<td>SDSS</td><td>i</td><td>.*?</td><td>\s*?(\d*?\.\d*?)\s*?</td>",
                        html_text)
    if tmp:
        df['sdssi'][rowI] = tmp.group(1)
    else:
        df['sdssi'][rowI] = -1

    tmp = re.search(r"\d\dh\d\dm\d+?\.\d+?s",
                        html_text)
    if tmp:
        df['RAX'][rowI] = tmp.group(0)
    else:
        df['RAX'][rowI] = -1

    tmp = re.search(r"[+-]\d\dd\d\dm\d+?\.\d+?s",
                        html_text)
    if tmp:
        df['DECX'][rowI] = tmp.group(0)
    else:
        df['DECX'][rowI] = -1
    df['Zcmb'][rowI] =  redshiftdf['Zcmb'][rowI]

df.to_csv(outputfile, index=False)
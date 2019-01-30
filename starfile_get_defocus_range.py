#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        else:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

if len(sys.argv) != 2:
    sys.exit("USAGE: starfile_get_defocus_range.py <star file>")

(labels,header,data) = read_starfile(sys.argv[1])
defoci = []
for i in data:
    defocus = (float(i[labels['_rlnDefocusU ']]) + float(i[labels['_rlnDefocusV ']]))/2.0
    defoci.append(defocus*0.0001)

print '''
{0} particles

Min defocus: {1}
Max defocus: {2}
'''.format(len(defoci),min(defoci),max(defoci))

binvals = []
binval=0
for i in range(0,int(max(defoci)*2)+2):
    binvals.append(binval)
    binval+=0.5
plt.hist(defoci,bins=binvals)
plt.title('{0} - {1} particles'.format(sys.argv[1].split('/')[-1].replace('.star',''),len(defoci)))
plt.xlabel('defocus (uM)')
plt.ylabel('particles')
plt.savefig('defocus_analysis.png')

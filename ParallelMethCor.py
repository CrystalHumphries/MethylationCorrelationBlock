#/isb/chumphri/anaconda/bin/python
__author__ = 'chumphri'

import pandas as pd
from scipy.stats import pearsonr
import numpy as np
from multiprocessing import Process

distance = [100,300,500, 1000, 5000, 10000, 15000, 20000, 30000, 40000, 50000, 100000]
betaFile = '/isb/chumphri/CpG_Correlation/batchCorrelatedMeth.txt'
f = '/isb/chumphri/CpG_Correlation/Blocks_correlation_info.txt'
print "hello"

def get_correl (CpG, List):
    new = []
    a = beta.loc[CpG]
    for c in List:
        b    = beta.loc[c]
        e    = pearsonr(a,b)[0]
        new  = np.append(new, e)


    if any(new):
        newm = new.mean()
        newm = np.around(newm, decimals=4)
    else:
        newm=0
    return(newm)

def grab_CpG_sites(chr, dist, init_loc, interval):
    if (dist == 100):
        dist_start = init_loc + dist
        dist_stop  = init_loc + dist
        listCpG    = df[ (df[ 'Pos']>= dist_start)& (df['Pos']< dist_stop) & (df['Chr']==chr)]['CpGSites']
        listCpG    = listCpG.tolist()

    else:
         # intervals downstream of CpG site
        dist_start = init_loc - dist
        dist_stop  = init_loc - dist + interval
        a = df[ (df[ 'Pos']>= dist_start)& (df['Pos']< dist_stop) & (df['Chr']==chr)]['CpGSites']
        # intervals upstream of CpG Site
        dist_start = init_loc + dist
        dist_stop  = init_loc + dist - interval
        b = df[ (df[ 'Pos']>= dist_stop)& (df['Pos']< dist_start) & (df['Chr']==chr)]['CpGSites']
        listCpG = a.append(b)
        listCpG = listCpG.tolist()
    return listCpG


def main_stuff(start, end, name, proc):
    myfile = open(name, 'w')
#    with open (name, "a")  as myfile:
        #CpGList = df.CpGSites[start:end]
    CpGList  = list_temp[start:end]
    print name
    print len(CpGList)
    myfile.write("##RANDOM file:" + str(a))
    for CpG in CpGList:
        chr = df.Chr.where(df.CpGSites==CpG).max()
        init_loc = df.Pos.where(df.CpGSites==CpG).max()
        theList = []
        for i in range(0, len(distance)):
            interval = 0
            dist = distance[i]
            if (i>0):
                interval = distance[i] - distance[i-1]
                
            tempList = grab_CpG_sites(chr, dist, init_loc, interval)
            if len(tempList) ==1 and 0 in tempList:
                cor = 'NaN'
            else:
                cor   = get_correl(CpG, tempList)

            theList = np.append(theList, cor)
            
        final = CpG + str(theList)
        final = final.replace('[', ' ')
        final = final.replace('\n', '')
        final = final.replace(']', '')
        myfile.write(final+"\n")
    myfile.close()

df = pd.io.parsers.read_table(f)
beta = pd.io.parsers.read_table(betaFile)
df =  df.loc[df['CpGSites'].isin(beta.index)]
list_temp = df.CpGSites

#p = "/Users/chumphri/Projects/MethylationLD/DataAnalysis/Correlation_real.txt", "a" "" #as myfile:
#p = Process(target=main_stuff, args=(0,10,"process1",))
#p.start()
#p2 = Process(target=main_stuff, args=(11,20,"process2",))
#p2.start()
#p.join()
#p2.join()

start = 0
file_list = []
processes = []

for a in range(1,11):
    increment = 22156
    stop      = increment + start #a
    dir       = "/isb/chumphri/CpG_Correlation/"
    temp_file = dir + "CpGsites." + str(a) + ".txt"
    temp_start = start + 1
    p = Process(target=main_stuff, args=(temp_start, stop, temp_file, a))
    p.start()
#    p.join()
    start   = stop
    file_list.append(temp_file)
    processes.append(p)

for p in processes:
        p.join()

files =  " ".join(file_list)
last_line = "cat " + files + " > CpG_final_correlation.txt"


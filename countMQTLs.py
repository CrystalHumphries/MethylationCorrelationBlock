import pandas as pd
import time
import sys

def calculate_pos(Var, CpG):
    CpG_loc = float(CpG.split('_')[-1])
    Var_loc = float(Var.split('_')[-1])
    return Var_loc - CpG_loc

def add_pos(fdr, beta):
    if (float(fdr)<0.01) and (float(beta)>0):
        return 1
    elif (float(fdr)<0.01) and (float(beta)<0):
        return 2
    else:
        return 3

startTime = time.time()

dict_pos = range(int(-1e6),int(1000001))
dict_all = dict((k,["NA", 0,0,0]) for k in dict_pos)

#run file
n = 0

for line in sys.stdin:
    n+=1
    line = line.rstrip("\n")
    Var, CpG, beta, t_stat, pval, fdr = line.split('\t')
    pos  = int(calculate_pos(Var, CpG))
    loc  = add_pos(fdr, beta)
    dict_all[ pos][loc]+=1
    if n % 100 ==0:
        print "*",

#print dictionary
outputfile=sys.argv[1]
with open(outputfile, "w") as newFH:
    for num in dict_pos:
        a = map(str, dict_all[num])
        a.insert(0,str(num))
        line = "\t".join(a) + "\n"
        newFH.write(line)

elapsedTime = time.time() - startTime
print('finished in {} ms'.format(int(elapsedTime * 1000)))
print n

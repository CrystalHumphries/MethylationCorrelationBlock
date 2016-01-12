import os
import sys

total_num = int(sys.argv[1])
print total_num

def SED_sub(orig, new):
    new = new.replace("/", "\/")
    temp = 's/' + orig + '/' + new + '/g;'
    return(temp)

old_num   = 0
rounds    = 0
for i in xrange(0,total_num, 5):
    if i ==0:
        continue
    rounds +=1
    range = str(old_num) + "_" + str(i)
    new_file = " run_permutations." + range+ ".pbs"
    cmd = "sed -e '" + SED_sub("PERMNUMBER", str(rounds)) + SED_sub("RANGE",range) + SED_sub("START", str(old_num)) + SED_sub("STOP", str(i)) + SED_sub("RUNTHISFILE", "matrixMQTL.1mb.temp." + str(rounds) + ".R") + "' " + "/path/to/file/run_permutations.pbs  > " + new_file
    os.system(cmd)
    print cmd
    os.system("qsub" + new_file)
    print ("qsub" + new_file)
    old_num = i + 1

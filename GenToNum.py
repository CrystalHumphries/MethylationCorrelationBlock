#!/isb/to/chumphri/anaconda/bin/python
import sys
import re

def header(first):
    first = first.rstrip('\n')
    first = re.sub("M-","", first)
    furs  = first.split('\t')

    for i,k in enumerate(furs):
        furs[i] = k+"-FAM"
    furs.pop(0)
    furs[0]= "rownames"
    new_line = "\t".join(furs)
    return(new_line)
    
#f = open(, 'r')
#first_line = next(f)
#header = header(first_line)
#print header


mapping = [ ('0/0', '0'), ('0/1', '1'), ('1/0', '1'), ('1/1', '2')]
line_counter=1
for line in sys.stdin:
    if line_counter == 1:
         new_header = header(line)
         print new_header

    for k,v in mapping:
        line = line.rstrip('\n')
        line = line.replace(k,v)

    line = re.sub("\./\.|\./1|\./0|1/\.|0/\.", "NA", line)
    line = line.split('\t')
    chr = line.pop(0)
    pos = line.pop(0)
    first = "C:GNMC:Data:" + chr + "_" + str(pos)
    line.insert(0, first)
    line_counter += 1
    print "\t".join(line)


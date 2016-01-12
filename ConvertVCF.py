import gzip
import sys
import re

File = sys.argv[1]
#f = gzip.open('file.txt.gz', 'wb')
with gzip.open(File, 'r') as f:
    for line in f:
        li=line.strip()
        if not li.startswith("##"):
            if li.startswith("#CHROM"):
                new = re.sub('[A-z]{1,3}-', '', li)
                print new
            else:
                new = li.split()
                new[2]= new[0]+"_" + new[1]
                print '\t'.join(new)
                

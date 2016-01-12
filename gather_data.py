import sys

f = open(sys.argv[1], 'r')

location = []

for line in f:
    line = line.rstrip('\n')
    loc, gene = line.split('\t')
    location.append(loc)

with open(sys.argv[2], 'r') as fp:
    for line in fp:
        line = line.rstrip('\n')
        loc  = line.split('\t')
        if (loc[0] in location):
            print line


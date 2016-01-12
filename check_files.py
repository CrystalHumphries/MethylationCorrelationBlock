import os
import sys
import glob
import subprocess

files = glob.glob('/path/to/file/pop_mQTLS/MQL_res.*.*.out')

for fh in files:
    process = subprocess.Popen(["grep", "Task finished in", fh], stdout=subprocess.PIPE)
#    stdout, stderr = process.communicate()
    dim = []
    for line in iter(process.stdout.readline, ''):
        dim.append(line.rstrip('\n'))
    last = dim[-1]
    time = last.split(' ')
    x    = float(time[4])
    if (x < 100):
        print fh




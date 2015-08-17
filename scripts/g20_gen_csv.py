#!/bin/python3.3
import os, re

rr = 50
it = 500

def fill_csv(i, j):
    match='%d,%d,'%(i, j)
    #~ print(match)
    with open('output.txt') as out:
        for line in out.readlines()[1:]:
            temp = re.findall(r'[\d.]+', line)
            match+=temp[0]+' ms,'
            #~ print(temp[0])
        #~ print(match)
        val = os.system('echo %s >> ./data/g20_lab05data_02.csv' % match)


for i in range(1, it + 1) :
    for j in range(1, rr + 1) :
        os.system('./bin/cs296_base %d > output.txt' % i)
        fill_csv(i, j)
    
    os.system('rm output.txt')

#~ fill_csv(1,10)

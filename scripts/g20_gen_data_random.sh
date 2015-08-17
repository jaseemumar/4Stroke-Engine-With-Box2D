#!/bin/bash

# replace with file to read
FILE=./data/g20_project_bash.csv
SELECT=5 #this selects the number of random number to be selected that is in our case 15
ReRUNS=50
ITER=500
# count number of lines
#~ NUM=$(wc - l < ${FILE})
#~ NUM=$(echo $(awk -F, 'END{print NR}' $FILE))
NUM=$ReRUNS
# generate random number in range 0-NUM
j=0
while [ $j -lt $ITER ]
do
i=0
while [ $i -lt $SELECT ]
do
X=$((${RANDOM} % ${NUM} + 1 + ${j}*${ReRUNS})) #$(()) does arithematic manipulation
#~ echo $X
echo "$(sed -n ${X}p ${FILE})" >> ./data/g20_project_bashrandom.csv
i=$[$i+1]
j=$[$j+1]
done
done

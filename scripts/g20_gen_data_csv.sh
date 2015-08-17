#!/bin/sh
ReRUNS=51
ITER=501

row_entries()
{
	while read -r iter
	do
	read -r step
    read -r collision
    read -r velocity
    read -r position
    read -r loop 
	newiter=$(echo $iter|rev|cut -f1 -d' '|rev)
	collisionTime=$(echo $collision|rev|cut -f2 -d' '|rev)
	velocityTime=$(echo $velocity|rev|cut -f2 -d' '|rev)
	positionTime=$(echo $position|rev|cut -f2 -d' '|rev)
	loopTime=$(echo $loop|rev|cut -f2 -d' '|rev)
	stepTime=$(echo $step|rev|cut -f2 -d' '|rev)
    echo "${newiter},$1,${stepTime},${collisionTime},${velocityTime},${positionTime},${loopTime}" >> ./data/g20_project_bash.csv
	done
}
i=1
while [ $i -lt $ITER ]
do
j=1
while [ $j -lt $ReRUNS ]
do
./bin/cs296_base $i| row_entries $j
j=$[$j+1]
done
i=$[$i+1]
done

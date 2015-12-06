#!/usr/bin/env bash
#name=$(basename $1)
STARTTIME=$(date +%s.%3N)
bzcat -f $1 | ~/bin/cudf2lp | gringo -t cudflp2edges.lp - | grep '^edge' |  gawk -F ',' '{gsub(/^edge/,""); gsub(/[\(:"\-+\.\)]/,""); print "edge(\""$1$2"\""",""\""$3$4"\")."}' | gringo -t vertex.lp - | sed 's/[:"]//g' > $1.graph
ENDTIME=$(date +%s.%3N)
runtime=$(echo $ENDTIME - $STARTTIME | bc)
echo 'instance,runtime in s,method' > $1.graph.log
echo "$1,$runtime,graph" >> $1.graph.log

#TODO:
#clique
#component
#maxversion
#component
#installed
#request

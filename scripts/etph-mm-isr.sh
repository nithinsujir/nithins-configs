#!/bin/bash

tb3s=( 0109-1414-420
0109-1414-149
0109-1414-413
0109-1420-433
0109-1411-054
0109-1414-833
0109-1414-425
0109-1407-002
0109-1407-001
0109-1411-595
0109-1411-734
0109-1411-436
0109-1411-919
0109-1414-121
0109-1414-251
0109-1420-169
0109-1420-196
0109-1414-725
0109-1419-918
0109-1419-602
0109-1419-991
)

time=$1

for tb3 in ${tb3s[@]} ; do
	echo $tb3
	wget -T 99999 http://etph.tintri.com/schema/$tb3/$time/varLogMessagesBothControllers/filter%28str%28line%29.find%28%27IO%20timeout%27%29%3E0%29csv%28systemSerialNumber,timestamp,report.summary.OS,report.summary.nodename,line%29 -O $tb3.log &
	#wget -T 99999 http://etph.tintri.com/schema/$tb3/$time/varLogMessagesBothControllers/filter%28str%28line%29.find%28%27MM0:%20CSR%27%29%3E0%29csv%28systemSerialNumber,timestamp,report.summary.OS,report.summary.nodename,line%29 -O $tb3.log &
done

wait


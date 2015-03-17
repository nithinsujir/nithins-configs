#!/bin/bash
NVCFG=/tmp/nvperf.cfg
reqsize=16384
numthreads=10
compress=false

while getopts 's:t:c' OPTION
do
	case $OPTION in
		s) reqsize=$OPTARG
			;;
		t) numthreads=$OPTARG
			;;
		c) compress=true
			;;
	esac
done



/bin/cat > $NVCFG <<-EOF
{
	"useFiles" : false,
	"echoToScreen" : true,
	"nvperfRequestSize": $reqsize,
	"nvperfNumThreads": $numthreads,
	"nvperfCompress": $compress,
	"nvperfMirrorNv": true,
	"nvperfAddHeader": true,
	"nvperfHeaderSize": 1536
}
EOF

./nvperf -c $NVCFG


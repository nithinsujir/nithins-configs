#!/bin/bash
START=$1
END=$2

for ((i=$START; i>=$END; i--)); do
	cs=$(hg log -r $i | head -n 1 | sed 's/.*://')
	bug=$(hg log -r $i | grep summary | sed 's/.* bug/bug/' | sed 's/:.*//')
	echo "$bug: Backout change $cs for 4.0.0.8 per PM instructions" > /tmp/msg.txt
	echo "Original change: " >> /tmp/msg.txt
	hg log -r $i >> /tmp/msg.txt

	hg backout $i --commit -l /tmp/msg.txt
done


fils=`p4 opened ... | grep -v "delete" | sed 's/#.*//;' | p4 -x - where |  sed 's/.*\/\/.* \//\//'`; 
gvim $fils

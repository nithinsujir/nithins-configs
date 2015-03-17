fils=`p4 opened ... | sed 's/#.*//' | sed 's/.*nsujir\///'`
#echo $fils;

for f in $fils ;
do
    p4 revert $f;
    p4 edit $f;
    echo $f;
done

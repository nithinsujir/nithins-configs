dest=$1

if [ $# -lt 1 ]
then
    echo "Need dest folder";
    exit;
fi

fils=`p4 opened ... | grep add | sed 's/#.*//' | sed 's/.*nsujir\///' | sed 's/.*main\///'`

for f in $fils ;
do
gvimdiff $dest$f $f
done

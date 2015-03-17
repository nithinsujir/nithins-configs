if [ $# -lt 1 ]
then
    echo "$0 <changelist>";
    exit 1;
fi

svn diff /home/nsujir/ws_svn/$1 | kompare -

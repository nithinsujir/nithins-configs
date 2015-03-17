backupdir='/home/nsujir/backups'
export P4USER=nsujir

#backup <client> <client dir>
backup()
{
    export P4CLIENT=$1;
    cd $2;

    fils=`/bin/p4 opened | wc -l`;
    if [ $fils -ne 0 ] 
    then
        fils=`/bin/p4 opened | grep -v "delete" | sed 's/#.*//;' | /bin/p4 -x - where |  sed 's/.*\/\/.* \//\//'`; 

        tar cf /tmp/bak.tar $fils;
        last_update=`ls -t $backupdir/${P4CLIENT} | head -n 1`;

        difs=`diff /tmp/bak.tar $backupdir/$P4CLIENT/$last_update | grep differ | wc -l`;


        if [ $difs -ne 0 ]
        then
            cp /tmp/bak.tar $backupdir/${P4CLIENT}/$(date +%d%b%y-%H%M).tar;
            echo "Saved $(date +%d%b%y-%H%M).tar";
        else
            echo "No differences since previous backup for client $P4CLIENT";
        fi

    else
        echo "No open files for $P4CLIENT";
        echo "fils: $fils"
    fi

    # Generate cscope
    cd src_ne
    /bin/bash /home/nsujir/bin/cs.sh
}

backup nsujir-rb /home/nsujir/dawn_v1/xtndev/


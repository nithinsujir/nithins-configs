backupdir='/home/nsujir/hdrive/backups'
export P4USER=nsujir

#backup <client> <client dir>
backup()
{
    export P4CLIENT=$1;
    cd $2;

    fils=`/home/nsujir/bin/p4 opened | wc -l`;
    if [ $fils -ne 0 ] 
    then
        fils=`/home/nsujir/bin/p4 opened | grep -v "delete" | sed 's/#.*//;' | /home/nsujir/bin/p4 -x - where |  sed 's/.*\/\/.* \//\//'`; 

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
    sh /home/nsujir/bin/cs.sh
}

backup nsujir-1 /home/nsujir/dawn_v1/main/
backup nsujir-2 /home/nsujir/client2/dawn_v1/main/


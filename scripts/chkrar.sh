#!/bin/bash

find . -type f -name '*.rar' -print0 | while read -d $'\0' file
do
    # skip loop iteration if file no longer exists
    if [[ ! -f "$file" ]] ; then continue; fi
    #echo "$file"
    
    unrar t -idq "$file"
    RETVAL=$?
    
    case $RETVAL in
        # 0=success, archive file is okay
        0) 
            echo "OK: $file"
            ;;
        
        # codes that indicate a broken archive
        3) 
            echo "BROKEN($RETVAL): $file"
            mv "$file" "$file.broken"
            ;;
            
        # probably indicates wrong format (ZIP or 7Z file as RAR)
        10) 
            echo "WRONGFORMAT($RETVAL): $file"
            mv "$file" "$file.wrongformat"
            ;;
            
        # user pressed ctrl-C or break or killed the process    
        255) 
            echo "USER ABORT: $file"
            ;;
            
        # other errors
        *) 
            echo "ERROR($RETVAL): $file"
            ;;
    esac
done


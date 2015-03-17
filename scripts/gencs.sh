#!/bin/bash
set -x

gencs()
{
    export P4CLIENT=$1;
    echo $2
    cd $2

    # Generate cscope
    echo "Generating cscope for $2"
    cd src_ne
    /bin/bash /home/nsujir/bin/cs.sh
}


gencs nsujir-1 /home/nsujir/dawn_v1/main/
#gencs nsujir-1 /home/nsujir/dawn_v1/ganga/
gencs nsujir-1 /home/nsujir/dawn_v1/xtndev/

#gencs nsujir-2 /home/nsujir/client2/dawn_v1/main/
gencs nsujir-2 /home/nsujir/client2/dawn_v1/xtndev/

#gencs nsujir-3 /home/nsujir/client3/dawn_v1/main/


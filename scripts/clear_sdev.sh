#!/bin/bash

sdev=$1
sg_persist -s $sdev
sg_persist -o -I -S badbad -Z $sdev
sg_persist -s $sdev
sg_persist -o -C -K badbad $sdev
sg_persist -s $sdev

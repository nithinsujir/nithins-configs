#!/bin/bash

REMOTE=nsujir-vm
rsync -av --delete $HOME/nithins-configs $REMOTE:nlap-backups
rsync -av --delete $HOME/tintri $REMOTE:nlap-backups

#!/bin/bash
# borg backup sample
#borg create -v -s /media/hdd1/borg-backup/::ds-cron-$(date +%F-%s) /media/hdd2/data-source/ 2>&1 | tee -a /tmp/borgbackup.log


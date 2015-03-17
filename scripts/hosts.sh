#!/bin/bash

set -x

sudo grep -v nnshost /etc/hosts > /tmp/hosts
sudo cat nithins-configs/hosts >> /tmp/hosts
sudo cp /tmp/hosts /etc/hosts

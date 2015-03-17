#!/bin/bash

sudo groupadd wireshark
sudo usermod -a -G wireshark nsujir
newgrp wireshark
sudo chgrp wireshark `which dumpcap`
sudo chmod 750 `which dumpcap`
sudo setcap cap_net_raw,cap_net_admin=eip `which dumpcap`

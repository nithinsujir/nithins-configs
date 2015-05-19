#!/bin/bash

dirs=(
	/data/workspaces/build0
	/data2/workspaces/build2
	/data2/workspaces/build3
	/data3/workspaces/build1
	/data3/workspaces/build4
	/data3/workspaces/build5
	/data3/workspaces/build6
)

for d in ${dirs[@]}; do
	/usr/sbin/tmpwatch -mvf 7d ${d}/distro_bld
	/usr/sbin/tmpwatch -mvf 7d ${d}/kbuild/install.d
done


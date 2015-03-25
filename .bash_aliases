#!/bin/bash
alias a2c='aria2c -s 8 -x 8'
alias ac='autoconf'
alias acs='apt-cache search'
alias ag='alias | grep'
alias am='automake'
alias app='sudo aptitude purge ~c'
alias bdr='DEB_BUILD_OPTIONS='parallel=8' fakeroot debian/rules binary'
alias c="clear"
alias cho='sudo chown -R nsujir'
alias ckp='echo "Signed-off-by: Nithin Sujir" > /tmp/gdckpatch && git diff >> /tmp/gdckpatch && git diff --cached >> /tmp/gdckpatch && ./scripts/checkpatch.pl /tmp/gdckpatch'
alias cls='clear;ls'
alias cpi='cat /proc/interrupts'
alias cpu='cat /proc/cpuinfo'
alias d='cd ..'
alias dg='distccmon-gnome &'
alias dis='disper -d DFP-0,DFP-1 -e'
alias disl='disper -d DFP-3 -c'
alias e='evince'
alias eg="export P4DIFF='gvimdiff -f'"
alias elm='echo "================================= `date` =============================" >> /var/log/messages'
alias ep="export P4DIFF='diff -bru'"
alias f='sudo find . -iname'
alias g4='bash ~/bin/p4.sh'
alias gar='git am --reject'
alias gcp='git cherry-pick'
alias gd='gitvimdiff -g'
alias gg4="git status | grep -e modified -e new | awk '{print \$4;}' | xargs gvim"
alias ggc='git gc'
alias gg="git status | grep -e modified -e new | awk '{print \$3;}' | xargs gvim"
alias g='gvim -geometry 135x60'
alias gia='mkdir -p patches/$(cur_git_branch);git format-patch -s -o patches/$(cur_git_branch)/`date +"%b-%d__%H.%M"`'
alias gib='git branch'
alias gica='git commit --amend'
alias gicb='git checkout -b'
alias gic='git commit'
alias gic.='git commit -am .'
alias gich='git checkout'
alias gicl='git clone'
alias gidc='git diff --cached'
alias gid='git diff'
alias gie='git send-email --no-signed-off-by-cc --smtp-server=mail.broadcom.com'
alias GIE='git send-email --smtp-server=mail.broadcom.com'
alias GIENDEV='git send-email --smtp-server=mail.broadcom.com --to davem@davemloft.net --cc netdev@vger.kernel.org'
alias giendev='git send-email --smtp-server=mail.broadcom.com --to davem@davemloft.net --cc netdev@vger.kernel.org --dry-run'
alias gien='git send-email --suppress-cc=all --no-signed-off-by-cc --smtp-server=mail.broadcom.com --to nsujir@broadcom.com'
alias GIES='git send-email --smtp-server=mail.broadcom.com --to stable@vger.kernel.org'
alias gif='git format-patch -s'
alias gi='grep -I -i'
alias gih='git help'
alias gil='git log'
alias gimb='git checkout master; git branch'
alias gim='git checkout master'
alias gin='git init && git add . && git commit -am "init" && git gc'
alias gio='git log origin..'
alias gip='git pull'
alias gir='git reset'
alias GIR='git reset --hard'
alias girH='git rebase -i HEAD~15'
alias girh='git rebase -i HEAD~5'
alias giri='git rebase -i'
alias GIS='git reset --soft'
alias gis='git status'
alias giu='git update-index --assume-unchanged'
alias gmm='git merge master'
alias golv='git am --resolved'
alias gow='git show'
alias gpr='git p4 rebase'
alias gps='git p4 sync'
alias grm='git rebase master'
alias gs='gvim -S .gvimsession'
alias gtc='git tag --contains'
alias gt='gnome-terminal &'
alias ho='cd;rs;./nc/scripts/hosts.sh;cd -'
alias ifc='ifconfig'
alias ind='indent -nbad -bap -nbc -bbo -hnl -br -brs -c33 -cd33 -ncdb -ce -ci4 -cli0 -d0 -di1 -nfc1 -i8 -ip0 -l80 -lp -npcs -nprs -npsl -sai -saf -saw -ncs -nsc -sob -nfca -cp33 -ss -ts8 -il1'
alias k='killall -9'
alias la='ls -A'
alias lg='ssh lg'
alias lld='ll | grep ^d'
alias ll='ls -l --color'
alias l='ls -CF'
alias lnd='ls -l /sys/class/net/*/device'
alias loc='locate -i'
alias lsb='lspci | grep Broadcom'
alias lse='lspci | grep Ethernet'
#alias ls='ls --color'
alias lss='lsscsi'
alias mcl='make clean'
alias mc='make menuconfig'
alias md='mkdir'
alias mi='make install'
alias mj='export CPUS=`grep processor /proc/cpuinfo | wc -l`; make -j $[$CPUS*2]'
alias mjmi='export CPUS=`grep processor /proc/cpuinfo | wc -l`; make -j $[$CPUS*2] && sudo make modules_install && sudo make install && sync'
alias mki='mkisofs -l'
alias mm='export CPUS=`grep processor /proc/cpuinfo | wc -l`; make modules -j $[$CPUS*2]'
alias mmi='sudo make modules_install && sync'
alias mmmi='export CPUS=`grep processor /proc/cpuinfo | wc -l`; make modules -j $[$CPUS*2] && sudo make modules_install && sync'
alias mn='mount /media/nseg'
alias mps='ps -eo pid,ppid,rss,vsize,pcpu,cmd --sort=vsize'
alias nd='ssh -X ndesk'
alias nme='sudo nm-connection-editor'
alias od='objdump -Sld'
alias p4b='bash ~/bin/p4bak.sh'
alias p4d='p4 diff ...'
alias pl='p4 login'
alias p='ping google.com'
alias rba='rpmbuild -ba'
alias rbb='rpmbuild -bb'
#alias rs='rsync -r nsujir@nsujir-vm:nithins-configs $HOME --delete'
alias rss='python $HOME/nithins-configs/python/rssh.py'
alias saar='sudo apt-get autoremove'
alias sai='sudo apt-get install'
alias sar='sudo apt-get remove --purge'
alias saud='sudo apt-get dist-upgrade -y'
alias saug='sudo apt-get upgrade'
alias sau='sudo apt-get update'
alias scp='scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
alias sda='sudo depmod -a'
alias sdc='sudo dmesg -c'
alias sdn='sudo dmesg -n8'
alias sd='sudo dhclient'
alias see='sudo ethtool --show-eee'
alias sei='sudo ethtool -i'
alias sek='sudo ethtool -k'
alias seK='sudo ethtool -K'
alias sese='sudo ethtool --set-eee'
alias se='sudo ethtool'
alias sget='aria2c --ftp-user=partnernet --ftp-passwd=code.10 -s 8 -x 8'
alias si='sudo ifconfig'
alias SI='sudo init 0'
alias skd='sudo killall dhclient'
alias skm='sudo killall -9 minicom'
alias sk='sudo killall -9'
alias smc='mount /media/scratch'
alias smi='sudo make install'
alias smn='mount /media/nseg'
alias sm='sudo minicom'
alias smt='sudo mii-tool -vvv'
alias snr='sudo service network-manager restart'
alias spz='sudo pain -Z'
alias ssh='ssh -X -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
alias ss='sudo setpci -s'
alias s='sudo'
alias sv='sudo vpnc'
alias syi='sudo yum install -y'
alias syr='sudo yum remove'
alias sys='sudo yum search'
alias sy='sync';
alias syu='sudo yum update'
alias szi='sudo zypper install'
alias szr='sudo zypper remove'
alias szs='sudo zypper search'
alias szu='sudo zypper update'
alias ta='tmux attach'
alias tb='sh /home/nsujir/nithins-configs/scripts/tb.sh'
alias tbzh='tar --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=*.unsigned --exclude=*.sig --exclude=*.digest --exclude=cscope.* --exclude=tags --exclude=vmlinux --exclude=.tmp_vmlinu* -jcvfh'
alias tbz='tar --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=*.unsigned --exclude=*.sig --exclude=*.digest --exclude=cscope.* --exclude=tags --exclude=vmlinux --exclude=.tmp_vmlinu* -jcvf'
alias tf='tree -A'
alias tgb='ssh root@tgb'
alias tl='telnet x86 9090'
alias tm='tmux'
alias t='tree -Ad'
alias tx='telnet x86'
alias tz='tar --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=*.unsigned --exclude=*.sig --exclude=*.digest --exclude=cscope.* --exclude=tags --exclude=vmlinux --exclude=.tmp_vmlinu* -zcvf'
alias ua='uname -a'
alias un='uname -a'
alias vef='sudo vim /etc/fstab'
alias vg="echo sudo vim /boot/grub/grub.conf && sudo vim /boot/grub/grub.conf"
alias vh="echo sudo vim /etc/hosts && sudo vim /etc/hosts"
alias vi=vim
alias vlm='sudo tail -f /var/log/messages'
alias vn='vncserver -geometry 1900x1000'
alias xr='xrandr --output DP-2 --right-of DP-1'
alias xv='xvncviewer -noraiseonbeep'
alias zi='zenity --info'

# P4 aliases
alias p4opened='p4 opened'

#Tintri
alias assim='/auto/e2e/bin/assimilate.py --ignore_quarantined --ignore_owner'
alias bb='./build.sh build -j 16'
alias be='pushd $TOPDIR/platform/os/extdrivers; ./build.sh build -j 16; popd'
alias bec='pushd $TOPDIR/platform/os/extdrivers; ./build.sh clean; popd'
alias bi='./build.sh install'
alias bt='pushd $TOPDIR/platform/os/tools; ./build.sh build -j 16; popd'
alias btc='pushd $TOPDIR/platform/os/tools; ./build.sh clean; popd'
alias hbd='hg bookmark -d'
alias hd='hg vd'
alias hdc='hg diff -g -c .'
alias hgb='hg bookmarks'
alias hgc0='hg commit -m "bug 0"'
alias hgca='hg commit --amend'
alias hgc='hg commit'
alias hgd='hg diff -g'
alias hgg='hg glog -b .'
alias hgh='hg histedit'
alias hgi='hg in -b .'
alias hgk='hg backup'
alias hgo='hg out -r .'
alias HGP='hg purge --all'
alias HGR='hg revert --all'
alias hgs='hg status'
alias hgv='hg backup && hg review'
alias ltx='ls -lrt ../../distro_bld/local_rpms/RPMS/x86_64/txos*'
alias nvm='ssh -X nsujir-vm'
alias pxe='ssh -X pxesrv1'
alias tvm='ssh -X test-vm205'
alias uvm='ssh -X nsujir-ubuntu14'

alias rsv='rsync -av --exclude="*.swp" $HOME/nithins-configs nsujir-vm:'
alias upgl='cd; /auto/e2e/bin/UpgradeTools.py install --rpmpath `readlink latest` '

# Tintri Build
alias ws='export TOPDIR=/data/workspaces/build0; cd $TOPDIR/platform/os'
alias ws1='export TOPDIR=/data3/workspaces/build1; cd $TOPDIR/platform/os'
alias ws2='export TOPDIR=/data2/workspaces/build2; cd $TOPDIR/platform/os'
alias ws3='export TOPDIR=/data2/workspaces/build3; cd $TOPDIR/platform/os'
alias ws4='export TOPDIR=/data3/workspaces/build4; cd $TOPDIR/platform/os'
alias ws5='export TOPDIR=/data3/workspaces/build5; cd $TOPDIR/platform/os'
alias ws6='export TOPDIR=/data3/workspaces/build6; cd $TOPDIR/platform/os'

alias ix='cd $TOPDIR/platform/os/extdrivers/intel/enet/ixgbe-3.11.33/src'
alias os='cd $TOPDIR/platform/os'
alias fs='cd $TOPDIR/fs'
alias ui='cd $TOPDIR/ui'


#!/bin/bash
alias a2c='aria2c -s 8 -x 8'
alias ac='autoconf'
alias acs='apt-cache search'
alias am='automake'
alias app='sudo aptitude purge ~c'
alias c="clear"
alias cho='sudo chown -R nsujir'
alias cls='clear;ls'
alias cpi='cat /proc/interrupts'
alias cpu='cat /proc/cpuinfo'
alias d='cd ..'
alias e='evince'
alias eg="export P4DIFF='gvimdiff -f'"
alias ep="export P4DIFF='diff -bru'"
alias f='find . -iname'
alias g3artman="/google/data/ro/teams/oneplatform/g3artman"
alias gar='git am --reject'
alias gcp='git cherry-pick'
alias gd='gitvimdiff'
alias gdc='gitvimdiff --cached'
alias gg4="git status | grep -e modified -e new | awk '{print \$4;}' | xargs gvim"
alias ggc='git gc'
alias gg="git status | grep -e modified -e new | awk '{print \$3;}' | xargs gvim"
alias g='gvim -geometry 135x60'
alias gib='git branch'
alias gica='git commit --amend'
alias gicA='git commit -a --amend --no-edit'
alias gicb='git checkout -b'
alias gic='git commit'
alias gic.='git commit -am .'
alias gich='git checkout'
alias gicl='git clone'
alias gidc='git diff --cached'
alias gid='git diff'
alias gifu='git fetch upstream'
alias gi='grep -I -i -n'
alias gih='git help'
alias gil='git log'
alias giln='gil --name-only'
alias gilp='git log -p'
alias gimb='git checkout master; git branch'
alias gim='git checkout master'
alias gimu='git merge upstream/master'
alias gin='git init && git add . && git commit -am "init" && git gc'
#alias gio='git log --branches --not --remotes=origin'
alias gip='git pull'
alias gir='git reset'
alias GIR='git reset --hard'
alias girH='git rebase -i HEAD~10'
alias girh='git rebase -i HEAD~5'
alias giri='git rebase -i'
alias GIS='git reset --soft'
alias gis='git status'
alias giu='git update-index --assume-unchanged'
alias gmm='git merge master'
alias golv='git am --resolved'
alias gow='git show'
alias gp='g4 pending -s relativepath'
alias gps='git5 presubmit'
alias grm='git rebase master'
alias gsy='git5 sync'
alias gtc='git tag --contains'
alias ha='history -a'
alias hn='history -n'
alias ind='indent -linux -il0 -bad -nbbo'
alias k='killall -9'
alias la='ls -A'
alias lld='ll | grep ^d'
alias ll='ls -l --color'
alias l='ls -CF'
alias loc='locate -i'
alias mck='make menuconfig KCONFIG_CONFIG=arch/x86/configs/tintri.config'
alias mcl='make clean'
alias mc='make menuconfig'
alias md='mkdir'
alias mi='make install'
alias mj='export CPUS=`grep processor /proc/cpuinfo | wc -l`; make -j $[$CPUS*2]'
alias mjmi='export CPUS=`grep processor /proc/cpuinfo | wc -l`; make -j $[$CPUS*2] && sudo make modules_install && sudo make install && sync'
alias mm='export CPUS=`grep processor /proc/cpuinfo | wc -l`; make modules -j $[$CPUS*2]'
alias mmi='sudo make modules_install && sync'
alias mmmi='export CPUS=`grep processor /proc/cpuinfo | wc -l`; make modules -j $[$CPUS*2] && sudo make modules_install && sync'
alias mps='ps -eo pid,ppid,rss,vsize,pcpu,cmd --sort=vsize'
alias od='objdump -Sld'
alias p4d='p4 diff ... | colordiff | less'
alias p='ping google.com'
alias pst='pstree -G'
alias saar='sudo apt-get autoremove'
#alias sai='sudo apt-get install'
#alias sar='sudo apt-get remove --purge'
alias saud='sudo apt-get dist-upgrade -y'
alias saug='sudo apt-get upgrade'
alias sau='sudo apt-get update'
alias scp='scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
alias sei='sudo ethtool -i'
alias sek='sudo ethtool -k'
alias seK='sudo ethtool -K'
alias se='sudo ethtool'
alias si='sudo ifconfig'
alias SI='sudo init 0'
alias sk='sudo killall -9'
alias smi='sudo make install'
alias spand='/google/data/rw/projects/spanner/links/span.daily'
#alias ssh='ssh -y -Y -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
alias ss='sudo setpci -s'
alias s='sudo'
alias sys='sudo yum search'
alias sy='sync';
#alias syu='sudo yum update'
alias ta='tmux attach'
alias tat='tmux attach -t'
alias tbzh='tar --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=*.unsigned --exclude=*.sig --exclude=*.digest --exclude=cscope.* --exclude=tags --exclude=vmlinux --exclude=.tmp_vmlinu* -jcvfh'
alias tbz='tar --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=*.unsigned --exclude=*.sig --exclude=*.digest --exclude=cscope.* --exclude=tags --exclude=vmlinux --exclude=.tmp_vmlinu* -jcvf'
alias tf='tree -A'
alias tm='tmux'
alias tns='tmux new-session -s'
alias t='tree -Ad'
alias tz='tar --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=*.unsigned --exclude=*.sig --exclude=*.digest --exclude=cscope.* --exclude=tags --exclude=vmlinux --exclude=.tmp_vmlinu* -zcvf'
alias ua='uname -a'
alias vh="echo sudo vim /etc/hosts && sudo vim /etc/hosts"
alias vi=vim
alias vlm='sudo tail -f /var/log/messages'
alias vn='vncserver -geometry 1900x1000'
alias yw='yum whatprovides'

#Tintri
alias hbd='hg bookmark -d'
alias hd='hg vd'
alias hdc='hg diff -g -c .'
alias hgcl='hg clone'
alias hgb='hg bookmarks'
alias hgca='hg commit --amend'
alias hgg='hg log -G -b .'
#alias hgd='hg diff -g -p -I "listfile:$HOME/hgdiffinc.txt"'
alias hgh='hg histedit'
alias hghc='hg histedit --continue'
alias hgi='hg in -b .'
alias hgk='hg backup'
alias hgo='hg out -n -r .'
alias HGP='hg purge --all'
alias HGR='hg revert --all'
alias hgs='hg status'
alias hgv='hg backup && hg review'

alias vd='P4DIFF=vimdiff g4 diff'


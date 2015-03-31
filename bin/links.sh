set -x
touch $HOME/.bash_local
ln -sf $HOME/nithins-configs/.hgrc $HOME
ln -sf $HOME/nithins-configs/hgignore $HOME/.hgignore
ln -sf $HOME/nithins-configs/hgdiffinc $HOME/.hgdiffinc
ln -sf $HOME/nithins-configs/.tudurc $HOME
ln -sf $HOME/nithins-configs/.gitconfig $HOME
ln -sf $HOME/nithins-configs/.gitignore $HOME
ln -sf $HOME/nithins-configs/.gvimrc $HOME
ln -sf $HOME/nithins-configs/.gvimrc $HOME/.vimrc
ln -sf $HOME/nithins-configs/.mrxvtrc $HOME
ln -sf $HOME/nithins-configs/.vim $HOME
ln -sf $HOME/nithins-configs/.vrapperrc $HOME
ln -sf $HOME/nithins-configs/.inputrc $HOME
ln -sf $HOME/nithins-configs/.bashrc $HOME
ln -sf $HOME/nithins-configs/.bash_aliases $HOME
ln -sf $HOME/nithins-configs/.bash_aliases $HOME/.ba
ln -sf $HOME/.bash_local $HOME/.bl
ln -sf $HOME/nithins-configs/.bash_exports $HOME
ln -sf $HOME/nithins-configs/.bash_exports $HOME/.be
ln -sf $HOME/nithins-configs/.bash_funcs $HOME
ln -sf $HOME/nithins-configs/.bash_funcs $HOME/.bf
ln -sf $HOME/nithins-configs/.tmux.conf $HOME/
ln -sf $HOME/nithins-configs/.fonts.conf $HOME/
ln -sf $HOME/nithins-configs/bin $HOME
ln -sf $HOME/nithins-configs/ $HOME/nc

ssh-keygen -t rsa
ln -sf $HOME/nithins-configs/ssh_config .ssh/config

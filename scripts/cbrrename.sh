for ((i=0; i<9; i++)); do fil=$(ls -1 f1* | head -n 1); comix $fil; read -rei $oldname; echo "mv -i $fil $REPLY.cbr"; mv -i $fil $REPLY.cbr; oldname=$ {
	REPLY/-*/
}-; done

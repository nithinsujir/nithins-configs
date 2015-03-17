echo; echo "Client 1";
cd $tm1
ls -oght *ppc.tar.gz;
echo; echo "Client 2";
cd $tm2
ls -oght *ppc.tar.gz;
echo; echo "Client3";
cd $tm3
ls -oght *ppc.tar.gz

echo; echo "Client 1"; 
cd $tm1
ls -oght *x86.tar.gz;
echo; echo "Client 2";
cd $tm2
ls -oght *x86.tar.gz;
echo; echo "Client3";
cd $tm3
ls -oght *x86.tar.gz

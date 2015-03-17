dirs=( 
       component/Fim 
       component/FimSoaker
       component/Ics
       component/Mog
       component/NvUtil
       component/Og
       component/pmCommon
       component/SysCommon 
       component/Trc
       mcm/moapps
       mcm/McmUtil
       mcm/MoError
       mcm/equipment
       mcm/UpgradeRestore
       mcm/TP
     )

dirs=(
        component/
        mcm/
     )

rm /tmp/cscope.files
rm tags

for di in ${dirs[@]}
do
    echo "Processing $di"

    find $di -name "*.cpp" >> /tmp/cscope.files
    find $di -name "*.hpp" >> /tmp/cscope.files
    find $di -name "*.h" >> /tmp/cscope.files

    ctags -aR $di
done

echo "Copying cscope.files to local dir"
cp /tmp/cscope.files .

ls -l cscope.*

cscope -bq

echo "Done generating cscope"

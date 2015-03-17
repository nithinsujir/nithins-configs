dirs=( 
       component/ChassisConnMngr
       component/ConnMngr
       component/DH
       component/Db
       component/EH
       component/EvtAggregator
       component/Fim 
       component/FimSoaker
       component/Ics
       component/Mog
       component/Net
       component/NvUtil
       component/ObCo
       component/ObCommon
       component/ObMo
       component/Og
       component/OsEncap
       component/OsThreadPool
       component/Ssm
       component/SsmCommon
       component/SsmCoordinator
       component/SysCfg
       component/SysCommon 
       component/TH
       component/Trc
       component/Util
       h/
       mcm/Alarm
       mcm/CMog
       mcm/equipment
       mcm/McmUtil
       mcm/moapps
       mcm/MoError
       mcm/Security/
       mcm/TP
       mcm/UpgradeRestore
       sys/mcm
     )

#dirs=(
#        component/
#        mcm/
#        h/
#     )

rm cscope.files
rm tags /tmp/tags
rm obfiles

for di in ${dirs[@]}
do
    echo "Processing $di"

    find $di -name "*.cpp" >> cscope.files
    find $di -name "*.hpp" >> cscope.files
    find $di -name "*.h" >> cscope.files
    find $di -name "*.ob" >> obfiles

    ctags -f /tmp/tags -aR --c++-kinds=+p --fields=+ia --extra=+q --language-force=C++ $di

done

ls -l cscope.*

/usr/local/bin/cscope -bq
cp /tmp/tags .

echo "Done generating cscope"

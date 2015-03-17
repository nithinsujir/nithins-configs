import os
import shutil
import sys

def delete_pfne():
    wrk_area = os.getenv('INF_WRK_AREA') + r'\pf_ne'
    print 'Deleting ' + wrk_area
    shutil.rmtree(wrk_area)
    sys.exit(0)

def delete_file(fil):
    print fil + ': ',
    try:
        if os.path.isdir(fil):
            shutil.rmtree(fil)
        else:
            os.remove(fil)

        print 'Deleted'

    except OSError:
        print 'Unable to delete'
        pass
        #raise


qnxtemp = os.path.dirname(os.path.dirname(os.getenv('TEMP')))
delete_file(os.path.join(os.path.join(qnxtemp, 'cmn'), 'temp'))
delete_file(os.path.join(os.path.join(qnxtemp, 'dlm'), 'temp'))
delete_file(os.path.join(os.path.join(qnxtemp, 'mcm'), 'temp'))
delete_file(os.path.join(os.path.join(qnxtemp, 'oa'), 'temp'))


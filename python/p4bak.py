import os
import P4
import tarfile
import time
import shutil
import filecmp
import logging

CLIENTS = ['nsujir-1', 'nsujir-2', 'nsujir-3']

logger = logging.getLogger('p4bak')

fileHandler = logging.FileHandler(r'c:\p4bak.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler.setFormatter(formatter)


logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

p4 = P4.P4()
p4.connect()

backupdir = r'h:\backups'

def get_latest_tar(client):
    client_backup = os.path.join(backupdir, client)

    # Create the backup directory if it doesn't exist
    try:
        os.makedirs(client_backup)
    except OSError:
        print 'Directory ' + client_backup + ' exists'

    fils = os.listdir(client_backup)

    latest = fils[0]

    for fil in fils:
        if (os.path.getmtime(os.path.join(client_backup, fil)) >
            os.path.getmtime(os.path.join(client_backup, latest))):
            latest = fil

    return os.path.join(client_backup, latest)


def backup(client):
    logger.info('Processing client: ' + client)
    client_backup = os.path.join(backupdir, client)
    p4.client = client

    opened = p4.run('opened')

    if len(opened) > 0:
        now = time.localtime()
        tar_name = time.strftime('%b_%d_%I_%M_%S_%p.tar', now)

        tar = tarfile.open(tar_name, 'w')

        for item in opened:
            p4_file = item['clientFile']
            local_file = p4.run('where', p4_file)[0]['path']
            tar.add(local_file)

        tar.close()

        latest_tar = get_latest_tar(client)
        logger.info('Latest backup: ' + latest_tar)

        logger.info('Comparing ' + latest_tar + ' and ' + tar_name)

        if filecmp.cmp(latest_tar, tar_name) == False:
            logger.info('Files differ')
            logger.info('Copied ' + tar_name + ' to ' + client_backup)
            shutil.copy(tar_name, client_backup)
        else:
            logger.info('No differences found')

        os.remove(tar_name)
    else:
        logger.info('Files not opened for client ' + client)


logger.info('')
logger.info('------------[ Starting Backup ]--------------------------------')
for client in CLIENTS:
    backup(client)


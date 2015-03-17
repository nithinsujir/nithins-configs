#!/usr/bin/python
import httplib
import logging
import re
import time
import sys

CONF_FILE = '/home/nsujir/.warm-cache'
SERVER = '10.220.0.40'

def read_last():
    config_fd = open(CONF_FILE, 'r')
    lin = config_fd.readline()
    config_fd.close()

    m = re.match('last_sync = (.*)', lin)
    if m:
        return int(m.group(1))
    else:
        raise NameError('Last not found')


def update_last(last):
    config_fd = open(CONF_FILE, 'w')
    config_fd.write('last_sync = %d' % last)
    config_fd.close()


logger = logging.getLogger('warm_cache')

fileHandler = logging.FileHandler(r'/tmp/warm-cache.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler.setFormatter(formatter)


logger.addHandler(fileHandler)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

last_sync = read_last()
#logger.info('Syncing from %d' % last_sync)


def get_incrementing(start, end):
    for review_id in xrange(start, end):
        h = httplib.HTTPConnection(SERVER)
        logger.info('Requesting diff for %s' % review_id)
        h.request('GET', '/r/%s/diff/' % review_id)
        r = h.getresponse()
        d = r.read()
        logger.info('Status: %s Response: %s' % (r.status, r.reason))
        h.close()

def get_all_on_page():
    h = httplib.HTTPConnection('10.220.0.40')
    h.request('GET', '/r/')
    r = h.getresponse()
    data = r.read()
    h.close()

    # Get diffs for all reviews on front page
    for review_id in re.findall(r'<a href="/r/(\d+)/"', data):
        logger.info('Requesting diff for %s' % review_id)
        h = httplib.HTTPConnection('10.220.0.40')
        h.request('GET', '/r/%s/diff/' % review_id)
        r = h.getresponse()
        d = r.read()
        logger.info('Status: %s Response: %s' % (r.status, r.reason))
        h.close()

def continue_sync():
    global last_sync
    h = httplib.HTTPConnection('10.220.0.40')
    h.request('GET', '/r/?sort=-time_added')
    r = h.getresponse()
    data = r.read()
    h.close()

    m = re.search(r'<a href="/r/(\d+)/"', data)
    latest = int(m.group(1))

    if last_sync < latest:
        logger.info('Syncing from %d to %d' % (last_sync + 1, latest))
        for review_id in xrange(last_sync + 1, latest + 1):
            h = httplib.HTTPConnection('10.220.0.40')
            logger.info('Requesting diff for %s' % review_id)
            h.request('GET', '/r/%s/diff/' % review_id)
            r = h.getresponse()
            d = r.read()
            logger.info('Status: %s Response: %s' % (r.status, r.reason))
            h.close()

            update_last(review_id)
            last_sync = review_id


#get_all_on_page()
#sys.exit(0)

continue_sync()



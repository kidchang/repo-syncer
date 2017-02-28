#!/usr/bin/env python

import syncer

CONF = {
    "worker_num": 21,
    "flavor": "intermediate"
}


def sync():
    try:
        source_syncer = syncer.Syncer(CONF['worker_num'], sync_flavor=CONF['flavor'])
        source_syncer.sync()
    except Exception as error:
        print 'Sync failed!'
        print error


if __name__ == '__main__':
    sync()

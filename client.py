#!/usr/bin/env python

import argparse
import syncer


def sync(worker_num, flavor, branch_path):
    try:
        source_syncer = syncer.Syncer(worker_num, flavor, branch_path)
        source_syncer.sync()
    except Exception as error:
        print 'Sync failed!'
        print error


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--worker_num", type=int, default=21,
                        help="number of workers")
    parser.add_argument("-f", "--flavor", type=str, default="greedy",
                        help="which flavor to map sources to workers")
    parser.add_argument("-b", "--branch_path", type=str, default="",
                        help="branch path of the repo on workers")
    args = parser.parse_args()
    worker_num = args.worker_num
    flavor = args.flavor
    branch_path = args.branch_path
    sync(worker_num, flavor, branch_path)

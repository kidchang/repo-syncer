#!/usr/bin/env python

import os
import yaml

def clean_ansible():
    with open('config.yml', 'r') as config_file:
        ansible_dir = config_file['ansible_dir']

    if os.path.exists(ansible_dir):
        os.rmdir(ansible_dir)


if __name__ == '__main__':
    clean_ansible()

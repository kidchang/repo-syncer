#!/usr/bin/env python

import os
import shutil
import yaml

def clean_ansible():
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)
        ansible_dir = config['ansible_dir']

    if os.path.exists(ansible_dir):
        shutil.rmtree(ansible_dir)


if __name__ == '__main__':
    clean_ansible()

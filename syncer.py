"""Module to manage scheduling, spawning and syncing.
"""

from jinja2 import Template

import os
import utils
import yaml

FLAVOR_MAPPING = {
    "satisfied": 6,
    "intermediate": 4,
    "greedy": 3
}



class Syncer(object):
    """Syncer module."""
    def __init__(self, worker_num, sync_flavor, branch_path):
        self.workers_per_source = FLAVOR_MAPPING[sync_flavor]
        self.worker_num = worker_num
        self.sync_flavor = sync_flavor
        self.branch_path = branch_path
        with open('config.yml', 'r') as config_file:
            config = yaml.load(config_file)
            self.all_sources = config['sources']
            self.all_workers = config['workers']
            self.ansible_dir = config['ansible_dir']
        if not os.path.exists(self.ansible_dir):
            os.mkdir(self.ansible_dir)


    def _get_num_of_sources(self, worker_num):
        return worker_num/self.workers_per_source


    def _spawn_sources(self, source_num):
        """spawning a list of names of source machines for syncing."""
        return self.all_sources[0:source_num]


    def map_sources(self, source_list):
        mapping = {}
        redundant_num = self.worker_num % len(source_list)
        if redundant_num:
            redundant_workers = self.all_workers[-redundant_num:]
            workers = self.all_workers[:-redundant_num]
        else:
            redundant_workers = []
            workers = self.all_workers
        start = 0
        for source in source_list:
            mapping[source] = workers[start:start+self.workers_per_source]
            if redundant_workers:
                mapping[source].append(redundant_workers.pop())
            start = start+self.workers_per_source
        return mapping


    def _sync(self, source_worker_mapping):
        inventory_file = os.path.join(self.ansible_dir, 'inventory.yml')
        vars_file = os.path.join(self.ansible_dir, 'group_vars/all')
        self._generate_inventories(source_worker_mapping, inventory_file)
        self._generate_vars(source_worker_mapping, vars_file)
        cmd = "ANSIBLE_CONFIG=%s ansible-playbook -i %s sync.yml" % (os.path.join(self.ansible_dir),
                                                                     inventory_file)

#        with open(os.path.join(self.ansible_dir, 'run.log')) as logfile:
#            subprocess.Popen(cmd, shell=True, stdout=logfile, stderr=logfile)


    def _generate_inventories(self, source_worker_mapping, inventory_file):
        source_dict = {'sources': source_worker_mapping.keys()}
        utils.render_jinja_templates('templates/inventory.yml.j2', source_dict, inventory_file)


    def _generate_vars(self, source_worker_mapping, ansible_vars):
        vars_dir = os.path.join(self.ansible_dir, 'group_vars')
        if not os.path.exists(vars_dir):
            os.mkdir(vars_dir)
        mapping = {'source_worker_mapping': source_worker_mapping}
        mapping['branch_path'] = self.branch_path
        utils.render_jinja_templates('templates/vars.j2', mapping, ansible_vars)


    def sync(self):
        source_num = self._get_num_of_sources(self.worker_num)
        source_list = self._spawn_sources(source_num)
        source_worker_mapping = self.map_sources(source_list)
        self._sync(source_worker_mapping)

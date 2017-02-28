"""Module to manage scheduling, spawning and syncing.
"""

from jinja2 import Template

import yaml
import utils

FLAVOR_MAPPING = {
    "satisfied": 6,
    "intermediate": 4,
    "greedy": 3
}



class Syncer(object):
    """Syncer module."""
    def __init__(self, worker_num, sync_flavor='greedy'):
        self.workers_per_source = FLAVOR_MAPPING[sync_flavor]
        self.worker_num = worker_num
        self.sync_flavor = sync_flavor
        self.sources_list = _spawn_sources(self.num_of_sources)
        with open('config.yml', 'r') as config_file:
            config = yaml.load(config_file)
            self.all_sources = config['sources']
            self.all_workers = config['workers']
            self.inventory_file = config['inventory_file']
            self.ansible_vars = config['ansible_vars']

    @staticmethod
    def _get_num_of_sources(worker_num, sync_flavor):
        return worker_num/self.workers_per_source


    @staticmethod
    def _spawn_sources(source_num):
        """spawning a list of names of source machines for syncing."""
        return self.all_sources[0:source_num]


    def map_sources(self, source_list):
        mapping = {}
        redundant_num = self.worker_num % len(source_list)
        redundant_workers = self.all_workers[-redundant_num:]
        workers = self.all_workers[:-redundant_num]
        start = 0
        for source in source_list:
            mapping[source] = [start, start+self.workers_per_source]
            if redundant_workers:
                mapping[source].append(reduntant_workers.pop())
        return mapping


    @staticmethod
    def _prepare_ansible_environment(source_worker_mapping):
        _generate_inventories(source_worker_mapping, self.inventory_file)
        _generate_vars(source_worker_mapping, self.ansible_vars)

        def _generate_inventories(source_worker_mapping, inventory_file):
            source_dict = {'sources': source_worker_mapping.keys()}
            utils.render_jinja_templates('templates/inventory.yml.j2', source_dict, inventory_file)

        def _generate_vars(source_worker_mapping, ansible_vars):
            utils.render_jinja_templates('templates/vars.j2', source_worker_mapping, ansible_vars)

    def sync(self):
        source_num = _get_num_of_sources(self.worker_num, self.sync_flavor)
        source_list = _spawn_sources(source_num)
        source_worker_mapping = self.map_sources(source_list)
        _prepare_ansible_environment(source_worker_mapping)

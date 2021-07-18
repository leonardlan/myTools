'''YAML tools.'''

from ruamel.yaml import YAML


def load_yaml(file_path):
    '''Return data from yaml file.'''
    yaml = YAML()
    with open(file_path, 'r') as fil:
        return yaml.load(fil)

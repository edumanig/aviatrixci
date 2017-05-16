from __future__ import print_function
from __future__ import unicode_literals

import logging
import io
import sys

def parse_yaml(yaml_file):
    """
    Parse a yaml file, returning its contents as a dict
    """
    try:
        import yaml
    except ImportError:
        sys.exit('Unable to import yaml module.')

    try:
        with io.open(yaml_file, encoding='utf-8') as fname:
            return yaml.load(fname)
    except IOError:
        sys.exit('Unable to open YAML file: {0}'.format(yaml_file))


def create_logger(file_name):
    # create logger
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger

import configparser
import os
import sys


def read():
    """Return the application configurations."""
    file_location = os.path.abspath(os.path.dirname(sys.argv[0]))
    inifile = file_location + '/config.cfg'
    config = configparser.ConfigParser()
    config.read(inifile, encoding='utf-8')
    return config

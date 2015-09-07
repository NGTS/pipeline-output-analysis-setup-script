#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import os
import subprocess as sp
from contextlib import contextmanager
import sys
import tempfile
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

MINICONDA_ROOT = 'https://repo.continuum.io/miniconda'


def miniconda_url():
    ''' 
    Return the miniconda url for the architecture of the current machine
    '''
    endpoint_map = {
        'linux': 'Miniconda-latest-Linux-x86_64.sh',
        'darwin': 'Miniconda-latest-MacOSX-x86_64.sh',
    }
    for os_type in endpoint_map:
        if sys.platform.startswith(os_type):
            return os.path.join(MINICONDA_ROOT, endpoint_map[os_type])



@contextmanager
def change_directory(path):
    old_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_cwd)


def download_install_script():
    location = os.path.join(
        tempfile.gettempdir(),
        os.path.split(miniconda_url())[-1])

    with open(location, 'wb') as outfile:
        response = urllib2.urlopen(miniconda_url())
        data = response.read()
        outfile.write(data)
    return location


def install_miniconda(script_path, name):
    dest = os.path.join(
        os.getcwd(), name)
    cmd = ['bash', script_path, '-b', '-f', '-p', dest]
    sp.check_call(cmd)


def main(args):
    with change_directory(args.directory):
        install_location = download_install_script()
        install_miniconda(install_location, args.environment_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory',
                        required=False,
                        default=os.getcwd())
    parser.add_argument('-n', '--environment-name', required=False,
                        default='miniconda')
    main(parser.parse_args())

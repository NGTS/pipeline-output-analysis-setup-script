#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import os
import subprocess as sp
from contextlib import contextmanager
import sys
import logging
import tempfile
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

logging.basicConfig(level='INFO', format='%(levelname)7s %(message)s')
logger = logging.getLogger(__name__)


def miniconda_url():
    ''' 
    Return the miniconda url for the architecture of the current machine
    '''
    miniconda_root = 'https://repo.continuum.io/miniconda'
    endpoint_map = {
        'linux': 'Miniconda-latest-Linux-x86_64.sh',
        'darwin': 'Miniconda-latest-MacOSX-x86_64.sh',
    }
    for os_type in endpoint_map:
        logger.debug('Trying os type: %s', os_type)
        if sys.platform.startswith(os_type):
            url = os.path.join(miniconda_root, endpoint_map[os_type])
            logger.debug('OS type found: %s', os_type)
            logger.info('Miniconda url: %s', url)
            return url


@contextmanager
def change_directory(path):
    old_cwd = os.getcwd()
    try:
        logger.debug('Changing directory to %s', path)
        os.chdir(path)
        yield
    finally:
        logger.debug('Changing directory to %s', old_cwd)
        os.chdir(old_cwd)


def run(cmd, env=None):
    str_cmd = list(map(str, cmd))
    logger.debug('Running command: `%s`', ' '.join(str_cmd))
    sp.check_call(cmd, env=env)


def download_install_script(url):
    logger.info('Downloading install script')
    location = os.path.join(tempfile.gettempdir(), os.path.split(url)[-1])
    logger.debug('Download destination: %s', location)

    with open(location, 'wb') as outfile:
        logger.debug('Sending web request')
        response = urllib2.urlopen(url)
        logger.debug('Response received')
        data = response.read()
        logger.debug('Parsing response')
        outfile.write(data)
    return location


def install_miniconda(script_path, name):
    dest = os.path.join(
        os.getcwd(), name)
    cmd = ['bash', script_path, '-b', '-f', '-p', dest]
    sp.check_call(cmd)


def main(args):
    if args.verbose:
        logger.setLevel(logging.DEBUG)

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

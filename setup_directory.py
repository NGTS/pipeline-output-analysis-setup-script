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
    logger.info('Installing miniconda to %s', name)
    dest = os.path.join(os.getcwd(), name)
    run('bash', script_path, '-b', '-f', '-p', dest)


def print_shell_integration_info(environment_path):
    print('''To activate your new environment, run:

    export PATH={path}/bin:${{PATH}}'''.format(path=environment_path))


def install_required_packages(environment_path, custom_packages):
    default_packages = [
        'pip',
        'astropy',
        'matplotlib',
        'scipy',
        'numpy',
        'seaborn',
        'ipython',
    ]

    new_env = os.environ.copy()
    new_env['PATH'] = ':'.join([
        os.path.join(environment_path, 'bin'), new_env['PATH']
    ])
    cmd = ['conda', 'install', '--yes']
    cmd.extend(default_packages)
    cmd.extend(custom_packages)
    run(cmd, env=new_env)


def main(args):
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    script_url = miniconda_url()

    with change_directory(args.directory):
        install_location = download_install_script(script_url)
        install_miniconda(install_location, args.environment_name)
    environment_path = os.path.join(args.directory, args.environment_name)

    install_required_packages(environment_path, args.package)
    print_shell_integration_info(environment_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory',
                        required=False,
                        default=os.getcwd())
    parser.add_argument('-n', '--environment-name',
                        required=False,
                        default='miniconda')
    parser.add_argument('-p', '--package',
                        help='Custom packages to install',
                        nargs='*',
                        default=[])
    parser.add_argument('-v', '--verbose', action='store_true')
    main(parser.parse_args())

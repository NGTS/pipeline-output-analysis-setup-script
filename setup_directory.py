#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import os
import subprocess as sp
from contextlib import contextmanager
import tempfile
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

MINICONDA_URL = 'https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh'


def main(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory',
                        required=False,
                        default=os.getcwd())
    main(parser.parse_args())

# Analysis setup script

This script allows a quick setup for analysing a fits file. It installs miniconda to a local directory (in the cwd) and installs the likely required packages. It presents the user with commands to activate the conda environment for their shell.

## Usage

Use the `setup_directory.py` script to install a fresh `miniconda` installation to (by default) the current directory with the name (default) `miniconda`. The package contains the following libraries:

* pip
* astropy
* matplotlib
* scipy
* numpy
* seaborn
* ipython

More packages can be specified when the script is run with the `-p/--package` flag.

## Program help

```
usage: setup_directory.py [-h] [-d DIRECTORY] [-n ENVIRONMENT_NAME]
                          [-p [PACKAGE [PACKAGE ...]]] [-v]

Set up a miniconda installation

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory to install to (default:
                        /Users/simon/work/NGTS/pipeline-output-analysis-setup-
                        script)
  -n ENVIRONMENT_NAME, --environment-name ENVIRONMENT_NAME
                        Name to call install directory (default: miniconda)
  -p [PACKAGE [PACKAGE ...]], --package [PACKAGE [PACKAGE ...]]
                        Custom packages to install (default: [])
  -v, --verbose

By default it installs a `miniconda` installation to the current directory
under the `miniconda` path. The PATH environment variable must be altered to
use this new installation. How to do this is explained after installation
completes.
```

from __future__ import print_function

import os
import errno
import stat
import tempfile
import subprocess
import platform

from distutils.spawn import find_executable
from hashlib import md5
from urllib import urlopen

USER_DIR = os.path.join(os.path.expanduser('~'), '.casa')
BIN_DIR = os.path.join(os.path.expanduser('~'), '.casa', 'bin')
USER_SITE = os.path.join(os.path.expanduser('~'), '.casa', 'lib', 'python2.6', 'site-packages')

PIP_URL = "https://pypi.python.org/packages/source/p/pip/pip-1.5.4.tar.gz"
PIP_MD5 = "834b2904f92d46aaa333267fb1c922bb"


def mkdir_p(path):
    # Create a directory using mkdir -p
    # Solution provided on StackOverflow
    try:
        os.makedirs(path)
    except OSError as exc:
        if not(exc.errno == errno.EEXIST and os.path.isdir(path)):
            raise


def make_executable(filename):
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


def get_casapy_path():
    return os.path.realpath(find_executable('casapy'))


def get_python_version_mac():
    casapy_path = get_casapy_path()
    parent = os.path.dirname(casapy_path)
    python = os.path.join(parent, 'python')
    p = subprocess.Popen([python, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    version = p.stderr.read().split()[1][:3]
    print("Determined Python version in CASA... {0}".format(version))
    return version


def get_python_version_linux():
    casapy_path = get_casapy_path()
    parent = os.path.dirname(os.path.dirname(casapy_path))
    if os.path.exists(os.path.join(parent, 'lib64', 'python2.6')):
        version = "2.6"
    elif os.path.exists(os.path.join(parent, 'lib64', 'python2.7')):
        version = "2.7"
    else:
        raise ValueError("Could not determine Python version")
    print("Determined Python version in CASA... {0}".format(version))
    return version


def install_pip(pv="2.7"):

    print("Downloading pip...")

    # Create temporary directory

    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)

    # Download pip and expand

    content = urlopen(PIP_URL).read()

    if md5(content).hexdigest() != PIP_MD5:
        raise ValueError("pip checksum does not match")

    with open(os.path.basename(PIP_URL), 'wb') as f:
        f.write(content)

    # Prepare installation script

    print("Installing pip...")

    site_packages = os.path.expanduser('~/.casa/lib/python{pv}/site-packages'.format(pv=pv))
    mkdir_p(site_packages)

    PIP_INSTALL = """
#!/bin/bash
export PYTHONUSERBASE=$HOME/.casa
export PATH=$HOME/.casa/bin:$PATH
tar xvzf {pip_filename}
cd {pip_name}
casa-python setup.py install --prefix=$HOME/.casa
    """

    pip_filename = os.path.basename(PIP_URL)
    pip_name = pip_filename.rsplit('.', 2)[0]

    with open('install_pip.sh', 'w') as f:
        f.write(PIP_INSTALL.format(pip_filename=pip_filename, pip_name=pip_name))

    make_executable('install_pip.sh')

    # Need to use subprocess instead
    retcode = os.system('./install_pip.sh')
    if retcode != 0:
        raise SystemError("pip installation failed!")


def write_casa_python_mac(pv="2.7"):

    print("Creating casa-python script...")

    TEMPLATE_PYTHON = """
#!/bin/sh

INSTALLPATH={casapy_path}

PROOT=$INSTALLPATH/Frameworks/Python.framework/Versions/{pv}
PBIND=$PROOT/MacOS
PLIBD=$PROOT/lib/python{pv}
PPATH=$PBIND:$PLIBD:$PLIBD/plat-mac:$PLIBD/plat-darwin
PPATH=$PPATH:$PBIND/lib-scriptpackages:$PLIBD/lib-tk
PPATH=$PPATH:$PLIBD/lib-dynload:$PLIBD/site-packages
PPATH=$PPATH:$PLIBD/site-packages/Numeric:$PLIBD/site-packages/PyObjC
PPATH=$INSTALLPATH/Resources/python:$PPATH

export PYTHONUSERBASE=$HOME/.casa

export PYTHONHOME=$PROOT
export PYTHONPATH=$PPATH
export PYTHONEXECUTABLE=$PROOT/Resources/Python.app/Contents/MacOS/Python

export DYLD_FRAMEWORK_PATH="$INSTALLPATH/Frameworks"

exec -a pythonw $INSTALLPATH/MacOS/pythonw -W ignore::DeprecationWarning "$@"
    """

    mkdir_p(BIN_DIR)

    casapy_path = os.path.dirname(os.path.dirname(get_casapy_path()))

    with open(os.path.join(BIN_DIR, 'casa-python'), 'w') as f:
        f.write(TEMPLATE_PYTHON.format(casapy_path=casapy_path, pv=pv))

    make_executable(os.path.join(BIN_DIR, 'casa-python'))


def write_casa_python_linux(pv="2.7"):

    print("Creating casa-python script...")

    TEMPLATE_PYTHON = """
#!/bin/sh

INSTALLPATH={casapy_path}

export LD_LIBRARY_PATH=$INSTALLPATH/lib64:/lib64:/usr/lib64:$LD_LIBRARY_PATH
export LDFLAGS="-L$INSTALLPATH/lib64/"

export PYTHONHOME=$INSTALLPATH

export PYTHONUSERBASE=$HOME/.casa

export PYTHONPATH=$INSTALLPATH/lib64/python{pv}/site-packages:$PYTHONPATH
export PYTHONPATH=$INSTALLPATH/lib64/python{pv}/heuristics:$PYTHONPATH
export PYTHONPATH=$INSTALLPATH/lib64/python{pv}:$PYTHONPATH

exec $INSTALLPATH/lib64/casapy/bin/python $*
    """

    mkdir_p(BIN_DIR)

    casapy_path = os.path.dirname(os.path.dirname(get_casapy_path()))

    with open(os.path.join(BIN_DIR, 'casa-python'), 'w') as f:
        f.write(TEMPLATE_PYTHON.format(casapy_path=casapy_path, pv=pv))

    make_executable(os.path.join(BIN_DIR, 'casa-python'))


def write_casa_pip():

    print("Creating casa-pip script...")

    TEMPLATE_PIP = """
$HOME/.casa/bin/casa-python $HOME/.casa/bin/pip $* --user
    """

    with open(os.path.join(BIN_DIR, 'casa-pip'), 'w') as f:
        f.write(TEMPLATE_PIP)

    make_executable(os.path.join(BIN_DIR, 'casa-pip'))


def write_init():

    print("Creating init.py script...")

    TEMPLATE_INIT = """
import site
site.addsitedir("{site_packages}")
    """

    with open(os.path.join(USER_DIR, 'init.py'), 'a') as f:
        f.write(TEMPLATE_INIT.format(site_packages=USER_SITE))


def add_bin_to_path():
    # TODO: make this happne in future
    print("You should now add {0} to your PATH".format(BIN_DIR))


if __name__ == "__main__":

    if platform.system() == 'Darwin':

        python_version = get_python_version_mac()
        write_casa_python_mac(pv=python_version)

    else:

        python_version = get_python_version_linux()
        write_casa_python_linux(pv=python_version)

    install_pip(pv=python_version)
    write_casa_pip()
    write_init()

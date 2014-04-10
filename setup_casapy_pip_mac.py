import os
import errno

from distutils.spawn import find_executable
from hashlib import md5
from urllib import urlopen

def mkdir_p(path):
    """
    Create a directory using mkdir -p

    Solution provided on StackOverflow
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if not(exc.errno == errno.EEXIST and os.path.isdir(path)):
            raise

def make_executable(filename):
    import os
    import stat
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


# DEFINE CONSTANTS

PIP_URL = "https://pypi.python.org/packages/source/p/pip/pip-1.5.4.tar.gz"

TEMPLATE_PYTHON = """
#!/bin/sh

INSTALLPATH={casapy_path}

PROOT=$INSTALLPATH/Frameworks/Python.framework/Versions/2.6
PBIND=$PROOT/MacOS
PLIBD=$PROOT/lib/python2.6
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

TEMPLATE_PIP = """
$HOME/.casa/bin/casa-python $HOME/.casa/bin/pip $* --user
"""

TEMPLATE_INIT = """
import site
site.addsitedir("{site_packages}")
"""

# SET UP PIP ENVIRONMENT

# Go to a work directory

import tempfile
tmpdir = tempfile.mkdtemp()
os.chdir(tmpdir)

print "Creating temporary directory {0}".format(tmpdir)

# Find path to CASA

# we use realpath in case /usr/bin/casapy is a sympolic link
casapy_path = os.path.dirname(os.path.dirname(os.path.realpath(find_executable('casapy'))))

print "Finding path to casapy... {0}".format(casapy_path)

# Set up casa-python script

print "Setting up casa-python"

bin_dir = os.path.expanduser('~/.casa/bin/')
mkdir_p(bin_dir)

with open(os.path.join(bin_dir, 'casa-python'), 'w') as f:
    f.write(TEMPLATE_PYTHON.format(casapy_path=casapy_path))

make_executable(os.path.join(bin_dir, 'casa-python'))

# Download the pip tar file and verifying the checksum

print "Downloading and installing pip"

content = urlopen(PIP_URL).read()

if md5(content).hexdigest() != "834b2904f92d46aaa333267fb1c922bb":
    raise ValueError("pip checksum does not match")

with open(os.path.basename(PIP_URL), 'wb') as f:
    f.write(content)

# Install it to .casa directory

site_packages = os.path.expanduser('~/.casa/lib/python2.6/site-packages')
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
pip_name = pip_filename.rsplit('.',2)[0]

with open('install_pip.sh', 'w') as f:
    f.write(PIP_INSTALL.format(pip_filename=pip_filename, pip_name=pip_name))

make_executable('install_pip.sh')

# Need to use subprocess instead
retcode = os.system('./install_pip.sh')
if retcode != 0:
    raise SystemError("pip installation failed")

# Now create casapy-pip tool

print "Setting up casa-pip"

with open(os.path.join(bin_dir, 'casa-pip'), 'w') as f:
    f.write(TEMPLATE_PIP)

make_executable(os.path.join(bin_dir, 'casa-pip'))

# Finally edit init.py to make casapy pick up .casa installed packages

print "Setting up init.py"

with open(os.path.expanduser('~/.casa/init.py'), 'a') as f:
    f.write(TEMPLATE_INIT.format(site_packages=site_packages))

print "You should now add {0} to your PATH".format(bin_dir)
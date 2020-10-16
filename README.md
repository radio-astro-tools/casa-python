CASA Python executable wrapper
==============================

The approach described below is deprecated.

Instead, follow instructions here:
https://docs.astropy.org/en/stable/install.html#installing-astropy-into-casa
to install astropy or other packages into CASA.

About
-----

``casa-python`` is a simple script that allows users to invoke the 
Python executable for [CASA](http://casa.nrao.edu/) as one would 
invoke a normal Python executable. This allows users to easily install 
third-party libraries into CASA. To do this, whenever installation 
instructions require you to run for example ``python setup.py install``, 
instead use:

    casa-python setup.py install

We also provide an interface to the ``pip`` package manager, ``casa-pip``. One can install
any\* python package this way:

    casa-pip install requests

Installation
------------

The installation requires that you have CASA installed.  You can check this by doing 

    $ which casa

at the command prompt.  You should see the path to the file.

To install, download the latest version of the ``casa-python`` script from
[here](https://raw.githubusercontent.com/radio-tools/casa-python/master/setup_casapy_pip.py)
and run it.  This should be your *system* python, not *CASA* python (which
should be on your path by default).

    python setup_casapy_pip.py

or, alternatively:

    curl -O https://raw.githubusercontent.com/radio-tools/casa-python/master/setup_casapy_pip.py
    python setup_casapy_pip.py

You should then add `$HOME/.casa/bin/` to your path.

Example
-------

To install Astropy into CASA, assuming you have the appropriate compilers on
your system, you can run

    casa-pip install astropy

Once the installation has completed, you can start up CASA as usual, and 
Astropy should be available:

    CASA Version 4.1.0 (r22971)
      Compiled on: Thu 2013/02/21 17:38:25 UTC
    ___________________________________________________________________
        For help use the following commands:
        tasklist               - Task list organized by category
        taskhelp               - One line summary of available tasks
        help taskname          - Full help for task
        toolhelp               - One line summary of available tools
        help par.parametername - Full help for parameter name
    ___________________________________________________________________
    Activating auto-logging. Current session state plus future input saved.
    Filename       : ipython-20130319-150704.log
    Mode           : backup
    Output logging : False
    Raw input log  : False
    Timestamping   : False
    State          : active
    *** Loading ATNF ASAP Package...
    *** ... ASAP (trunk rev#22948) import complete ***

    CASA <2>: import astropy

    CASA <3>: 


Caveats
-------

Packages requiring c-compiled code rely on the existence of a C-compiler on
your unix path.

Alternatives
------------

Rather than install packages into CASA, it is also possible (although a little hackier) to try and import CASA into your existing Python installation - see [here](http://newton.cx/~peter/2014/02/casa-in-python-without-casapy/) for more details.

Credits
-------

The wrapper was prepared by Thomas Robitaille (@astrofrog) based on code from
CASA, with contributions from Adam Leroy and Adam Ginsburg (@keflavich).

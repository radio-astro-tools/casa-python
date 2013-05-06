CASA Python executable wrapper
==============================

About
-----

``casa-python`` is a simple script that allows users to invoke the 
Python executable for [CASA](http://casa.nrao.edu/) as one would 
invoke a normal Python executable. This allows users to easily install 
third-party libraries into CASA. To do this, whenever installation 
instructions require you to run for example ``python setup.py install``, 
instead use:

    casa-python setup.py install

Installation
------------

To install, download the latest version of the ``casa-python`` script
from [here](https://raw.github.com/astrofrog/casa-python/master/casa-python)
and place it in any directory that is in your ``$PATH``.

Example
-------

To install Astropy into CASA, you can download the latest stable release 
from the [Astropy homepage](http://www.astropy.org/) then expand it 
and install it with e.g.:

    tar xvzf astropy-0.2.tar.gz
    cd astropy-0.2
    casa-python setup.py install

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

Known limitations
-----------------

The wrapper script currently assumes that CASA.app is located inside
/Applications, and that casapy uses Python 2.6. The wrapper will need to be
updated once CASA switches to a more recent version of Python.

Credits
-------

The wrapper was prepared by Thomas Robitaille (@astrofrog) based on code from
CASA.

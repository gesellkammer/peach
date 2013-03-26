"""
peach, a successor of pitchtools
"""

import os
import sys

from numpy.distutils.core import setup, Extension
from setuphelp import info_factory, NotFoundError

f = open('version.cfg')
VERSION = f.readline().strip()

def is_valid_version(s):
    def is_valid_int(s):
        try:
            int(s)
        except ValueError:
            return False
        return True
    digits = s.split('.')
    o = len(digits) == 3
    o = all(is_valid_int(digit) for digit in digits) and o
    return o

assert is_valid_version(VERSION)
print "version = ", VERSION

descr    = __doc__.split('\n')[1:-1]; del descr[1:3]

classifiers = """
Development Status :: 2 - Pre-Alpha
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Operating System :: MacOS
Operating System :: POSIX
Operating System :: Unix
Programming Language :: C
Programming Language :: Cython
Programming Language :: Python
Programming Language :: Python :: 2
Topic :: Scientific/Engineering
Topic :: Software Development :: Libraries :: Python Modules
"""

keywords = """
scientific computing
music
"""

platforms = """
Linux
Mac OS X
"""


metadata = {
    'name'             : 'peach',
    'version'          : VERSION,
    'description'      : descr.pop(0),
    'long_description' : '\n'.join(descr),
    'url'              : '',
    'download_url'     : '', 
    'author'           : '',
    'author_email'     : '',
    'maintainer'       : '',
    'maintainer_email' : '',
    'classifiers'      : [c for c in classifiers.split('\n') if c],
    'keywords'         : [k for k in keywords.split('\n')    if k],
    'platforms'        : [p for p in platforms.split('\n')   if p],
    }



def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    confgr = Configuration('peach',parent_package,top_path)
    confgr.add_extension('_peach', ['_peach.c']) # , extra_info=sf_config)
    return confgr

def cython_setup(annotate=False):
    annotate = "-a" if annotate else ""
    os.system("cython %s _peach.pyx" % annotate)

if __name__ == "__main__":
    cython_setup()
    from numpy.distutils.core import setup as numpy_setup
    config = configuration(top_path='').todict()
    config.update(metadata)
    numpy_setup(**config)

import os, sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# ----------------------------------------------
# monkey-patch for parallel compilation
# ----------------------------------------------
def parallelCCompile(self, sources, output_dir=None, macros=None, include_dirs=None, debug=0, extra_preargs=None, extra_postargs=None, depends=None):
    # those lines are copied from distutils.ccompiler.CCompiler directly
    macros, objects, extra_postargs, pp_opts, build =  self._setup_compile(output_dir, macros, include_dirs, sources, depends, extra_postargs)
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)
    # parallel code
    N = 2 # <---------- number of parallel compilations
    import multiprocessing.pool
    def _single_compile(obj):
        try: src, ext = build[obj]
        except KeyError: return
        self._compile(obj, src, ext, cc_args, extra_postargs, pp_opts)
    # convert to list, imap is evaluated on-demand
    list(multiprocessing.pool.ThreadPool(N).imap(_single_compile,objects))
    return objects
import distutils.ccompiler
distutils.ccompiler.CCompiler.compile = parallelCCompile

# -----------------------------------------------------------------------------
# Global
# -----------------------------------------------------------------------------

# detect platform
platform = os.uname()[0] if hasattr(os, 'uname') else 'Windows'

# get numpy include directory
try:
    import numpy
    try:
        numpy_include = numpy.get_include()
    except AttributeError:
        numpy_include = numpy.get_numpy_include()
except ImportError:
    print 'Error: Numpy was not found.'
    sys.exit(1)

include_dirs = ['peach', numpy_include]
compile_args = ["-march=i686"]

peach_ext = Extension(
    '_peach',
    sources = ['peach/_peach.pyx'],
    include_dirs = include_dirs,
    extra_compile_args = compile_args
)   

setup(
    name = 'peach',
    ext_modules = [peach_ext],
    cmdclass = {'build_ext':build_ext},
    packages = ['peach']
)
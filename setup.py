from  __future__ import print_function, absolute_import
import os, sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

include_dirs = ['peach']
compile_args = []

platform = os.uname()[0] if hasattr(os, 'uname') else 'Windows'
if platform == 'Windows':
    compile_args.append("-march=i686")

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

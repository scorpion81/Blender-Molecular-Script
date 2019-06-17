import setuptools
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython.Compiler.Options 

Cython.Compiler.Options.annotate = True

ext_modules = [Extension("cmolcore", ["cmolcore.pyx"],extra_compile_args=['/Ox','/openmp','/GT','/arch:SSE2','/fp:fast'])]

setup(
  name = 'Molecular script',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)

import platform
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import Cython.Compiler.Options


os_name = platform.architecture()[1]
Cython.Compiler.Options.annotate = True
module_name = 'core'

if os_name == "WindowsPE":
    ext_modules = [Extension(
        module_name,
        ['core' + '.pyx'],
        extra_compile_args=['/Ox','/openmp','/GT','/arch:SSE2','/fp:fast']
    )]
else:
    ext_modules = [Extension(
        module_name,
        ['core' + '.pyx'],
        extra_compile_args=['-O3','-msse4.2','-ffast-math']
    )]

setup(
    name = 'Molecular script',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)

import platform
from distutils.core import setup
from Cython.Distutils import build_ext, Extension
import Cython.Compiler.Options


os_name = platform.architecture()[1]
Cython.Compiler.Options.annotate = True
module_name = 'core'
is_linux = platform.architecture()[1] == "ELF" or platform.system() == "Linux"

if os_name == "WindowsPE":
    ext_modules = [Extension(
        module_name,
        ['core' + '.pyx'],
        extra_compile_args=['/Ox','/openmp','/GT','/arch:SSE2','/fp:fast'],
        cython_directives={'language_level' : "3", 'cpow': True}
    )]
elif is_linux:
     ext_modules = [Extension(
        module_name,
        ['core' + '.pyx'],
        extra_compile_args=['-O3','-msse4.2','-ffast-math','-fno-builtin'],
        extra_link_args=['-lm'],
        cython_directives={'language_level' : "3", 'cpow': True}
    )]
else:
    # under mac OS, with the advent of the M1 ARM chips, its necessary to build an universal intel/arm binary.
    # this is done by passing -arch arm64 -arch x86_64 from here to clang, the default mac OS compiler.

    ext_modules = [Extension(
        module_name,
        ['core' + '.pyx'],
        extra_compile_args=['-O3','-msse4.2','-ffast-math','-fno-builtin','-arch','arm64e','-arch','x86_64','-arch','arm64'],
        extra_link_args=['-lm','-arch','arm64e','-arch','x86_64','-arch','arm64'],
        cython_directives={'language_level' : "3", 'cpow': True}
    )]

setup(
    name = 'Molecular script',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)

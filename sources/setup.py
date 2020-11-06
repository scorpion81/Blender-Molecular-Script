import platform, os, shutil
from distutils.core import setup
from Cython.Distutils import build_ext, Extension
import Cython.Compiler.Options


os_name = platform.architecture()[1]
Cython.Compiler.Options.annotate = True
PYX = '.pyx'
source_dir = os.path.dirname(os.path.abspath(__file__))
repo_dir = os.path.dirname(source_dir)
addon_folder = os.path.join(repo_dir, 'molecular')
ext_modules = []

for root, dirs, files in os.walk('.'):
    for file in files:
        module_name, extension = os.path.splitext(file)
        module_name = module_name.lower()
        extension = extension.lower()
        if extension == PYX:
            if os_name == "WindowsPE":
                module = Extension(
                    module_name,
                    [os.path.join(root, module_name + '.pyx')],
                    extra_compile_args=['/Ox','/openmp','/GT','/arch:SSE2','/fp:fast'],
                    cython_directives={'language_level' : "3"}
                )
                ext_modules.append(module)
            else:
                ext_modules.append(Extension(
                    module_name,
                    [os.path.join(root, module_name + '.pyx')],
                    extra_compile_args=['-O3','-msse4.2','-ffast-math','-fno-builtin'],
                    extra_link_args=['-lm'],
                    cython_directives={'language_level' : "3"}
                ))

setup(
    name = 'Molecular',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)

for root, dirs, files in os.walk('.'):
    for file in files:
        module_name, extension = os.path.splitext(file)
        module_name = module_name.lower()
        extension = extension.lower()
        if not extension in ('.pyx', '.pyd', '.py', '.bat'):
            os.remove(os.path.join(root, file))

shutil.rmtree('build')

for root, dirs, files in os.walk('.'):
    for file in files:
        module_name, extension = os.path.splitext(file)
        module_name = module_name.lower()
        extension = extension.lower()
        pyd_file_path = os.path.join(addon_folder, file)
        if os.path.exists(pyd_file_path):
            os.remove(pyd_file_path)
        if extension == '.pyd':
            os.rename(
                os.path.join(root, file),
                pyd_file_path
            )

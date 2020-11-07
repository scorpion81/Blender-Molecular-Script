import platform, os, shutil
from distutils.core import setup
from Cython.Distutils import build_ext, Extension
import Cython.Compiler.Options


os_name = platform.architecture()[1]
Cython.Compiler.Options.annotate = True
PYX = '.pyx'
source_dir = os.path.dirname(os.path.abspath(__file__))
addon_folder = os.path.join(os.path.dirname(source_dir), 'molecular', 'core')
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
    name='Molecular',
    cmdclass={'build_ext': build_ext},
    include_dirs=['.'],
    ext_modules=ext_modules
)

for root, dirs, files in os.walk('.'):
    for file in files:
        module_name, extension = os.path.splitext(file)
        module_name = module_name.lower()
        extension = extension.lower()
        if not extension in ('.pyx', '.pyd', '.pxd', '.py', '.bat'):
            os.remove(os.path.join(root, file))

shutil.rmtree('build')

addon_path = os.environ.get('BLENDER_USER_ADDON_PATH', None)
if addon_path:
    if addon_path[:-1] == '/':
        addon_path = addon_path[:-1]
    if not addon_path.endswith(os.path.join('scripts', 'addons')):
        raise BaseException('Incorrect addons path')
core_folder = os.path.join(addon_path, 'molecular', 'core')

for root, dirs, files in os.walk('.'):
    for file in files:
        module_name, extension = os.path.splitext(file)
        module_name = module_name.lower()
        extension = extension.lower()
        pyd_file_path = os.path.join(addon_folder, file)
        if os.path.exists(pyd_file_path):
            os.remove(pyd_file_path)
        if extension == '.pyd':
            if addon_path:
                print('#', os.path.join(core_folder, file))
                shutil.copyfile(
                    os.path.join(root, file),
                    os.path.join(core_folder, file)
                )
            os.rename(
                os.path.join(root, file),
                pyd_file_path
            )

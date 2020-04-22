from molecular import bl_info
from zipfile import ZipFile, ZIP_DEFLATED
from os import path, walk, remove, chdir, getcwd
import shutil
import sys
from subprocess import Popen, PIPE

chdir(getcwd()+"\\sources")

try:
    remove("core.cp37-win_amd64.pyd")
    remove("core.html")
    remove("core.c")
    shutil.rmtree("build")
except:
    pass

#TODO, blenders (or a compatible) python bin needs to be in $PATH, and if you use blender's you need to copy the python includes from SVN
#into the include folder of blenders python, too

with Popen([sys.executable, "setup.py", "build_ext", "--inplace"], stdout=PIPE) as proc:
    print(proc.stdout.read())
   
    shutil.move("core.cp37-win_amd64.pyd", "..\\molecular\\core.cp37-win_amd64.pyd")

    chdir("..")

    with ZipFile('molecular_{}_'.format(('.'.join(map(str, bl_info['version'])))) + 'win.zip', 'w') as z:
        for root, _, files in walk('molecular'):
            for file in files:
                if not file.endswith('.py') and not file.endswith('.pyd'):
                    continue
                z.write(path.join(root, file), compress_type=ZIP_DEFLATED)

    chdir(getcwd()+"\\molecular")
    try: 
        remove("core.cp37-win_amd64.pyd")
    except:
        pass
    chdir("..")
